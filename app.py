import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from sqlalchemy import create_engine

app.title = "Purwadhika Dash Plotly"

conn = create_engine("mysql+mysqlconnector://root:gempelo10@localhost/ujiantitanic?host=localhost?port=3306")

def fetch_data(q):
    result = pd.read_sql(
        sql=q,
        con=conn
    )
    return result

def get_titanic():

    titanic_query = (
        f'''
        SELECT * 
        FROM titanic
        '''
    )
    titanic = fetch_data(titanic_query)
    titanic = list(titanic['titanic'])
    return titanic

app.layout = html.Div(
    children=[
        dcc.Tabs(id='tabs', value='tab-1',
            style={
                'fontFamily' : 'system-ui'
            },
            content_style={
                'fontFamily' : 'Arial',
                'borderLeft' : '1px solid #d6d6d6',
                'borderRight' : '1px solid #d6d6d6',
                'borderBottom' : '1px solid #d6d6d6',
                'padding' : '44px'
            },
            children=[ #value buat tampilan default tab yg mau diliatin
                dcc.Tab(label='Tips DataSet', value='tab-1', children=[
                    html.Div([
                        html.H1(
                            children='Tips Dataset',
                            className='h1FirstTab'
                        ),
                        html.Table([
                            html.Tr([
                                html.Td([
                                    html.P('Jenis Plot : '),
                                    dcc.Dropdown(
                                        id='ddl-jenis-categorical-plot',
                                        options=[{'label': 'Bar'   , 'value': 'bar'},
                                                 {'label': 'Violin', 'value': 'violin'},
                                                 {'label': 'Box'   , 'value': 'box'}],
                                        value='bar'
                                    )
                                ]),
                                html.Td([
                                    html.P('X Axis : '),
                                    dcc.Dropdown(
                                        id='ddl-x-categorical-plot',
                                        options=[{'label': 'Survived', 'value': 'survived'},
                                                 {'label': 'Sex'   , 'value': 'sex'},
                                                 {'label': 'Ticket Class'   , 'value': 'class'},
                                                 {'label': 'Embark Town'  , 'value': 'embark_town'},
                                                 {'label': 'Who'   , 'value': 'who'},
                                                 {'label': 'Outlier'   , 'value': 'outlier'}],
                                        value='survived'
                                    )
                                ])
                            ])
                        ],
                            style={'width':'900px','margin':'0 auto'}
                        ), 
                        html.Div( id='divTableSlider', children=
                        []
                        )
                    ])
                ]),
                dcc.Tab(label='Categorical Plot', value='tab-3', children=[
                    html.Div([
                        html.H1(
                            children='Categorical Plot',
                            className='h1FirstTab'
                        ),
                        html.Table([
                            html.Tr([
                                html.Td([
                                    html.P('Jenis Plot : '),
                                    dcc.Dropdown(
                                        id='ddl-jenis-categorical-plot',
                                        options=[{'label': 'Bar'   , 'value': 'bar'},
                                                 {'label': 'Violin', 'value': 'violin'},
                                                 {'label': 'Box'   , 'value': 'box'}],
                                        value='bar'
                                    )
                                ]),
                                html.Td([
                                    html.P('X Axis : '),
                                    dcc.Dropdown(
                                        id='ddl-x-categorical-plot',
                                        options=[{'label': 'Smoker', 'value': 'smoker'},
                                                 {'label': 'Sex'   , 'value': 'sex'},
                                                 {'label': 'Day'   , 'value': 'day'},
                                                 {'label': 'Time'  , 'value': 'time'}],
                                        value='smoker'
                                    )
                                ]),
                                html.Td([
                                    html.P('Text : '),
                                    dcc.Dropdown(
                                        id='ddl-text-categorical-plot',
                                        options=[{'label': 'Smoker', 'value': 'smoker'},
                                                 {'label': 'Sex'   , 'value': 'sex'},
                                                 {'label': 'Day'   , 'value': 'day'},
                                                 {'label': 'Time'  , 'value': 'time'},
                                                 {'label': 'Size'  , 'value': 'size'}],
                                        value='smoker'
                                    )
                                ])
                            ])
                        ],
                            style={'width':'900px','margin':'0 auto'}
                        ), 
                        generate_bar()
                    ])
                ])
            ])
    ],
style={
    'maxWidth' : '1000px',
    'margin' : '0 auto',
}
)


@app.callback(
    Output('divTableSlider','children'),
    [
        Input('range-slider-total-bill','value')
    ]
)
def update_table_dataset(slider):
    dfT=dfTips[dfTips['total_bill'].between(slider[0],slider[1])]
    return [
        html.H4(f'Min : {slider[0]} Max : {slider[1]}'),
        html.H4(f'Total Row : {len(dfT)}'),
        dcc.Graph(
            id='table-data',
            figure={
                'data' : [
                    go.Table(
                        header=dict(values=['<b>'+ col +'</b>' for col in dfT.columns],
                                    fill=dict(color='#C2D4FF'),
                                    font=dict(size=15),
                                    height=30 ),
                        cells=dict(values=[dfT[col] for col in dfT.columns]
                                    , fill=dict(color='#F5F8FF')
                                    , align= ['right']
                                    , font=dict(size=15)
                                    , height=30 
                                    )
                    )
                ],
                'layout' : go.Layout(
                    height=500, 
                    margin={'l':40, 'b':40, 't':10, 'r':10}
                    )
            }
        )
    ]

@app.callback(
    Output('categoricalPlot','figure'),
    [
        Input('ddl-jenis-categorical-plot','value'),
        Input('ddl-x-categorical-plot','value'),
        Input('ddl-text-categorical-plot','value')
    ]
)
def update_category_graph(ddljenis,ddlx,ddltext):
    return {
        'data' : getPlot(ddljenis,ddlx,ddltext),
        'layout' : go.Layout(
                xaxis={'title':ddlx.title()}, yaxis={'title':'US$'},
                margin={'l':40, 'b':40, 't':10, 'r':10},
                legend={'x':0, 'y':1.2}, hovermode='closest',
                boxmode='group', violinmode='group'
                # , plot_bgcolor='black'
                # , paper_bgcolor='black'
                )
    }