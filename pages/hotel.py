from dash import html, dcc, callback, Output, Input
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from googletrans import Translator

from data import df, nationalities_list, hotels_list, years_list

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label('Отель'),
            dcc.Dropdown(
                id = 'crossfilter-hotel',
                options = [{'label': i, 'value': i} for i in hotels_list],
                value=hotels_list[0],
                multi=False
            ),
            html.Label('Национальность рецензентов', style={'margin-top': '25px'}),
            dcc.Dropdown(
                id = 'crossfilter-natio',
                options = [{'label': i, 'value': i} for i in nationalities_list],
                multi=True
            )
        ],width=4),
        dbc.Col([
            dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Средний рейтинг за все время")
                    ]),
                    dbc.Row([
                        dbc.CardBody(
                            html.P(
                            id='card-average-total',
                            className="card-value"),
                            style={'font-size':32},
                        )
                    ])
            ], color = "info", outline=True, style={'textAlign': 'center', 'height': '180px', 'overflow': 'hidden'}),
        ],width=4),
        dbc.Col([
            html.Div(id='card-average-year')
        ],width=4),
    ]),
    html.Label('Адрес отеля'),
    dbc.Input(
        id="hotel-address",
        type="text",
        disabled=True
    ),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Положительный отзыв")
                    ]),
                    dbc.Row([
                        dbc.CardBody(
                            html.P(
                            id='card-pos-review',
                            className="card-value"),
                            style={'font-size':14},
                        )
                    ])
            ], color = "success", outline=True, style={'textAlign': 'center', 'overflow': 'hidden'}),
        ],width=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div(html.Img(src=r'./static/translate-off.svg', alt='image', height=20), style={"text-align": "right"})
                ],width=4),
                dbc.Col([
                    daq.ToggleSwitch(
                        label='Перевод',
                        labelPosition='bottom',
                        id = 'translate-toggle'
                    )
                ],width=4),
                dbc.Col([
                    html.Div(html.Img(src=r'./static/translate-on.svg', alt='image', height=20))
                ],width=4)
            ])
        ],width=2),
        dbc.Col([
            dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Отрицательный отзыв")
                    ]),
                    dbc.Row([
                        dbc.CardBody(
                            html.P(
                            id='card-neg-review',
                            className="card-value"),
                            style={'font-size':14},
                        )
                    ])
            ], color = "danger", outline=True, style={'textAlign': 'center', 'overflow': 'hidden'}),
        ],width=5)
    ], style={'margin': '20px 0 0'}),

    dcc.Graph(id='graph-dynamics')

], fluid=True)

tltr = Translator()

@callback(
    [Output('hotel-address', 'value'),
     Output('card-average-total', 'children'),
     Output('card-average-year', 'children'),
     Output('card-pos-review', 'children'),
     Output('card-neg-review', 'children'),
     Output('graph-dynamics', 'figure')],
    [Input('crossfilter-hotel', 'value'),
    Input('crossfilter-natio', 'value'),
    Input('translate-toggle', 'value')]
)
def update_page(hotel,nationalities,translate_on):
    if not nationalities:
        nationalities = []
    hotel_data = df[(df["Hotel_Name"]==hotel)&(df["Reviewer_Nationality"].str.contains('|'.join(nationalities)))]
    hotel_data.reset_index(inplace=True)
    this_year = hotel_data[(hotel_data["Review_Year"]==years_list[-1])]
    prev_year = hotel_data[(hotel_data["Review_Year"]==years_list[-2])]

    avg_tot = round(hotel_data["Reviewer_Score"].mean(),3)
    avg_ty = this_year["Reviewer_Score"].mean()
    avg_py = prev_year["Reviewer_Score"].mean()

    delta = go.Figure()
    delta.add_trace(go.Indicator(mode="number+delta", value=avg_ty, number={'valueformat':".1f","font":{"size":32}}, delta={'reference':avg_py,'relative':True, 'position':"bottom", 'valueformat':".0%","font":{"size":20}}))
    delta.update_layout(autosize=True, height=80, margin={'t':0,'b':0})
    diff = dbc.Card([
    dbc.Row([
        dbc.CardHeader("Средний рейтинг за год"),    
    ]),
    dbc.Row([
        html.Div([
            dcc.Graph(figure=delta),
            html.I(' в % к прошлому году'),
        ])
    ],)
    ], color='info', outline=True, style={'textAlign': 'center', 'height': '180px', 'overflow': 'hidden'})

    # figure = px.bar(
    #     hotel_data.groupby(["Review_Month"]).agg({"Reviewer_Score": "mean", "Review_Month": "first", "Reviewer_Nationality": "first"}),
    #     x = "Review_Month",
    #     y = "Reviewer_Score",
    #     color = "Reviewer_Nationality",
    #     title = "Статистика оценок"
    # )

    figure = px.scatter(
        hotel_data.groupby(["Review_Month"]).agg({"Reviewer_Score": "mean", "Review_Month": "first", "Reviewer_Nationality": "first", "Review_Weighted_Score": "count"}),
        x="Review_Month",
        y="Reviewer_Score",
        size="Review_Weighted_Score",
        color="Reviewer_Nationality",
        hover_name="Reviewer_Nationality",
        size_max=60
    )

    if hotel_data.empty:
        pos_rev = "No Positive"
        neg_rev = "No Negative"
    else:
        pos_rev = str(hotel_data.iloc[hotel_data["Review_Weighted_Score"].idxmax()]["Positive_Review"])
        neg_rev = str(hotel_data.iloc[hotel_data["Review_Weighted_Score"].idxmin()]["Negative_Review"])
        if translate_on:
            pos_rev = tltr.translate(pos_rev, dest='ru').text
            neg_rev = tltr.translate(neg_rev, dest='ru').text

    return hotel_data["Hotel_Address"][0],avg_tot,diff,pos_rev,neg_rev,figure
