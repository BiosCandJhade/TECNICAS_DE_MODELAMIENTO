import dash
from dash import html, dcc, register_page
import numpy as np
import plotly.graph_objs as go

# Registrar la página
register_page(
    __name__,
    path="/resultados_modelo_sir",
    name="Resultados: Susceptibles S(t)"
)

# ------------------------
# Modelo SIR
# ------------------------
def modelo_sir(beta, gamma, S0, I0, R0, tmax=60, steps=600):
    t = np.linspace(0, tmax, steps)
    dt = t[1] - t[0]

    S = np.zeros(steps)
    I = np.zeros(steps)
    R = np.zeros(steps)

    S[0], I[0], R[0] = S0, I0, R0

    for k in range(steps - 1):
        dS = -beta * S[k] * I[k]
        dI = beta * S[k] * I[k] - gamma * I[k]
        dR = gamma * I[k]

        S[k+1] = S[k] + dS * dt
        I[k+1] = I[k] + dI * dt
        R[k+1] = R[k] + dR * dt

    return t, S, I, R

# ------------------------
# Layout adaptado a tu CSS
# ------------------------
layout = html.Div(className="page-container", children=[

    html.H1("Resultados del Modelo SIR", className="page-title"),

    html.Div(className="card", children=[
        html.P(
            "Este módulo muestra los resultados del modelo epidemiológico SIR, "
            "permitiendo visualizar la evolución temporal de los individuos Susceptibles (S), "
            "Infectados (I) y Recuperados (R).",
            className="page-text"
        )
    ]),

    html.Div(className="card", children=[
        html.Div(className="input-block", children=[
            html.Label("Tasa de contagio (β):", className="input-label"),
            dcc.Input(id="beta", type="number", value=0.3, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Tasa de recuperación (γ):", className="input-label"),
            dcc.Input(id="gamma", type="number", value=0.1, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Susceptibles iniciales (S0):", className="input-label"),
            dcc.Input(id="S0", type="number", value=0.99, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Infectados iniciales (I0):", className="input-label"),
            dcc.Input(id="I0", type="number", value=0.01, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Recuperados iniciales (R0):", className="input-label"),
            dcc.Input(id="R0", type="number", value=0.0, step=0.01, className="input-field")
        ])
    ]),

    html.Div(className="graph-container", children=[
        dcc.Graph(id="grafico-sir")
    ])
])

# ------------------------
# Callbacks
# ------------------------
from dash import callback, Input, Output

@callback(
    Output("grafico-sir", "figure"),
    Input("beta", "value"),
    Input("gamma", "value"),
    Input("S0", "value"),
    Input("I0", "value"),
    Input("R0", "value")
)
def actualizar(beta, gamma, S0, I0, R0):
    if None in (beta, gamma, S0, I0, R0):
        return go.Figure()

    t, S, I, R = modelo_sir(beta, gamma, S0, I0, R0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode="lines", name="Susceptibles S(t)"))
    fig.add_trace(go.Scatter(x=t, y=I, mode="lines", name="Infectados I(t)"))
    fig.add_trace(go.Scatter(x=t, y=R, mode="lines", name="Recuperados R(t)"))

    fig.update_layout(
        title="Evolución del Modelo SIR",
        xaxis_title="Tiempo",
        yaxis_title="Proporción de la población",
        template="plotly_white",
        height=550
    )

    return fig
