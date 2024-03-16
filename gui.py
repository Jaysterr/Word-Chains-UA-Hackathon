from nicegui import ui, Client

from GameManager import *
from nicegui.events import *
from GameManager import GameManager
import asyncio

input_fields = []
pointer = 0
@ui.page('/')
def init_gui():
    while(len(input_fields) != 0):
        input_fields.pop()
    
    with ui.tabs().classes('w-full') as tabs:
        standard = ui.tab("Standard Mode")
        not_standard = ui.tab("Not Standard Mode")
    with ui.tab_panels(tabs, value=standard).classes('w-full'):
        with ui.tab_panel(standard).classes("items-center"):
            timer = ui.label()
            with ui.row(wrap=False).classes("content-center"):
                for i in range(5):
                    input_fields.append(ui.input().classes("w-1/6 text-2xl").props('input-class="text-center" filled'))
                    input_fields[i].disable()
            ui.button(on_click=lambda: focus(input_fields[2]))
            textfield = ui.input("enter a word here!").classes("object-center")
            ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
            label = ui.label()

        with ui.tab_panel(not_standard).classes('w-full'):
            ui.label("woah you found the not standard page").classes('text-emerald-500')
            
    otp_set = [ui.input(on_change=lambda i=i: focus(i+1)) for i in range(4)]
    otp_set[0].props('autofocus')

    print(pointer)
    with ui.header(elevated=True):
        ui.markdown("# **Word Chains**")
    textfield = ui.input("enter a word here!")
    game = GameManager()
    ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
    label = ui.label()

    # with ui.left_drawer(top_corner=True, bottom_corner=True):
    #     ui.label("left")

    # ui.add_head_html(r'''
    # <style>
    # @keyframes fade {
    # from {opacity: 0;}
    # to {opacity: 1.0;}
    # }
    # </style>
    # ''')

    ui.label('Hello world!').style('animation: fade 3s')
    # ui.timer(0.001, lambda: timer.set_text("{0:.3f}s".format(game.get_time_elapsed() / (10**9)))) # alt timer style
    ui.timer(0.001, lambda: timer.set_text(format_timer(game.get_time_elapsed() / (10**9))))
    keyboard = ui.keyboard(on_key=handle_key)
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
