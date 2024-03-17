from nicegui import ui, Client

from GameManager import *
from nicegui.events import *
from GameManager import GameManager
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
    #ui.colors(dark='#cccccc')
    
    # header and footer
    with ui.header(elevated=True).props("text-center"):
        ui.markdown("# **Word Chains**")
    with ui.footer(elevated=True):
        theme = ui.button(icon="dark_mode", on_click=toggle_lightdark_mode)
    
    # main content
    with ui.tabs().classes('w-full') as tabs:
        standard = ui.tab("Standard Mode")
        not_standard = ui.tab("Not Standard Mode")
    with ui.tab_panels(tabs, value=standard).classes('w-full'):
        with ui.tab_panel(standard).classes("items-center"):
            timer = ui.label()
            with ui.row(wrap=False).classes("content-center"):
                for i in range(5):
                    input_fields[i] = ui.input().classes("w-1/6 text-2xl").props('input-class="text-center" filled')
                    input_fields[i].disable()
            ui.button("focus box 3 test", on_click=lambda: focus(input_fields[2]))

        with ui.tab_panel(not_standard).classes('w-full'):
            ui.label("woah you found the not standard page").classes('text-emerald-500')

    print(pointer)

    
    with ui.card().tight().props("bordered").classes("w-full items-center"):
        with ui.card_section().classes("w-full bg-primary text-white"):
            ui.label("Game Rules").classes("text-h6")
        with ui.card_section().classes(""):
            with ui.row():        
                ui.checkbox("first_last_match", on_change=lambda: SessionData.active_game_rules.__setitem__(0, not SessionData.active_game_rules[0]))
                ui.checkbox("random_letter_match", on_change=lambda: SessionData.active_game_rules.__setitem__(1, not SessionData.active_game_rules[1]))
                ui.checkbox("no_duplicate_letters", on_change=lambda: SessionData.active_game_rules.__setitem__(2, not SessionData.active_game_rules[2]))    
            #ui.label().bind_text_from(SessionData, "active_game_rules", backward=lambda x: x.__str__())
            
    # ui.timer(0.001, lambda: timer.set_text("{0:.3f}s".format(game.get_time_elapsed() / (10**9)))) # alt timer style
    ui.timer(0.001, lambda: timer.set_text(format_timer(game.get_time_elapsed() / (10**9))))
    keyboard = ui.keyboard(on_key=handle_key)
    
    # RUN UI
    ui.run(native=True)



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

def backspace():
    global pointer
    if pointer > 0:
        pointer -= 1
        input_fields[pointer].set_value("")
        # input_fields[pointer].enable()
        focus(input_fields[pointer])

def enter():
    global pointer
    full = True
    for i in input_fields:
        full = full and i.value != ""
    if full:
        input_fields[0].set_value("")
        input_fields[1].set_value("")
        input_fields[2].set_value("")
        input_fields[3].set_value("")
        input_fields[4].set_value("")
        pointer = 0

def add_letter(key):
    global pointer
    if pointer <= 4:
        input_fields[pointer].set_value(key)
        if input_fields[pointer].value.isalpha() and len(
                input_fields[pointer].value) == 1:
            input_fields[pointer].disable()
            pointer += 1
            if pointer <= 4:
                focus(input_fields[pointer])
        else:
            input_fields[pointer].set_value("")

def focus(input_field) -> None:
    ui.run_javascript(f'getElement({input_field.id}).$refs.qRef.focus()')


def toggle_lightdark_mode():
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