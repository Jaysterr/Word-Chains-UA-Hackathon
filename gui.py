from nicegui import ui
from GameManager import GameManager

@ui.page('/')
def init_gui():
    input_fields = []
    with ui.tabs().classes('w-full') as tabs:
        standard = ui.tab("Standard Mode")
        not_standard = ui.tab("Not Standard Mode")
        
    with ui.tab_panels(tabs, value=standard).classes('w-full'):
        with ui.tab_panel(standard).classes("items-center"):
            with ui.row(wrap=False):
                for i in range(5):
                    input_fields.append(ui.input().classes("w-1/5").props("square"))
                    
            textfield = ui.input("enter a word here!").classes("object-center")
            ui.button("Click to submit answer", on_click=lambda: label.set_text("You typed: " + textfield.value))
            label = ui.label()
        with ui.tab_panel(not_standard).classes('w-full'):
            ui.label("woah you found the not standard page").classes('text-emerald-500')
            
    with ui.header(elevated=True):
        ui.markdown("# **Word Chains**")
    with ui.left_drawer(top_corner=True, bottom_corner=True):
        ui.label("left")

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
