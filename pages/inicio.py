import dash 
from dash import html, dcc
import plotly.express as px
import numpy as np
import pandas as pd
P0 = 100
r = 0.03
t = np.linspace(0, 100, 50)
P = P0 * np.exp(r * t)
df = pd.DataFrame({"Tiempo": t, "Población": P})
dash.register_page(__name__, path="/", name="Inicio")
fig = px.line(
    df, x="Tiempo", y="Población",
    title="Crecimiento Exponencial",
    markers=True,
    line_shape="spline"
)
layout = html.Div(children=[
    html.Div(children=[
        html.H2("Crecimiento Exponencial"),
        dcc.Markdown("""
        Se modela la población con:
        $$P(t) = P_0 e^{rt}$$  
        donde:  
        - $P_0 = 100$ es la población inicial  
        - $r = 0.03$ es la tasa de crecimiento  
        ---
        """, mathjax=True)
    ], className="content"),
    html.Div(children=[
        html.H2("Gráfica", className="title"),
        dcc.Graph(
            id="grafico-crecimiento",
            figure=fig,
            style={"height": "500px"}
        )
    ])
])
