import dash
from dash import html, dcc, register_page
import plotly.graph_objs as go
import numpy as np

# Registrar página
register_page(__name__, path="/crecimiento_poblacion", name="Crecimiento_Poblacion")

def crecimiento_modelo(r, P0, tmax):
    t = np.linspace(0, tmax, 200)
    P = P0 * np.exp(r * t)
    return t, P

layout = html.Div(className="page-container", children=[
    
    html.H1("Crecimiento de la Población", className="page-title"),

    html.Div(className="card", children=[
        html.P(
            "Este modelo muestra el comportamiento de una población sometida a un crecimiento exponencial "
            "de acuerdo a la ecuación P(t) = P0 · e^(r·t).",
            className="page-text"
        )
    ]),

    html.Div(className="card", children=[
        html.Div(className="input-block", children=[
            html.Label("Tasa de crecimiento (r):", className="input-label"),
            dcc.Input(
                id="input-r",
                type="number",
                value=0.1,
                step=0.01,
                className="input-field"
            )
        ]),

        html.Div(className="input-block", children=[
            html.Label("Población inicial (P0):", className="input-label"),
            dcc.Input(
                id="input-p0",
                type="number",
                value=10,
                step=1,
                className="input-field"
            )
        ]),

        html.Div(className="input-block", children=[
            html.Label("Tiempo máximo (t):", className="input-label"),
            dcc.Input(
                id="input-tmax",
                type="number",
                value=10,
                step=1,
                className="input-field"
            )
        ])
    ]),

    html.Div(className="graph-container", children=[
        dcc.Graph(id="graph-crecimiento")
    ])
])

# Callbacks
from dash import callback, Input, Output

@callback(
    Output("graph-crecimiento", "figure"),
    Input("input-r", "value"),
    Input("input-p0", "value"),
    Input("input-tmax", "value"),
)
def actualizar_grafico(r, P0, tmax):
    if r is None or P0 is None or tmax is None:
        return go.Figure()

    t, P = crecimiento_modelo(r, P0, tmax)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=P, mode="lines", name="Población"))

    fig.update_layout(
        title="Crecimiento Exponencial de la Población",
        xaxis_title="Tiempo (t)",
        yaxis_title="Población",
        template="plotly_white",
        height=500
    )
    return fig
