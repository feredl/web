import requests
import pandas as pd
import dash
from dash import dash_table as dt
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

#DATAFRAME 
df = pd.read_csv('london_weather.csv')

#APP ENTITIES 
date_selector = dcc.RangeSlider(
    id = 'date_range_slider',
    min = min(df['date']),
    max = max(df['date']),
    marks = {19800101: '1980', 19810101: '1981', 19820101: '1982', 19830101: '1983', 
             19840101: '1984', 19850101: '1985', 19860101: '1986', 19870101: '1987', 19880101: '1988', 19890101: '1989',
             19900101: '1990', 19910101: '1991', 19920101: '1992', 19930101: '1993', 19940101: '1994', 19950101: '1995',
             19960101: '1996', 19970101: '1997', 19980101: '1998', 19990101: '1999', 20000101: '2000', 20010101: '2001',
             20020101: '2002', 20030101: '2003', 20040101: '2004', 20050101: '2005', 20060101: '2006', 20070101: '2007',
             20080101: '2008', 20090101: '2009', 20100101: '2010', 20110101: '2011', 20120101: '2012', 20130101: '2013', 
             20140101: '2014', 20150101: '2015', 20160101: '2016', 20170101: '2017' ,20180101: '2018', 20190101: '2019'
    },
    step = 365,
    value = [19790102, 20201230]
)

#APP INIT
app = dash.Dash(__name__)

#APP LAYOUT
app.layout = html.Div([
    html.H1('London Weather'),
    html.Div(date_selector),
    dcc.Graph(id = 'temp_snow_chart'), 
    dcc.Graph(id = 'pressure_snow_chart'), 
    dcc.Graph(id = 'sunshine_snow_chart'), 
    dcc.Graph(id = 'precipitation_snow_chart'), 
    dcc.Graph(id = 'global_radiation_snow_chart'), 
    dcc.Graph(id = 'cloud_snow_chart'), 
    ])

#CALLBACKS
@app.callback(
    Output(component_id = 'temp_snow_chart', component_property = 'figure'),
    Output(component_id = 'pressure_snow_chart', component_property = 'figure'),
    Output(component_id = 'sunshine_snow_chart', component_property = 'figure'),
    Output(component_id = 'precipitation_snow_chart', component_property = 'figure'),
    Output(component_id = 'global_radiation_snow_chart', component_property = 'figure'),
    Output(component_id = 'cloud_snow_chart', component_property = 'figure'),
    Input(component_id = 'date_range_slider', component_property = 'value'), 
) 
def update_chart(date_range):
    chart_data = df[(df['date'] > date_range[0]) &
                    (df['date'] < date_range[1])
    ]
    fig = px.scatter(chart_data, x = 'min_temp', y = 'snow_depth')
    fig1 = px.scatter(chart_data, x = 'pressure', y = 'snow_depth')
    fig2 = px.scatter(chart_data, x = 'sunshine', y = 'snow_depth')
    fig3 = px.scatter(chart_data, x = 'precipitation', y = 'snow_depth')
    fig4 = px.scatter(chart_data, x = 'global_radiation', y = 'snow_depth')
    fig5 = px.scatter(chart_data, x = 'cloud_cover', y = 'snow_depth')

    return fig, fig1, fig2, fig3, fig4, fig5


if __name__ == '__main__':
    app.run_server(debug = True)
