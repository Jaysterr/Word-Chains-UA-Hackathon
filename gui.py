from nicegui import ui, app, native
from gamemanager import *
from nicegui.events import *
from gamemanager import GameManager
import dataclasses

import os
script_dir = os.path.dirname(__file__)
rel_path = "how2play.md"
abs_file_path = os.path.join(script_dir, rel_path)

@dataclass
class SessionData:
    active_game_rules = [False]*3

input_fields = [0]*5 # empty list with 5 slots
pointer = 0
is_dark_mode = False
timer = None
theme = None # will contain day/night mode button
game = GameManager()
time_limit = 15
game.set_time_limit(time_limit)

app.config.quasar_config['animations'] = [
    'fadeOutDown'
]

@ui.page('/')
def init_gui():
    global theme
    global game
    # configure color palette
    ui.colors(primary='#40798c', dark='#051923', secondary="#003554")
    ui.add_head_html(r'''
    <style>
    @keyframes fadein {
    from {opacity: 0;}
    to {opacity: 1.0;}
    }
    @keyframes fadeout {
    from {opacity: 1.0;}
    to {opacity: 0;}
    }
    </style>
    ''')
    # header and footer
    with ui.header(elevated=True).props("text-center"):
        with ui.row().classes("w-full items-center items-stretch"):
            with ui.dialog() as dialog, ui.card().classes("items-center"):
                with open(abs_file_path) as file:
                    ui.markdown(file.read())
                ui.button('Close', on_click=dialog.close)
            
            ui.markdown("# **Word Chains**")
            ui.space()
            ui.button("How To Play", on_click=dialog.open, color='secondary').classes("text-lg")
            
    with ui.footer(elevated=True):
        theme = ui.button(icon="dark_mode", on_click=toggle_dark_mode)
    
    # main content
    with ui.tabs().classes('w-full') as tabs:
        standard = ui.tab("Game")
        highscores = ui.tab("Highscores")
    with ui.tab_panels(tabs, value=standard).classes('w-full'):

        with ui.tab_panel(standard).classes("items-center"):
            score_label = ui.label("Score: ")
            start_game_button = ui.button("Start Game!", on_click=initialize_game).props('enter-active-class="animated fadeIn"')#.classes("transition ease-in-out delay-150 bg-blue-500 hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 duration-300")
            main_game_area()

        with ui.tab_panel(highscores).classes('w-full'):
            highscore_chart()

    
    with ui.card().tight().props("bordered").classes("w-full items-center"):
        with ui.card_section().classes("w-full bg-secondary text-white"):
            ui.label("Game Rules").classes("text-h6")
        with ui.card_section().classes(""):
            with ui.row():        
                ui.checkbox("Single Letter Match (UNTESTED)" , value = True, on_change=lambda: game.toggle_gamemode(0))
                ui.checkbox("Muti-Letter Match (UNTESTED)", on_change=lambda: game.toggle_gamemode(1))
                ui.checkbox("First-Last Letter Match (TESTED)", value=True, on_change=lambda: game.toggle_gamemode(2))
                ui.checkbox("Random Letter Match (UNTESTED)", on_change=lambda: game.toggle_gamemode(3))
                ui.checkbox("No Duplicate Letters (UNTESTED)", on_change=lambda: game.toggle_gamemode(4))

            #ui.label().bind_text_from(SessionData, "active_game_rules", backward=lambda x: x.__str__())
    
    # ui.timer(0.001, lambda: timer.set_text("{0:.3f}s".format(game.get_time_elapsed() / (10**9)))) # alt timer style
    
    keyboard = ui.keyboard(on_key=handle_key, ignore=[])

    # DISABLE RELOAD WHEN BUILDING
    ui.run(reload=True, native=True, window_size=(1000, 850))
    #ui.run(reload=False, port=native.find_open_port(), native=True, window_size=(1000, 850))

    
def main_game_area():
    global timer
    with ui.circular_progress(show_value=False, value=time_limit, max=time_limit).props('size="6rem" animation-speed="100"') as timer_circle_display:
        timer = ui.label(time_limit).bind_text_from(timer_circle_display, 'value', backward=lambda x: (format_timer(x)))

    #ui.timer(0.001, lambda: timer.set_text(format_timer(game.get_time_elapsed() / (10**9))))
    ui.timer(0.01, lambda: timer_update())
    ui.timer(0.01, lambda: timer_circle_display.set_value(game.get_time_elapsed() / (10**9)))

    with ui.row(wrap=False).classes("w-2/3 justify-center"):
        for i in range(5):
            input_fields[i] = ui.input().classes("w-1/6 text-2xl").props('input-class="text-center" standout="bg-primary" v-model="text" filled mask="A"')
            input_fields[i].disable()


highscores = {"player 1" : 100000, "player 2" : 72000, "player 3" : 10000, "player 4" : 190000}            
def highscore_chart():
    chart = ui.echart(({
    'xAxis': {'type': 'value'},
    'yAxis': {'type': 'category', 'data': list(highscores.keys()), 'inverse': True},
    'legend': {'textStyle': {'color': 'gray'}},
    'series': [
        {'type': 'bar', 'name': 'Alpha', 'data': list(highscores.values())},
    ],
}))


def initialize_game():
    game.reset_game()
    assign_req_letters()
    input_fields[0].enable()
    input_fields[0].props("autofocus")
    pass

def assign_req_letters():
    req_letters = game.get_letters()
    for i in range(5):
        input_fields[i].set_value(req_letters[i])


def format_timer(sec):
    ms = (sec % 1) * 1000
    s = sec // 1
    return str(int(s)) + "s " + "{0:02d}".format((int(ms//10))) #+ "ms"

def handle_key(e: KeyEventArguments):
    if e.key == "Backspace" and e.action.keydown:
        backspace()
    elif e.key == "Enter" and e.action.keydown:
        enter()
    elif e.action.keydown:
        add_letter(str(e.key))

def backspace(): # clear current input and move to previous input
    global pointer
    if pointer > 0:
        if pointer <= 4:
            input_fields[pointer].set_value("")
            input_fields[pointer].disable()
        pointer -= 1
        while pointer >= 0 and game._req_letters[pointer] != "":
            pointer -= 1
        if pointer < 0:
            pointer += 1
            while game._req_letters[pointer] != "":
                pointer += 1
        input_fields[pointer].set_value("")
        input_fields[pointer].enable()
        focus(input_fields[pointer])

def enter(): # reset entire input state
    global pointer
    full = True
    for i in input_fields:
        full = full and i.value != ""
    if full:

        # word = ""
        # for i in input_fields:
        #     word += i.value.lower()
        temp = [i for i in game.get_letters()]
        game.set_user_word([i.value.lower() for i in input_fields]) # input user word
        # print(game.check_word(), game._req_letters, game._word_rules.get_prev_words())
        # print(pointer)
        # print(temp)
        
        did_win = game.run_game() # run game
        
        if did_win:
            
            # if  won, reset text fields, so they're filled with required letters of next round
            input_fields[0].enable()
            focus(input_fields[0])
            pointer = 0
            input_fields[0].set_value(game.get_letters()[0])
            input_fields[1].set_value(game.get_letters()[1])
            input_fields[2].set_value(game.get_letters()[2])
            input_fields[3].set_value(game.get_letters()[3])
            input_fields[4].set_value(game.get_letters()[4])

            # select first open text field
            while pointer < 5 and input_fields[pointer].value != "":
                input_fields[pointer].disable()
                pointer += 1
            if pointer <= 4:
                input_fields[pointer].enable()
                focus(input_fields[pointer])
        else:
            if not game.check_word()[1]:
                ui.notify("GAME OVER:\n Reason: Repeated a word")
                game_end()
            else:
                ui.notify("INVALID WORD")
    else:
        ui.notify("WORD TOO SHORT")

def add_letter(key): # add key to input and move to next input 
    global pointer
    if pointer <= 4:
        input_fields[pointer].set_value(key)
        if input_fields[pointer].value.isalpha() and len(
                input_fields[pointer].value) == 1:
            while pointer < 5 and input_fields[pointer].value != "":
                input_fields[pointer].disable()
                pointer += 1
            if pointer <= 4:
                input_fields[pointer].enable()
                focus(input_fields[pointer])
        else:
            input_fields[pointer].set_value("")

def focus(input_field) -> None:
    ui.run_javascript(f'getElement({input_field.id}).$refs.qRef.focus()')


def toggle_dark_mode():
    global is_dark_mode
    global theme
    if is_dark_mode:
        ui.dark_mode().disable()
        theme.props("icon=light_mode")
        is_dark_mode = False
    else:
        ui.dark_mode().enable()
        theme.props("icon=dark_mode")
        is_dark_mode = True

def reset_text_fields():
    for i in input_fields:
        i.set_value("")
        i.disable()
    input_fields[0].enable()
    focus(input_fields[0])
    global pointer
    pointer = 0


def timer_update():
    global timer
    timer.set_text(format_timer(game.get_time_elapsed() / (10 ** 9)))
    if game.get_time_elapsed() <= 0:
        timer.set_text(format_timer(0))
        game_end()
        ui.notify("GAME OVER:\n Reason: Ran out of time")


def game_end():
    global pointer
    pointer = 0
    game.reset_game()
    reset_text_fields()