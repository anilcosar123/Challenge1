import pandas as pd
from dash import Dash, dcc, html


app1 = Dash(__name__)



app1.layout = html.Div(
    
    #eating
    #slider count page to other page
    
    
    
    
    
    
    #health
    #3 zoomable graphs horizontal text next to it maybe
    
    dcc.graph1(pd.read_csv('BVP.csv'))
              
    
    
    graph2=[pd.read_csv('HR.csv')]
    graph3=[pd.read_csv('IRI.csv')]
)


            figure={
                "data": [
                    {
                        "x": data["Time"],
                        "y": data["BVP"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "BVP/seconds"},
            },