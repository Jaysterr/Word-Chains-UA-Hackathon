from nicegui import ui, Client

from GameManager import *
from nicegui.events import *

input_fields = []
import asyncio

@ui.page('/')
def init_gui():
    pointer = 0
    while(len(input_fields) != 0):
        input_fields.pop()
    async def javascript_stuff():
        ui.run_javascript(f"document.getElementById({input_fields[3].id}).select()")
    with ui.tabs().classes('w-full') as tabs:
        standard = ui.tab("Standard Mode")
        not_standard = ui.tab("Not Standard Mode")
        
    with ui.tab_panels(tabs, value=standard).classes('w-full'):
        with ui.tab_panel(standard).classes("items-center"):
            with ui.row(wrap=False).classes("content-center"):
                for i in range(5):
                    input_fields.append(ui.input().classes("w-1/6 text-2xl").props('input-class="text-center" filled'))
            ui.button(on_click=javascript_stuff)
            textfield = ui.input("enter a word here!").classes("object-center")
            ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
            label = ui.label()
        with ui.tab_panel(not_standard).classes('w-full'):
            ui.label("woah you found the not standard page").classes('text-emerald-500')
            
    with ui.header(elevated=True):
        ui.markdown("# **Word Chains**")
    textfield = ui.input("enter a word here!")
    game = GameManager()
    ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
    label = ui.label()
    label2 = ui.label()
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
    # ui.timer(0.001, lambda: label2.set_text("{0:.3f}s".format(game.get_time_elapsed() / (10**9)))) # alt timer style
    ui.timer(0.001, lambda: label2.set_text(format_timer(game.get_time_elapsed() / (10**9))))
    print(input_fields)
    ui.timer(0.001, lambda: input_fields[0].disable() if input_fields[0].value != "" else input_fields[0].enable())

    keyboard = ui.keyboard(on_key=handle_key)
    #ui.timer(1, lambda: print(keyboard))

    ui.run(native=True)
def format_timer(sec):
    ms = (sec % 1) * 1000
    s = sec // 1
    return str(int(s)) + "s " + "{0:02d}".format((int(ms//10))) #+ "ms"

def handle_key(e: KeyEventArguments):
    print(e.key)
    return str(e.key)

