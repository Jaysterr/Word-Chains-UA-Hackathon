# main.py
# probably gonna be where all GUI stuff is handled, unless things become more complicated such has having multiple pages
from nicegui import ui
import GameManager

# TODO: Finish implementing a functional GUI. Eventually try to make it extra pretty

textfield = ui.input("enter a word here!")
ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
label = ui.label()

ui.run()