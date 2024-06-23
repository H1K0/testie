from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, nationalities_list

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
            html.Div([
                html.H1("Тепловая карта национальностей посетителей"),
                html.Hr(style={"color": "black"})
            ])
        )
    ]),

    html.Br(),

    dbc.Row ([
        dbc.Col([
            dbc.Label("Выберите национальность:"),
            dcc.Dropdown(
                id = 'crossfilter-natio',
                options = [{'label': i, 'value': i} for i in nationalities_list],
                value=nationalities_list[0],
                multi=False
            )
        ],width=3),

        dbc.Col([
            dcc.Graph(id = 'choropleth', config={"displayModeBar": False}),
        ],width=9)
    ])
])


@callback(
    Output('choropleth', 'figure'),
    Input('crossfilter-natio', 'value')
)
def update_choropleth(nationality):
    data = df[(df["Reviewer_Nationality"]==nationality)].groupby(["Hotel_Country"]).agg({"Hotel_Country": "first", "Total_Number_of_Reviews": "first", "Review_Year": "first"}).sort_values(by="Review_Year")
    figure = px.choropleth(
        data,
        locations='Hotel_Country',
        locationmode = 'country names',
        color='Total_Number_of_Reviews',
        hover_name='Hotel_Country',
        # title='Показатели по странам',
        color_continuous_scale=px.colors.sequential.BuPu,
        animation_frame='Review_Year',
        height=650
    )
   
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        showlegend=False)
    return figure
