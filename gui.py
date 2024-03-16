from nicegui import ui

@ui.page('/')
def init_gui():
    with ui.header(elevated=True):
        ui.markdown("# **Word Chains**")
    textfield = ui.input("enter a word here!")
    ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
    label = ui.label()

    ui.add_head_html(r'''
    <style>
    @keyframes fade {
    from {opacity: 0;}
    to {opacity: 1.0;}
    }
    </style>
    ''')

    ui.label('Hello world!').style('animation: fade 3s')
    
    
    ui.run(native=True)
