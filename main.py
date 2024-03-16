from nicegui import ui

with ui.row():
    textfield = ui.input("enter a word here!")

with ui.row():
    ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
    
with ui.row():
    label = ui.label()
ui.run()