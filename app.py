from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from pages import overview, hotel, countries


external_stylesheets = [dbc.themes.ZEPHYR]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#76999b", # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.H2("Отзывы об отелях Европы", className="display-6"),
        html.Hr(),
        html.P(
            "Учебный проект Владислава Аршинова и Даниила Савина", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Все отели", href="/", active="exact"),
                dbc.NavLink("Сводка об отеле", href="/page-1", active="exact"),
                dbc.NavLink("Карта", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return overview.layout
    elif pathname == "/page-1":
        return hotel.layout
    elif pathname == "/page-2":
        return countries.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404. Мы изменим её в следующей практической.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == '__main__':
    app.run_server(debug=True)
