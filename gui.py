from nicegui import ui
from GameManager import *

@ui.page('/')
def init_gui():
    with ui.header(elevated=True):
        ui.markdown("# **Word Chains**")
    textfield = ui.input("enter a word here!")
    game = GameManager()
    ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
    label = ui.label()
    label2 = ui.label()
    ui.add_head_html(r'''
    <style>
    @keyframes fade {
    from {opacity: 0;}
    to {opacity: 1.0;}
    }
    </style>
    ''')

    ui.label('Hello world!').style('animation: fade 3s')
    ui.timer(0.001, lambda: label2.set_text("{0:.3f}".format(game.get_time_elapsed() / (10**9))))

    ui.run(native=True)

