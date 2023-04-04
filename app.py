
from dash import Dash
import plotly.express as px
import pandas as pd 
from dash import Input, Output, State, dcc, html, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from utils import *


text_color ="#a5c0af"
green_background ="rgba(143, 200, 168, 0.1)"

## Coins Images
bitcoin_src = 'assets/images/Bitcoin.png'
cardano_src = 'assets/images/Cardano.png'
dogecoin_src = 'assets/images/Dogecoin.png'
ethereum_src = 'assets/images/Ethereum.png'
litecoin_src = 'assets/images/Litecoin.png'
tron_src = 'assets/images/Tron.png'

"""#Read Data"""
df = read_data('Bitcoin')

"""#DataFrame for pie chart"""
df_all = pd.concat([read_data(coin) for coin in coins ])
pie_df=df_all.drop_duplicates(subset=["Name",'Year'],
                     keep='last')


currency_cards = html.Div([
    generate_currency_card("Bitcoin", bitcoin_src),
    generate_currency_card("Cardano", cardano_src),
    generate_currency_card("Dogecoin", dogecoin_src),
    generate_currency_card("Ethereum", ethereum_src),
    generate_currency_card("Litecoin", litecoin_src),
    generate_currency_card("Tron", tron_src)
    ], style={'textAlign': 'center'}) 
    



"""#Row0"""
Row0 = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Col(
               html.Img(src='assets/images/logo.png',width=150,height=100),
                    width=12)
        ])
    ], width=5),
    dbc.Col([
        dbc.Row([
          currency_cards
        ], align='center')
    ], width=7)
], align='center')

"""## Row1"""
Row1 = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Col(
              dbc.Card(dbc.CardBody([
              html.Div([
                        html.H2(id="coin_title",style={"color":text_color}),
                        html.Img(id="coin_img",width=90, height=100),
                    ], style={'textAlign': 'center'}) 
                ]),style={"background-color":green_background})
                , 
                    width=12)
        ])
    ], width=3),
    dbc.Col([
        dbc.Row([
            dbc.Col(create_graph_card('Market Cap', 'MarketcapBAN'),width=3),
            dbc.Col(create_graph_card('Volume', 'VolumeBAN'),width=3),
            dbc.Col(create_graph_card('High', 'HighBAN'),width=3),
            dbc.Col(create_graph_card('Low', 'LowBAN'),width=3)
        ], align='center')
    ], width=9)
], align='center')

"""#Row buttons"""
Row_buttons = dbc.Row([
    dbc.Col([
        dbc.Row([
            
        ])
    ], width=3),
    dbc.Col([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': str(o), 'value': str(o)} for o in list(df['Year'].unique())+['All']],
                        placeholder="years"
                    )
              ],width=4),
            dbc.Col([dbc.Button("CandleStick", color="secondary", id='CandleStick-Button',style={"margin": "5px"}),
                    dbc.Button("High&Low", color="secondary", id='High&Low-Button',style={"margin": "5px"}),
                    dbc.Button("Open&Close", color="secondary", id='Open&Close-Button',style={"margin": "5px"})
            ],width=8)
        ], align='center')
    ], width=9)
], align='center')

"""# Row 2"""

Row2 = dbc.Row([
    dbc.Col([
        dcc.Graph(id='PieChart')
    ], width=3),

    dbc.Col([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='VarPlot')
                
            ], width=12)
        ], align='center')
    ], width=9),
], align='center')

"""# Row3"""

Row3 = dbc.Row([
    dbc.Col([ 
        dbc.Card(dbc.CardBody([
            html.Div([
                html.H2('Currencies Marketcap',style={"color":text_color}),
                html.Div(id='table-graph')
            ], style={'textAlign': 'center'}) 
        ]),style={"background-color":'rgba(1,1,1,0.7)'})
        #html.Div()
    ] ,width=3),

    dbc.Col([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='MarketcapLinePlot')
            ], width=12),
        ], align='center')               
    ], width=9),
], align='center')

"""# Body"""
def create_layout():
    return html.Div([
                Row0,
                html.Br(),
                Row1,
                html.Br(),
                Row_buttons,
                Row2,
                html.Br(),
                Row3
    ],
        style={"background-image": "url(assets/images/background.jpg)"})


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.prevent_initial_callbacks = 'initial_duplicate'
server = app.server

# Change all plots with year
@app.callback(
    Output('MarketcapBAN', 'figure',allow_duplicate=True),
    Output('VolumeBAN', 'figure',allow_duplicate=True),
    Output('HighBAN', 'figure',allow_duplicate=True),
    Output('LowBAN', 'figure',allow_duplicate=True),
    Output('MarketcapLinePlot','figure',allow_duplicate=True),
    Output('PieChart', 'figure',allow_duplicate=True),
    Output('table-graph', 'children'),
    Input('year-dropdown', 'value')
)
def update_market_cap(year_value):
    # handling year_value
    if year_value == 'All' or year_value is None:
        plt_df = df
        plt_pie = pie_df
    else:
        year_value = int(year_value)
        plt_df = df[df.Year == year_value]
        plt_pie = pie_df[pie_df.Year ==year_value]
    
    
    # return figures
    cols = ['Marketcap','Volume','High','Low']
    return [figure_bigNo([col],plt_df) for col in cols] + [drawLineFigure(plt_df, 'Marketcap', title='Market Capitaliztiion', x_col='Date')] +[drawLPieChart(plt_pie)] +[get_table(year_value,coins)]

# change varPlot (CandleStick, High&Low, Open&Close)
@app.callback(
    Output('VarPlot', 'figure',allow_duplicate=True),
    Output('CandleStick-Button', 'color'),
    Output('High&Low-Button', 'color'),
    Output('Open&Close-Button', 'color'),
    Input('year-dropdown', 'value'),
    Input('CandleStick-Button', 'n_clicks'),
    Input('High&Low-Button', 'n_clicks'),
    Input('Open&Close-Button', 'n_clicks')
)
def update_varPlot(year, *n):
    if year == 'All' or year is None:
        plt_df = df
    else:
        plt_df = df[df.Year == int(year)]
    h=o=c='secondary'
    if "High&Low-Button" == ctx.triggered_id:
        h='success'
        return drawLineFigure(plt_df, ['High','Low'], title='High & Low', x_col='Date'),c,h,o
    elif "Open&Close-Button" == ctx.triggered_id:
        o='success'
        return drawLineFigure(plt_df, ['Open','Close'], title='Open & Close', x_col='Date'),c,h,o
    else:
        c='success'
        return Candlestick(plt_df),c,h,o
# change currency data
@app.callback(
    Output('VarPlot', 'figure',allow_duplicate=True),
    Output('MarketcapBAN', 'figure',allow_duplicate=True),
    Output('VolumeBAN', 'figure',allow_duplicate=True),
    Output('HighBAN', 'figure',allow_duplicate=True),
    Output('LowBAN', 'figure',allow_duplicate=True),
    Output('MarketcapLinePlot','figure',allow_duplicate=True),
    Output('year-dropdown', 'options'),
    Output('coin_title', 'children'),
    Output('coin_img', 'src'),
    Output('Bitcoin_button', 'color'),
    Output('Cardano_button', 'color'),
    Output('Dogecoin_button', 'color'),
    Output('Ethereum_button', 'color'),
    Output('Litecoin_button', 'color'),
    Output('Tron_button', 'color'),
    Input('Bitcoin_button', 'n_clicks'),
    Input('Cardano_button', 'n_clicks'),
    Input('Dogecoin_button', 'n_clicks'),
    Input('Ethereum_button', 'n_clicks'),
    Input('Litecoin_button', 'n_clicks'),
    Input('Tron_button', 'n_clicks'),
)
def update_app(*n):
    global df
    if ctx.triggered_id:
        coin = ctx.triggered_id.split('_')[0]
    else:
        coin = 'Bitcoin'
    figs = list(update_varPlot('All', 5))
    df = read_data(coin, path="datasets/")
    plt_df = df
    colors=["secondary" if c !=coin else "success" for c in coins ]
    cols = ['Marketcap','Volume','High','Low']
    return [Candlestick(plt_df)] + [figure_bigNo([col],plt_df) for col in cols] + [drawLineFigure(plt_df, 'Marketcap', title='Market Capitaliztiion', x_col='Date')] + [[{'label': str(year), 'value': str(year)} for year in list(df['Year'].unique())+['All']]] + [coin,eval(f"{coin.lower()}_src")] +colors
    
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=False)   

