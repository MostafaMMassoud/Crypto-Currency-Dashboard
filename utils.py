from dash import Dash
import plotly.express as px
import pandas as pd 
from dash import Input, Output, State, dcc, html, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

coins=["Bitcoin","Cardano","Dogecoin","Ethereum","Litecoin","Tron"]
text_color ="#a5c0af"
green_background ="rgba(143, 200, 168, 0.1)"

import pandas as pd 
def read_data(coin, path="datasets/"):
    df = pd.read_csv(path+ f"coin_{coin}.csv", parse_dates=["Date"])
    df['Year'] = df['Date'].dt.year
    return df
	


def generate_currency_card(currency_name, currency_src):
    return dbc.Button(id=f"{currency_name}_button", 
						children=[currency_name, html.Img(src=currency_src, width=40, height=40)],
						style={"margin": "5px", 'border': 'solid', 'borderWidth': '0px','width':"100"})
						

# Dash Components						
def create_graph_card(title, graph_id):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(title,className="card-title",style={"color":text_color}),
                    dcc.Graph(id=graph_id)
                ], style={'textAlign': 'center'}) 
            ])
        ,style={'background-color': green_background}),
    ])
	
def get_table(year,coins=coins):
    if year == 'All' or year is None:
        return dbc.Table.from_dataframe(pd.DataFrame([df.iloc[-1][['Name',"Year",'Marketcap']] for df in [read_data(coin) for coin in coins]]), striped=False, bordered=True, hover=False,size="sm", style={'color':text_color,'border-color':'rgb(61, 71, 89)'})
    else:
        return dbc.Table.from_dataframe(pd.DataFrame([df[df.Year==year].iloc[-1][['Name',"Year",'Marketcap']] for df in [read_data(coin) for coin in coins] if year in df.Year.unique()]), striped=False, bordered=True, hover=False, size="sm",style={'color':text_color,'border-color':'rgb(61, 71, 89)'})


# Figures
def figure_bigNo(col,df):
    return go.Figure(go.Indicator(
                mode = "number+delta",
                value = round(float(df.iloc[-1][col]),2),
                number = {'prefix': "$","font":{"size":40} , 'font_color':'rgb(85, 114, 170)'},
                delta = {'position': "top", 'reference': round(float(df.iloc[-2][col]),2)},
                domain = {'x': [0, 1], 'y': [0, 1]},
                ),layout=go.Layout(height=100,width=210, paper_bgcolor= 'rgba(1, 1, 1, 0)', plot_bgcolor= 'rgba(1, 1, 1, 0)')
                )
				
 
def drawLineFigure(df, y_col, title='Line Plot', x_col='Date'):
    return px.scatter(df, x=x_col, y=y_col,title=title,trendline='ols').update_layout(
                template='plotly_dark',
                plot_bgcolor= 'rgba(1, 1, 1, 0.8)',
                paper_bgcolor= 'rgba(1, 1, 1, 0.8)',
                title =  dict(text =title,
                               font =dict(family='Sherif',
                               size=25,
                               color = text_color)),
                               title_x=0.5
            ).update_traces(mode = 'lines')
			
def drawLPieChart(df):
    return  go.Figure(data=[go.Pie(labels=df['Name'], values=df['Marketcap'], textinfo='label+percent',
                             insidetextorientation='radial'
                            )]).update_layout(
                template='plotly_dark',
                plot_bgcolor= 'rgba(1, 1, 1, 0.8)',
                paper_bgcolor= 'rgba(1, 1, 1, 0.8)',
                title =  dict(text ="Market Capitaliztiion",
                               font =dict(family='Sherif',
                               size=25,
                               color = text_color)),
                               title_x=0.5,
                               title_y=0.1
            )
			
def Candlestick(df):
    return go.Figure(data=[go.Candlestick(
          x=df['Date'],
          open=df['Open'],
          high=df['High'],
          low=df['Low'],
          close=df['Close'])]).update_layout(
                  template='plotly_dark',
                  plot_bgcolor= 'rgba(1, 1, 1, 0.8)',
                  paper_bgcolor= 'rgba(1, 1, 1, 0.8)',
                  xaxis_rangeslider_visible=False,
                  title =  dict(text ="Candlestick",
                               font =dict(family='Sherif',
                               size=25,
                               color = text_color)),
                               title_x=0.5,
                              yaxis_title="value",
                               xaxis_title="Date",
              )
