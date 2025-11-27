import dash
from dash import html, dcc
import numpy as np
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/Semana1:1", name="Enfriamiento Newton")

# --- Datos y funciones ---
T_amb = 25
T0 = 200
k1 = 0.12
k2 = 0.6 * k1
t_cambio = 10

# Etapa 1
t1 = np.linspace(0, t_cambio, 100)
T1 = T_amb + (T0 - T_amb) * np.exp(-k1 * t1)

# Temperatura al momento de poner la tapa
T10 = T1[-1]

# Etapa 2
t2 = np.linspace(t_cambio, 25, 150)
T2 = T_amb + (T10 - T_amb) * np.exp(-k2 * (t2 - t_cambio))

# Unimos etapas
t_total = np.concatenate([t1, t2])
T_total = np.concatenate([T1, T2])

# Hallamos el instante donde T=65°C
t_obj = t2[np.argmin(np.abs(T2 - 65))]
T_obj = 65

df = pd.DataFrame({"Tiempo (min)": t_total, "Temperatura (°C)": T_total})

# --- Gráfico ---
fig = px.line(
    df, x="Tiempo (min)", y="Temperatura (°C)",
    title="Modelo de Enfriamiento con Cambio de Condiciones",
    markers=False,
    line_shape="spline"
)
fig.add_scatter(x=[t_obj], y=[T_obj],
                mode="markers+text",
                text=[f"T={T_obj}°C a t≈{t_obj:.1f} min"],
                textposition="top center",
                marker=dict(size=10, color="#1e3a8a"))

# --- Layout ---
layout = html.Div(className="app-container", children=[
    html.Div(className="app-header", children=[html.H1("Modelo 1: Enfriamiento")]),

    html.Div(style={"display": "flex", "flex-direction": "row",
                    "justify-content": "space-between"}, children=[

        html.Div(style={
            "flex": "1",
            "padding": "20px",
            "border-right": "1px solid #ccc"
        }, children=[
            html.H2("Planteamiento y resolución"),
            dcc.Markdown(r"""
            **Problema:**  
            Un cuerpo se enfría siguiendo la ley de Newton:
            $T(t) = T_a + (T_0 - T_a)e^{-kt}$

            **Etapas del proceso:**
            1. \( k = 0.12 \) hasta \( t = 10 \) min  
            2. \( k = 0.072 \) después de poner la tapa

            Se obtiene:
            $T(10) = 25 + 175e^{-1.2} \approx 75.4^\circ C$
            $T(t) = 25 + (75.4 - 25)e^{-0.072(t-10)}$
            De 
            $T = 65^\circ C \Rightarrow t \approx %.1f \text{min}$
            """ % t_obj, mathjax=True)
        ]),

        html.Div(style={
            "flex": "1.5",
            "padding": "20px"
        }, children=[
            html.H2("Gráfica del modelo", className="title"),
            dcc.Graph(
                id="grafico-enfriamiento",
                figure=fig,
                style={"height": "500px"}
            )
        ])
    ])
])
