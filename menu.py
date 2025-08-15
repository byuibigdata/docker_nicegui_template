from nicegui import ui

def menu() -> None:
    ui.link('Home', '/').classes(replace='text-black')
    ui.link('YouTube Titles', '/youtube-title-generator/').classes(replace='text-black')
    ui.link('YouTube Script Generator', '/youtube-script/').classes(replace='text-black')
    ui.link('Examples', '/example/').classes(replace='text-black')
    ui.link('Interactive Echart', '/page_echart/').classes(replace='text-black')