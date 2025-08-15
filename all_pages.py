from nicegui import ui
from pages.title_generator import title_generator
from pages.script_generator import script_generator
from pages.example_stuff import example_stuff
from pages.echart_page import page_echart

def create() -> None:
    ui.page('/youtube-title-generator/')(title_generator)
    ui.page('/youtube-script/')(script_generator)
    ui.page('/example/')(example_stuff)
    ui.page('/page_echart/')(page_echart)

if __name__ == '__main__':
    create()