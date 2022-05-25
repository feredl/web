import pandas as pd
import dash
from dash import dash_table as dt
import plotly.express as px
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

#DATAFRAME 
df = pd.read_csv('london_weather.csv')

#APP ENTITIES 
date_selector = dcc.RangeSlider(
    id = 'date_range_slider',
    min = min(df['date']),
    max = max(df['date']),
    marks = {19800101: '1980', 19810101: '', 19820101: '', 19830101: '', 
             19840101: '', 19850101: '1985', 19860101: '', 19870101: '', 19880101: '', 19890101: '',
             19900101: '1990', 19910101: '', 19920101: '', 19930101: '', 19940101: '', 19950101: '1995',
             19960101: '', 19970101: '', 19980101: '', 19990101: '', 20000101: '2000', 20010101: '',
             20020101: '', 20030101: '', 20040101: '', 20050101: '2005', 20060101: '', 20070101: '',
             20080101: '', 20090101: '', 20100101: '2010', 20110101: '', 20120101: '', 20130101: '', 
             20140101: '', 20150101: '2015', 20160101: '', 20170101: '' ,20180101: '', 20190101: '2019'
    },
    step = 365,
    value = [19790102, 20201230]
)

#APP INIT
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

#APP LAYOUT
app.layout = html.Div([
    dbc.Row([
        dbc.Col(),
        dbc.Col(html.Div([html.H1('SNOW DEPTH')], style={'margin-top': '30px', 'margin-bottom': '30px'})),
        dbc.Col(),
    ]), 
    dbc.Row(
        dbc.Col(
            dbc.Tabs([
                dcc.Tab(label = 'DATA', children = [
                    dbc.Row([
                        html.Div(style={'margin-top': '15px', 'margin-bottom': '15px'}),
                        dcc.Markdown(''' ##### Instruments for analyzing influence of different weather factors on snow depth level. Based on data on London weather years 1979-2020.'''),
                        html.Div(style={'margin-top': '15px', 'margin-bottom': '15px'}),
                        dcc.Markdown(''' Choose the time span: '''),
                        html.Div(date_selector),
                        html.Div(style={'margin-top': '30px', 'margin-bottom': '30px'}),
                    ]), 
                    dbc.Row([
                        dbc.Col([
                            html.Div(style={'margin-top': '55px'}),
                            dcc.Markdown(''' Choose the second weather specification: '''),
                            dcc.Dropdown(['temperature', 'sunshine', 'pressure', 'global radiation', 'precipitation', 'cloud cover'], 'min_temp', id='graph_dd')
                        ]), 
                        dbc.Col(dcc.Graph(id = 'snow_chart'), width=8),
                    ])
                ]), 
                dcc.Tab(label = 'CREDITS', children = [
                    html.Div(style={'margin-top': '30px'}),
                    dcc.Markdown(''' ### Dataset: '''), 
                    dcc.Markdown(''' https://www.kaggle.com/datasets/emmanuelfwerr/london-weather-data ''')
                ]),
            ]),
        ), 
    ), 
], 
style={'margin-left': '80px', 'margin-right': '80px'}
)

#CALLBACKS
@app.callback(
    Output(component_id = 'snow_chart', component_property = 'figure'),
    Input(component_id = 'date_range_slider', component_property = 'value'), 
    Input(component_id = 'graph_dd', component_property = 'value')
) 
def update_chart(date_range, dd):
    chart_data = df[(df['date'] > date_range[0]) &
                    (df['date'] < date_range[1])
    ]
    if dd == 'temperature':
        fig = px.scatter(chart_data, x = 'min_temp', y = 'snow_depth')
    elif dd == 'global radiation':
        fig = px.scatter(chart_data, x = 'global_radiation', y = 'snow_depth')
    elif dd == 'cloud cover':
        fig = px.scatter(chart_data, x = 'cloud_cover', y = 'snow_depth')
    else:
        fig = px.scatter(chart_data, x = dd, y = 'snow_depth')

    return fig


if __name__ == '__main__':
    app.run_server(debug = True)
