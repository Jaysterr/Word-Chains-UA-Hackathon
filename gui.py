from nicegui import ui, Client

from gamemanager import *
from nicegui.events import *
from gamemanager import GameManager
import dataclasses

@dataclass
class SessionData:
    active_game_rules = [False]*3

input_fields = [0]*5 # empty list with 5 slots
pointer = 0
is_dark_mode = False
theme = None # will contain day/night mode button
game = GameManager()





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
                with open("how2play.md") as file:
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
            start_game_button = ui.button("Start Game!", on_click=lambda:fade_out_button)
            main_game_area()

        with ui.tab_panel(highscores).classes('w-full'):
            highscore_chart()

    print(pointer)

    
    with ui.card().tight().props("bordered").classes("w-full items-center"):
        with ui.card_section().classes("w-full bg-secondary text-white"):
            ui.label("Game Rules").classes("text-h6")
        with ui.card_section().classes(""):
            with ui.row():        
                ui.checkbox("First Last Match", on_change=lambda: SessionData.active_game_rules.__setitem__(0, not SessionData.active_game_rules[0])).props("")
                ui.checkbox("Random Letter Match", on_change=lambda: SessionData.active_game_rules.__setitem__(1, not SessionData.active_game_rules[1]))
                ui.checkbox("No Duplicate Letters", on_change=lambda: SessionData.active_game_rules.__setitem__(2, not SessionData.active_game_rules[2]))    
                ui.checkbox("Game Letter Match", on_change=lambda: SessionData.active_game_rules.__setitem__(2, not SessionData.active_game_rules[2]))    

            #ui.label().bind_text_from(SessionData, "active_game_rules", backward=lambda x: x.__str__())
            
    # ui.timer(0.001, lambda: timer.set_text("{0:.3f}s".format(game.get_time_elapsed() / (10**9)))) # alt timer style
    
    keyboard = ui.keyboard(on_key=handle_key, ignore=[])

    # RUN UI
    ui.run(native=True, window_size=(1000, 850))

def fade_out_button():
    global start_game_button
    start_game_button.style('animation: fadeout 3s')
def main_game_area():
    timer = ui.label()
    ui.timer(0.001, lambda: timer.set_text(format_timer(game.get_time_elapsed() / (10**9))))
    with ui.row(wrap=False).classes("content-center"):
        for i in range(5):
            input_fields[i] = ui.input().classes("w-1/6 text-2xl").props('input-class="text-center" filled mask="A"')
            if i is not 0: 
                input_fields[i].disable()
            else:
                input_fields[0].props("autofocus")

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

def start_game():
    pass

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
        input_fields[pointer].set_value("")
        input_fields[pointer].enable()
        focus(input_fields[pointer])

def enter(): # reset entire input state
    global pointer
    full = True
    for i in input_fields:
        full = full and i.value != ""
    if full:
        input_fields[0].enable()
        focus(input_fields[0])
        pointer = 0

        input_fields[0].set_value("")
        input_fields[1].set_value("")
        input_fields[2].set_value("")
        input_fields[3].set_value("")
        input_fields[4].set_value("")

def add_letter(key): # add key to input and move to next input 
    global pointer
    if pointer <= 4:
        input_fields[pointer].set_value(key)
        if input_fields[pointer].value.isalpha() and len(
                input_fields[pointer].value) == 1:
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