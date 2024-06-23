from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from data import df, countries_list, years_list

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H3("Отели Европы"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

   dbc.Row ([
        dbc.Col([
            html.P("Выберите страну:")
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-cntr',
                options = [{'label': i, 'value': i} for i in countries_list],
                multi = True
            )
        ],width=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div(html.Img(src=r'./static/desc.svg', alt='image', height=20), style={"text-align": "right"})
                ],width=3),
                dbc.Col([
                    daq.ToggleSwitch(
                        label='Сортировка',
                        labelPosition='bottom',
                        id = 'crossfilter-sort'
                    )
                ],width=3),
                dbc.Col([
                    html.Div(html.Img(src=r'./static/asc.svg', alt='image', height=20))
                ],width=3)
            ])
        ],width=2),
        # dbc.Col([
        #     dcc.RadioItems(
        #         options=[
        #             {'label':'+', 'value': 'desc'},
        #             {'label':'-', 'value': 'asc'},
        #         ],
        #         id = 'crossfilter-sort',
        #         value="desc",
        #         inline=True
        #     )
        # ],width=2),
        dbc.Col([
            dcc.Slider(
                id = 'crossfilter-year',
                min = min(years_list),
                max = max(years_list),
                value = max(years_list),
                step = None,
                marks = {str(year):
                str(year) for year in years_list}
            )
        ],width=3)
    ]),

   html.Br(),

   dbc.Container([
    html.Div(id="hotels_table"),
   ])

])

@callback(
    [Output ('hotels_table','children')],
     [Input ('crossfilter-cntr','value'),
      Input ('crossfilter-sort','value'),
      Input ('crossfilter-year','value')]
)
def update_table(countries,sorting,year):
    if countries is None:
        countries = []
    reviews = df[(df["Hotel_Country"].str.contains('|'.join(countries)))&(df["Review_Year"]<=int(year))]
    hotels = reviews.drop_duplicates(subset=["Hotel_Name"])
    for i, row in hotels.iterrows():
        hotels.at[i, "Average_Score"] = round(reviews[(reviews["Hotel_Name"]==row["Hotel_Name"])]["Average_Score"].mean(),2)
    table = dbc.Table.from_dataframe(
        hotels
            .sort_values(by="Average_Score", ascending=sorting)
            [["Hotel_Name", "Average_Score", "Hotel_Address"]],
        striped=True,
        bordered=True,
        hover=True,
        index=False
    )


    return [table]
