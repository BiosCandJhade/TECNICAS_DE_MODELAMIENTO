import dash
from dash import html, dcc, register_page
import numpy as np
import plotly.graph_objs as go

# Registrar página dentro del sistema de tu app.py
register_page(
    __name__,
    path="/modelo_sir_rumor",
    name="Modelo SIR de Rumores"
)

# ------------------------------------------------------
# Modelo SIR adaptado a rumor propagación
# ------------------------------------------------------
def modelo_sir_rumor(beta, gamma, S0, I0, R0, tmax=60, steps=600):
    """
    Versión del modelo SIR aplicado a difusión de rumores:
      S(t) = personas que no conocen el rumor
      I(t) = personas que conocen y difunden el rumor
      R(t) = personas que pierden interés y dejan de difundir
    """
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

        S[k + 1] = S[k] + dS * dt
        I[k + 1] = I[k] + dI * dt
        R[k + 1] = R[k] + dR * dt

    return t, S, I, R

# ------------------------------------------------------
# Layout con tu CSS
# ------------------------------------------------------
layout = html.Div(className="page-container", children=[

    html.H1("Modelo SIR de Rumores", className="page-title"),

    html.Div(className="card", children=[
        html.P(
            "Este modelo simula cómo se difunde un rumor en una comunidad usando una variación del modelo SIR. "
            "Las personas pueden estar sin conocer el rumor (S), conocerlo y difundirlo (I), o dejar de difundirlo (R).",
            className="page-text"
        )
    ]),

    # Parámetros
    html.Div(className="card", children=[

        html.Div(className="input-block", children=[
            html.Label("Tasa de difusión del rumor (β):", className="input-label"),
            dcc.Input(id="beta_rumor", type="number", value=0.4, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Tasa de abandono (γ):", className="input-label"),
            dcc.Input(id="gamma_rumor", type="number", value=0.2, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Población susceptible inicial S₀:", className="input-label"),
            dcc.Input(id="S0_rumor", type="number", value=0.95, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Población difusora inicial I₀:", className="input-label"),
            dcc.Input(id="I0_rumor", type="number", value=0.05, step=0.01, className="input-field")
        ]),

        html.Div(className="input-block", children=[
            html.Label("Población retirada inicial R₀:", className="input-label"),
            dcc.Input(id="R0_rumor", type="number", value=0.0, step=0.01, className="input-field")
        ]),
    ]),

    html.Div(className="graph-container", children=[
        dcc.Graph(id="grafico-sir-rumor")
    ])
])

# ------------------------------------------------------
# Callback
# ------------------------------------------------------
from dash import callback, Output, Input

@callback(
    Output("grafico-sir-rumor", "figure"),
    Input("beta_rumor", "value"),
    Input("gamma_rumor", "value"),
    Input("S0_rumor", "value"),
    Input("I0_rumor", "value"),
    Input("R0_rumor", "value")
)
def actualizar_grafico(beta, gamma, S0, I0, R0):

    if None in (beta, gamma, S0, I0, R0):
        return go.Figure()

    t, S, I, R = modelo_sir_rumor(beta, gamma, S0, I0, R0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, name="No conocen (S)", mode="lines"))
    fig.add_trace(go.Scatter(x=t, y=I, name="Difunden (I)", mode="lines"))
    fig.add_trace(go.Scatter(x=t, y=R, name="Abandonan (R)", mode="lines"))

    fig.update_layout(
        title="Dinámica de difusión del rumor",
        xaxis_title="Tiempo",
        yaxis_title="Proporción de la población",
        template="plotly_white",
        height=550
    )

    return fig
