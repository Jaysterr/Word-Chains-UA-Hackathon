from nicegui import ui, Client

from GameManager import *
from nicegui.events import *
from GameManager import GameManager
import asyncio

input_fields = []
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
            ui.button(on_click=lambda: focus(input_fields[2]))
            textfield = ui.input("enter a word here!").classes("object-center")
            ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
            label = ui.label()

        with ui.tab_panel(not_standard).classes('w-full'):
            ui.label("woah you found the not standard page").classes('text-emerald-500')
            
    otp_set = [ui.input(on_change=lambda i=i: focus(i+1)) for i in range(4)]
    otp_set[0].props('autofocus')


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
    ui.timer(0.001, lambda: input_fields[0].disable() if input_fields[
                                                             0].value != "" else
    input_fields[0].enable())
    ui.timer(0.001, lambda: input_fields[1].disable() if input_fields[
                                                             1].value != "" else
    input_fields[1].enable())
    ui.timer(0.001, lambda: input_fields[2].disable() if input_fields[
                                                             2].value != "" else
    input_fields[2].enable())
    ui.timer(0.001, lambda: input_fields[3].disable() if input_fields[
                                                             3].value != "" else
    input_fields[3].enable())
    ui.timer(0.001, lambda: input_fields[4].disable() if input_fields[
                                                             4].value != "" else
    input_fields[4].enable())
    keyboard = ui.keyboard(on_key=handle_key)
    ui.run(native=True)

def format_timer(sec):
    ms = (sec % 1) * 1000
    s = sec // 1
    return str(int(s)) + "s " + "{0:02d}".format((int(ms//10))) #+ "ms"

def handle_key(e: KeyEventArguments):
    if e.key == "Backspace" and e.action.keydown:
        input_fields[0].set_value("")
        input_fields[1].set_value("")
        input_fields[2].set_value("")
        input_fields[3].set_value("")
        input_fields[4].set_value("")
    elif e.key == "Enter" and e.action.keydown:
        full = True
        for i in input_fields:
            full = full and i.value != ""
        if full:
            input_fields[0].set_value("")
            input_fields[1].set_value("")
            input_fields[2].set_value("")
            input_fields[3].set_value("")
            input_fields[4].set_value("")
            
def focus(input_field) -> None:
    ui.run_javascript(f'getElement({input_field.id}).$refs.qRef.focus()')
