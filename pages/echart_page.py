from nicegui import ui
import theme

@ui.page('/')
def page_echart():
    with theme.frame('Example Items'):
      ui.page_title('Example Echart')
      echart = ui.echart({
        'xAxis': {'type': 'category', 'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [150, 230, 224, 218, 135]}],
      })

      ui.button('Show Loading', on_click=lambda: echart.run_chart_method('showLoading'))
      ui.button('Hide Loading', on_click=lambda: echart.run_chart_method('hideLoading'))

      async def get_width():
        width = await echart.run_chart_method('getWidth')
        ui.notify(f'Width: {width}')
      ui.button('Get Width', on_click=get_width)
      ui.button('Set Tooltip', on_click=lambda: echart.run_chart_method(
        ':setOption', r'{tooltip: {formatter: params => "$" + params.value}}',
    ))