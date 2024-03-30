'''
File: gui.py
This is a view manager for the game, contains all the code for the GUI

@authors: Jakob Garcia, Caroline Schwengler, Jesse Oved, Soren Abrams
Primary authors: Jesse Oved, Soren Abrams
'''
from nicegui import ui, app, native
from gamemanager import *
from nicegui.events import *
from gamemanager import GameManager
import os

script_dir = os.path.dirname(__file__)
rel_path = "data/how2play.md"
how_to_play_path = os.path.join(script_dir, rel_path)


checkboxes = [ui.checkbox]*5
input_fields = [0]*5 # empty list with 5 slots
pointer = 0
is_dark_mode = False
timer = None
theme = None # will contain day/night mode button
game = GameManager()
time_limit = game.get_time_limit()
game.set_time_limit(time_limit)
score_display = None
timer_circle_display = None
app.config.quasar_config['animations'] = [
    'fadeOutDown'
]

# UI
@ui.page('/')
def init_gui():
    global theme
    global game
    global checkboxes
    # configure color palette
    ui.colors(primary='#40798c', dark='#051923', secondary="#003554")
    
    # header and footer
    with ui.header(elevated=True).props("text-center"):
        with ui.row().classes("w-full items-center items-stretch"):
            with ui.dialog() as dialog, ui.card().classes("items-center"):
                with open(how_to_play_path) as file:
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
    with ui.tab_panels(tabs, value=standard).classes('w-full'):

        with ui.tab_panel(standard).classes("items-center"):
            main_game_area()

    
    with ui.card().tight().props("bordered").classes("w-full items-center"):
        with ui.card_section().classes("w-full bg-secondary text-white"):
            ui.label("Game Rules").classes("text-h6")
        with ui.card_section().classes(""):
            with ui.row():        
                checkboxes[0] = ui.checkbox("Single Letter Match" , value=True, on_change=lambda: game.toggle_gamemode(0))
                checkboxes[1] = ui.checkbox("Muti-Letter Match", on_change=lambda: game.toggle_gamemode(1))
                checkboxes[2] = ui.checkbox("First-Last Letter Match", on_change=lambda: game.toggle_gamemode(2))
                checkboxes[3] = ui.checkbox("Random Letter Match", on_change=lambda: game.toggle_gamemode(3))
                # checkboxes[4] = ui.checkbox("No Duplicate Letters (UNTESTED)", on_change=lambda: game.toggle_gamemode(4))    
    
    # RUN GUI
    ui.run(native=False, on_air='yYMC2uYoKa71WBMN')

    # This is the UI content of the main gameplay screen
def main_game_area():
    
    # This displays current score and highest score
    global score_display
    score_display = ui.label("Highscore: " + str(game.get_highscore()) + "\nScore: 0").classes("font-extrabold text-xl")
    
    # This is the progress ring that displays how much time you have left
    global timer_circle_display
    with ui.circular_progress(show_value=False, value=time_limit, max=time_limit).props('size="6rem" animation-speed="100"') as timer_circle_display:
        ui.label(time_limit).bind_text_from(timer_circle_display, 'value', backward=lambda x: (format_timer(x)))
    
    # updates the timer display every millisecond
    ui.timer(0.01, lambda: timer_update())
    
    # Setup the main text fields
    with ui.row(wrap=False).classes("w-2/3 justify-center"):
        for i in range(5):
            input_fields[i] = ui.input().classes("w-1/6 text-2xl").props('input-class="text-center" standout="bg-primary" v-model="text" filled mask="A"')
            input_fields[i].disable()

    # This allows us to capture keyboard events
    ui.keyboard(on_key=handle_key, ignore=[])


def assign_req_letters():
    req_letters = game.get_letters()
    for i in range(5):
        input_fields[i].set_value(req_letters[i])


# formats time as 00s 00(ms)
def format_timer(sec):
    ms = (sec % 1) * 1000
    s = sec // 1
    return str(int(s)) + "s " + "{0:02d}".format((int(ms//10))) #+ "ms"

# this is run every time a key is pressed
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
        while pointer >= 0 and game.get_req_letters()[pointer] != "":
            pointer -= 1
        if pointer < 0:
            pointer += 1
            while game.get_req_letters()[pointer] != "":
                pointer += 1
        input_fields[pointer].set_value("")
        input_fields[pointer].enable()
        focus(input_fields[pointer])

def enter(): # submit word to game, process results, reset text boxes to initial state for next round
    global pointer
    global checkboxes
    
    full = True
    for i in input_fields:
        full = full and i.value != ""
    if full:

        temp = [i for i in game.get_letters()]
        game.set_user_word([i.value.lower() for i in input_fields]) # input user word
        
        round_result = game.run_game([i.value.lower() for i in input_fields]) # run game

        if round_result is RoundResult.GOOD:
            checkboxes[0].disable()
            checkboxes[1].disable()
            checkboxes[2].disable()
            checkboxes[3].disable()
            # checkboxes[4].disable()
            
            # if won, update score, reset text fields, so they're filled with required letters of next round
            global score_display
            score_update(game.get_highscore(), game.get_score())
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
                
        elif round_result is RoundResult.REPEAT:
            ui.notify("GAME OVER:\n Reason: Repeated a word", type='negative')
            reset_gui()
        else:
            ui.notify("INVALID WORD", type='warning')
    else:
        ui.notify("WORD TOO SHORT", type='warning')

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


# inserts custom javascript code to focus on the passed in input field
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


def score_update(highscore: int, score: int):
    global score_display
    score_display.set_text("Highscore: " + str(highscore) + "\nScore: " + str(score))


def timer_update():
    global timer_circle_display
    timer_circle_display.set_value(game.get_time_elapsed() / (10 ** 9))
    if game.get_time_elapsed() / (10 ** 9) <= 0:
        timer_circle_display.set_value(0)
        ui.notify("GAME OVER:\n Reason: Ran out of time", type='negative')
        game.reset_game()
        reset_gui()
    
    
def reset_gui():
    global pointer
    global checkboxes
    global game
    checkboxes[0].enable()
    checkboxes[1].enable()
    checkboxes[2].enable()
    checkboxes[3].enable()
    # checkboxes[4].enable()
    pointer = 0
    reset_text_fields()
    score_update(game.get_highscore(), 0)    
