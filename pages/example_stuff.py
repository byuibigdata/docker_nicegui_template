# %%
import httpx
import random
import theme
import polars as pl

from uuid import uuid4
from pathlib import Path
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.options import AxisOpts
from nicegui import events, ui, app

def example_stuff():
    with theme.frame('Example Items'):
        ui.page_title('Example Items')
        ui.markdown('# This is a test')


        # %%
        # Step 1: Create a pyobsplot chart and export it as HTML
        data = pl.DataFrame(
            {
                "x": [1, 5, 2, 4, 6, 2, 4],
                "y": [2, 1, 3, 4, 5, 1, 2],
                "type": ["T1", "T2", "T1", "T2", "T1", "T1", "T2"],
            }
        )

        ui.echart({
            'xAxis': {'type': 'category'},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [20, 10, 30, 50, 40, 30]}],
        }, on_point_click=ui.notify)

        echart = ui.echart({
            'xAxis': {'type': 'value'},
            'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
            'legend': {'textStyle': {'color': 'gray'}},
            'series': [
                {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
                {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
            ],
        })

        def update():
            echart.options['series'][0]['data'][0] = random()
            echart.update()

        ui.button('Update', on_click=update)



        # %%

        ui.button('Change page title', on_click=lambda: ui.page_title('New Title'))

        # Step 3: Serve it in NiceGUI


        # https://thelinuxcode.com/plotly-io-json/
        fig = {
            'data': [
                {
                    'type': 'scatter',
                    'name': 'Trace 1',
                    'x': [1, 2, 3, 4],
                    'y': [1, 2, 3, 2.5],
                },
                {
                    'type': 'scatter',
                    'name': 'Trace 2',
                    'x': [1, 2, 3, 4],
                    'y': [1.4, 1.8, 3.8, 3.2],
                    'line': {'dash': 'dot', 'width': 3},
                },
            ],
            'layout': {
                'margin': {'l': 15, 'r': 0, 't': 0, 'b': 15},
                'plot_bgcolor': '#E5ECF6',
                'xaxis': {'gridcolor': 'white'},
                'yaxis': {'gridcolor': 'white'},
            },
        }


        ui.plotly(fig).classes('w-full h-40')

        ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
        result = ui.label()

        ui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))
        result = ui.label()

        df = pl.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        ui.aggrid.from_polars(df).classes('max-h-40')

        ui.table.from_polars(df).classes('max-h-40')

        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')

        min_max_range = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
        ui.label().bind_text_from(min_max_range, 'value',
                                  backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

        editor = ui.codemirror('print("Edit me!")', language='Python').classes('h-32')
        ui.select(editor.supported_languages, label='Language', clearable=True) \
            .classes('w-32').bind_value(editor, 'language')
        ui.select(editor.supported_themes, label='Theme') \
            .classes('w-32').bind_value(editor, 'theme')



        toggle1 = ui.toggle([1, 2, 3], value=1)
        toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')

        radio1 = ui.radio([1, 2, 3], value=1).props('inline')
        radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')

        ui.input_chips('My favorite chips', value=['Pringles', 'Doritos', "Lay's"])


        with ui.row().classes('gap-1'):
            ui.chip('Click me', icon='ads_click', on_click=lambda: ui.notify('Clicked'))
            ui.chip('Selectable', selectable=True, icon='bookmark', color='orange')
            ui.chip('Removable', removable=True, icon='label', color='indigo-3')
            ui.chip('Styled', icon='star', color='green').props('outline square')
            ui.chip('Disabled', icon='block', color='red').set_enabled(False)


        with ui.fab('navigation', label='Transport'):
            ui.fab_action('train', on_click=lambda: ui.notify('Train'))
            ui.fab_action('sailing', on_click=lambda: ui.notify('Boat'))
            ui.fab_action('rocket', on_click=lambda: ui.notify('Rocket'))

        ui.markdown('This is **Markdown**.')

        ui.markdown('''
            ## Example

            This line is not indented.

                This block is indented.
                Thus it is rendered as source code.

            This is normal text again.
        ''')


        ui.button.default_props('rounded outline')
        ui.button('Button A')
        ui.button('Button B')

        with ui.card() as a:
            ui.label('A')
            x = ui.label('X')

        with ui.card() as b:
            ui.label('B')

        ui.button('Move X to A', on_click=lambda: x.move(a))
        ui.button('Move X to B', on_click=lambda: x.move(b))
        ui.button('Move X to top', on_click=lambda: x.move(target_index=0))


        navigation = ui.row()
        ui.link_target('target_A')
        ui.label(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
            'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        )
        label_B = ui.label(
            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip         ex ea commodo consequat. '
            'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu        fugiat nulla pariatur. '
            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt         mollit anim id est laborum.'
        )
        with navigation:
            ui.link('Goto A', '#target_A')
            ui.link('Goto B', label_B)

        @app.get('/random/{max}')
        def generate_random_number(max: int):
            return {'min': 0, 'max': max, 'value': random.randint(0, max)}

        max = ui.number('max', value=100)
        ui.button('generate random number',
                  on_click=lambda: ui.navigate.to(f'/random/{max.value:.0f}'))

        media = Path('media')
        media.mkdir(exist_ok=True)
        r = httpx.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')
        (media  / 'clouds.mp4').write_bytes(r.content)
        app.add_media_files('/my_videos', media)
        ui.video('/my_videos/clouds.mp4')

        with ui.row():
            ui.button('Back', on_click=ui.navigate.back)
            ui.button('Forward', on_click=ui.navigate.forward)
            ui.button('Reload', on_click=ui.navigate.reload)
            ui.button(icon='savings',
                      on_click=lambda: ui.navigate.to('https://github.com/sponsors/zauberzeug'))

        app.add_static_files('/data', 'data')
        ui.label('Some NiceGUI Examples').classes('text-h5')
        ui.link('AI interface', '/examples/ai_interface/main.py')
        ui.link('Custom FastAPI app', '/examples/fastapi/main.py')
        ui.link('Authentication', '/examples/authentication/main.py')


        @ui.page('/icon/{icon}')
        def icons(icon: str, amount: int = 1):
            ui.label(icon).classes('text-h3')
            with ui.row():
                [ui.icon(icon).classes('text-h3') for _ in range(amount)]
        ui.link('Star', '/icon/star?amount=5')
        ui.link('Home', '/icon/home')
        ui.link('Water', '/icon/water_drop?amount=3')

        @ui.page('/other_page')
        def other_page():
            ui.label('Welcome to the other side')

        @ui.page('/dark_page', dark=True)
        def dark_page():
            ui.label('Welcome to the dark side')

        ui.link('Visit other page', other_page)
        ui.link('Visit dark page', dark_page)


        ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
        ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
        ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')


        @ui.page('/page_layout')
        def page_layout():
            ui.label('CONTENT')
            [ui.label(f'Line {i}') for i in range(100)]
            with ui.header(elevated=True).style('background-color: #3874c8').classes        ('items-center justify-between'):
                ui.label('HEADER')
                ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat        color=white')
            with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color:         #d7e3f4'):
                ui.label('LEFT DRAWER')
            with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props        ('bordered') as right_drawer:
                ui.label('RIGHT DRAWER')
            with ui.footer().style('background-color: #3874c8'):
                ui.label('FOOTER')

        ui.link('show page with fancy layout', page_layout)

        def mouse_handler(e: events.MouseEventArguments):
            color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
            ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="       {color}" stroke-width="4" />'
            ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

        src = 'https://picsum.photos/id/565/640/360'
        ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'],         cross=True)

        ui.interactive_image(
            size=(800, 600), cross=True,
            on_mouse=lambda e: e.sender.set_content(f'''
                <circle cx="{e.image_x}" cy="{e.image_y}" r="50" fill="orange" />
            '''),
        ).classes('w-64 bg-blue-50')

        ui.label('Hello NiceGUI!')

        editor = ui.editor(placeholder='Type something here')
        ui.markdown().bind_content_from(editor, 'value',
                                        backward=lambda v: f'HTML code:\n```\n{v}\n```')

        json = {
            'array': [1, 2, 3],
            'boolean': True,
            'color': '#82b92c',
            None: None,
            'number': 123,
            'object': {
                'a': 'b',
                'c': 'd',
            },
            'time': 1575599819000,
            'string': 'Hello World',
        }
        ui.json_editor({'content': {'json': json}},
                       on_select=lambda e: ui.notify(f'Select: {e}'),
                       on_change=lambda e: ui.notify(f'Change: {e}'))


        m = ui.leaflet(center=(51.505, -0.09))
        ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center        [1]:.3f}')
        ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

        with ui.grid(columns=2):
            ui.button('London', on_click=lambda: m.set_center((51.505, -0.090)))
            ui.button('Berlin', on_click=lambda: m.set_center((52.520, 13.405)))
            ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
            ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))

        ui.tree([
            {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
            {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
        ], label_key='id', on_select=lambda e: ui.notify(e.value))


        with ui.row().classes('w-full items-center'):
            result = ui.label().classes('mr-auto')
            with ui.button(icon='menu'):
                with ui.menu() as menu:
                    ui.menu_item('Menu item 1', lambda: result.set_text('Selected item 1'))
                    ui.menu_item('Menu item 2', lambda: result.set_text('Selected item 2'))
                    ui.menu_item('Menu item 3 (keep open)',
                                 lambda: result.set_text('Selected item 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Close', menu.close)

        with ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):
            with ui.carousel_slide().classes('p-0'):
                ui.image('https://picsum.photos/id/30/270/180').classes('w-[270px]')
            with ui.carousel_slide().classes('p-0'):
                ui.image('https://picsum.photos/id/31/270/180').classes('w-[270px]')
            with ui.carousel_slide().classes('p-0'):
                ui.image('https://picsum.photos/id/32/270/180').classes('w-[270px]')


        with ui.stepper().props('vertical').classes('w-full') as stepper:
            with ui.step('Preheat'):
                ui.label('Preheat the oven to 350 degrees')
                with ui.stepper_navigation():
                    ui.button('Next', on_click=stepper.next)
            with ui.step('Ingredients'):
                ui.label('Mix the ingredients')
                with ui.stepper_navigation():
                    ui.button('Next', on_click=stepper.next)
                    ui.button('Back', on_click=stepper.previous).props('flat')
            with ui.step('Bake'):
                ui.label('Bake for 20 minutes')
                with ui.stepper_navigation():
                    ui.button('Done', on_click=lambda: ui.notify('Yay!', type='positive'))
                    ui.button('Back', on_click=stepper.previous).props('flat')

        with ui.button(icon='thumb_up'):
            ui.tooltip('I like this').classes('bg-green')


        with ui.timeline(side='right'):
            ui.timeline_entry('Rodja and Falko start working on NiceGUI.',
                              title='Initial commit',
                              subtitle='May 07, 2021')
            ui.timeline_entry('The first PyPI package is released.',
                              title='Release of 0.1',
                              subtitle='May 14, 2021')
            ui.timeline_entry('Large parts are rewritten to remove JustPy '
                              'and to upgrade to Vue 3 and Quasar 2.',
                              title='Release of 1.0',
                              subtitle='December 15, 2022',
                              icon='rocket')

        with ui.card():
            ui.label('Card content')
            ui.button('Add label', on_click=lambda: ui.label('Click!'))
            ui.timer(1.0, lambda: ui.label('Tick!'), once=True)

        with ui.card().tight():
            ui.image('https://picsum.photos/id/684/640/360')
            with ui.card_section():
                ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')

        with ui.list().props('bordered separator'):
            with ui.slide_item('Slide me left or right') as slide_item_1:
                slide_item_1.left('Left', color='green')
                slide_item_1.right('Right', color='red')
            with ui.slide_item('Slide me up or down') as slide_item_2:
                slide_item_2.top('Top', color='blue')
                slide_item_2.bottom('Bottom', color='purple')

        slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
        ui.linear_progress().bind_value_from(slider, 'value')


        fullscreen = ui.fullscreen()

        ui.button('Enter Fullscreen', on_click=fullscreen.enter)
        ui.button('Exit Fullscreen', on_click=fullscreen.exit)
        ui.button('Toggle Fullscreen', on_click=fullscreen.toggle)

        markdown = ui.markdown('Enter your **name**!')

        def inject_input():
            with ui.teleport(f'#{markdown.html_id} strong'):
                ui.input('name').classes('inline-flex').props('dense outlined')

        ui.button('inject input', on_click=inject_input)

        with ui.expansion('Expand!', icon='work').classes('w-full'):
            ui.label('inside the expansion')

        with ui.row():
            with ui.scroll_area().classes('w-32 h-32 border'):
                ui.label('I scroll. ' * 20)
            with ui.column().classes('p-4 w-32 h-32 border'):
                ui.label('I will not scroll. ' * 10)

        ui.label('text above')
        ui.separator()
        ui.label('text below')

        with ui.splitter() as splitter:
            with splitter.before:
                ui.label('This is some content on the left hand side.').classes('mr-2')
            with splitter.after:
                ui.label('This is some content on the right hand side.').classes('ml-2')


        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('One')
            two = ui.tab('Two')
        with ui.tab_panels(tabs, value=two).classes('w-full'):
            with ui.tab_panel(one):
                ui.label('First tab')
            with ui.tab_panel(two):
                ui.label('Second tab')

        
        # %%
