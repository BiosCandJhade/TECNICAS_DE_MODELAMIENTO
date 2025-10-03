import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
dash.register_page(__name__, path="/modelo", name="Modelo")
df = pd.DataFrame({
    "Tiempo (min)": [0, 5, 10, 15, 20],
    "Temperatura (°C)": [200, 75, 65, 55, 48]
})
fig = px.line(
    df, x="Tiempo (min)", y="Temperatura (°C)",
    title="Curva de enfriamiento",
    markers=True,
    line_shape="spline"
)
layout = html.Div(children=[
    html.Div(children=[
        html.H2("Enfriamiento"),
        dcc.Markdown("""
        Se pide el instante en que $T(t) = 65^\circ C$:

        ---

        **Hipótesis:**  
        - A los 10 minutos se coloca una tapa.  
        - El coeficiente de enfriamiento se reduce a $0.6k$.  
        - La temperatura inicial de esta etapa es $T(10)$.  
        """, mathjax=True)
    ], className="content"),

    html.Div(children=[
        html.H2("Gráfica", className="title"),
        dcc.Graph(
            id="grafico-enfriamiento",
            figure=fig,
            style={"height": "500px"}
        )
    ])
])
