# /pages/EjercicioSEIR.py
import dash
from dash import html, dcc, Input, Output, State
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import numpy.linalg as LA
import plotly.express as px

dash.register_page(__name__, path="/EjercicioSEIR", name="SEIR - Estabilidad")

# --- funciones de modelo y linealización ---
def seir_rhs(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt =  beta * S * I / N - sigma * E
    dIdt =  sigma * E - gamma * I
    dRdt =  gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

def jacobian_DFE(N, beta, sigma, gamma):
    # Orden: [S, E, I, R]
    J = np.array([
        [0.0,    0.0,      -beta,  0.0],
        [0.0,   -sigma,     beta,  0.0],
        [0.0,    sigma,    -gamma, 0.0],
        [0.0,    0.0,       gamma,  0.0]
    ])
    return J

def dominant_real_part_eig(J):
    eigs = LA.eigvals(J)
    return np.max(np.real(eigs)), eigs

# --- parámetros por defecto ---
N_default = 10000.0
beta_default = 0.5
sigma_default = 1/5.0
gamma_default = 1/7.0
I0_default = 10.0
tmax_default = 160
tsteps_default = 801

# --- layout ---
layout = html.Div(className="app-container", children=[

    html.Div(className="app-header", children=[html.H1("SEIR: estabilidad y tanteos")]),

    # controles principales
    html.Div(style={"display":"flex","gap":"20px","flexWrap":"wrap","padding":"18px"}, children=[

        html.Div(style={"flex":"1","minWidth":"300px","padding":"16px","borderRight":"1px solid #ccc"}, children=[
            html.H3("Parámetros de simulación"),
            html.Label("β (tasa de transmisión)"),
            dcc.Slider(id="beta-slider", min=0.0, max=1.5, step=0.01, value=beta_default,
                       marks={0:"0",0.25:"0.25",0.5:"0.5",1.0:"1.0",1.5:"1.5"}),
            html.Label("σ (tasa de progresión E→I, 1/días)"),
            dcc.Slider(id="sigma-slider", min=0.02, max=1.0, step=0.01, value=sigma_default,
                       marks={0.02:"0.02",0.2:"0.2",0.5:"0.5",1.0:"1.0"}),
            html.Label("γ (tasa de recuperación, 1/días)"),
            dcc.Slider(id="gamma-slider", min=0.02, max=1.0, step=0.005, value=gamma_default,
                       marks={0.02:"0.02",0.142857:"1/7",0.2:"0.2",0.5:"0.5"}),
            html.Br(),
            html.Label("Infectados iniciales I(0)"),
            dcc.Input(id="i0-input", type="number", value=I0_default, min=0, step=1),
            html.Br(), html.Br(),
            html.Label("Duración simulación (días)"),
            dcc.Input(id="tmax-input", type="number", value=tmax_default, min=10, step=10),
            html.Br(), html.Br(),
            html.Button("Simular", id="sim-btn", n_clicks=0, style={"padding":"8px 12px"})
        ]),

        # resultados analíticos y autovalores
        html.Div(style={"flex":"1.2","minWidth":"320px","padding":"16px"}, children=[
            html.H3("Resultados analíticos (DFE)"),
            dcc.Markdown(id="analytic-output", mathjax=True),
            html.H4("Autovalores del Jacobiano en DFE"),
            html.Pre(id="eigs-text", style={"whiteSpace":"pre-wrap","fontSize":"13px","background":"#fff","padding":"8px","borderRadius":"6px"})
        ])
    ]),

    # gráficos: simulación + tanteo estabilidad
    html.Div(style={"display":"flex","gap":"20px","flexWrap":"wrap","padding":"8px"}, children=[

        html.Div(style={"flex":"1.2","minWidth":"380px","padding":"12px","background":"#fff","borderRadius":"8px"}, children=[
            html.H3("Simulación S, E, I, R"),
            dcc.Graph(id="sim-graph", config={"displayModeBar": True}, style={"height":"520px"})
        ]),

        html.Div(style={"flex":"0.9","minWidth":"360px","padding":"12px","background":"#fff","borderRadius":"8px"}, children=[
            html.H3("Tanteo de estabilidad en β"),
            html.Label("Rango de β para tanteo"),
            dcc.Input(id="beta-min", type="number", value=0.0, step=0.01, style={"width":"120px","marginRight":"8px"}),
            dcc.Input(id="beta-max", type="number", value=1.0, step=0.01, style={"width":"120px"}),
            html.Br(), html.Br(),
            html.Label("Puntos en el barrido"),
            dcc.Input(id="n-points", type="number", value=200, min=10, max=2000, step=1),
            html.Br(), html.Br(),
            html.Button("Ejecutar tanteo", id="sweep-btn", n_clicks=0, style={"padding":"8px 12px"}),
            dcc.Graph(id="stability-graph", style={"height":"420px"})
        ])
    ]),

    # resumen numérico del pico
    html.Div(style={"maxWidth":"1000px","margin":"20px auto","padding":"12px"}, children=[
        html.H4("Resumen numérico"),
        html.Div(id="summary-metrics", style={"background":"#fff","padding":"10px","borderRadius":"6px"})
    ])
])

# --- callbacks ---
@dash.callback(
    Output("sim-graph", "figure"),
    Output("analytic-output", "children"),
    Output("eigs-text", "children"),
    Output("summary-metrics", "children"),
    Input("sim-btn", "n_clicks"),
    State("beta-slider", "value"),
    State("sigma-slider", "value"),
    State("gamma-slider", "value"),
    State("i0-input", "value"),
    State("tmax-input", "value")
)
def run_simulation(n_clicks, beta, sigma, gamma, I0, tmax):
    # parámetros
    N = N_default
    if I0 is None or I0 < 0:
        I0 = 1.0
    E0 = 0.0
    R0_init = 0.0
    S0 = N - I0 - E0 - R0_init
    y0 = [S0, E0, I0, R0_init]

    # tiempo
    t = np.linspace(0, float(tmax), int(max(101, np.round(float(tmax))*5)))

    # integración
    sol = odeint(seir_rhs, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = sol.T
    df = pd.DataFrame({"Tiempo": t, "Susceptibles": S, "Expuestos": E, "Infectados": I, "Recuperados": R})
    fig = px.line(df, x="Tiempo", y=["Susceptibles","Expuestos","Infectados","Recuperados"],
                  labels={"value":"Población","variable":"Compartimentos"},
                  title="Dinámica SEIR")
    fig.update_layout(legend_title_text="Compartimentos", template="plotly_white")
    fig.update_traces(mode="lines")

    # pico de I
    idx_peak = np.argmax(I)
    t_peak = float(t[idx_peak])
    I_peak = float(I[idx_peak])

    # Jacobiano y autovalores en DFE
    J = jacobian_DFE(N, beta, sigma, gamma)
    dom_real, eigs = dominant_real_part_eig(J)
    R0_basic = beta / gamma if gamma != 0 else np.nan

    analytic_md = f"""
**Parámetros usados:**  
- $N={int(N)}$  
- $\\beta={beta:.4f}$  
- $\\sigma={sigma:.4f}$  
- $\\gamma={gamma:.4f}$  

**Número reproductivo básico:**  
$$R_0=\\dfrac{{\\beta}}{{\\gamma}}={R0_basic:.4f}$$

**Mayor parte real de autovalores (DFE):** {dom_real:.6f}
"""

    eigs_text = np.array2string(np.round(eigs, 6), separator=", ")

    summary = html.Div([
        html.P(f"Tiempo pico de infectados: {t_peak:.2f} días"),
        html.P(f"Infectados máximos (I_peak): {I_peak:.1f} individuos"),
        html.P(f"R0 calculado: {R0_basic:.4f}"),
        html.P(f"Mayor parte real de autovalores en DFE: {dom_real:.6f} (estable si <0)")
    ])

    # anotar pico en la figura
    fig.add_scatter(x=[t_peak], y=[I_peak], mode="markers+text",
                    marker=dict(size=10, color="#1e3a8a"),
                    text=[f" pico I≈{I_peak:.0f}"],
                    textposition="top center")

    return fig, analytic_md, eigs_text, summary

@dash.callback(
    Output("stability-graph", "figure"),
    Input("sweep-btn", "n_clicks"),
    State("beta-min", "value"),
    State("beta-max", "value"),
    State("n-points", "value"),
    State("sigma-slider", "value"),
    State("gamma-slider", "value")
)
def run_stability_sweep(n_clicks, beta_min, beta_max, n_points, sigma, gamma):
    # validaciones básicas
    if beta_min is None: beta_min = 0.0
    if beta_max is None or beta_max <= beta_min: beta_max = max(beta_min + 0.1, 1.0)
    try:
        n = int(n_points)
    except:
        n = 200
    n = max(10, min(n, 2000))

    betas = np.linspace(float(beta_min), float(beta_max), n)
    dom_reals = []
    r0s = []
    for b in betas:
        J = jacobian_DFE(N_default, b, sigma, gamma)
        dom_real, eigs = dominant_real_part_eig(J)
        dom_reals.append(dom_real)
        r0s.append(b / gamma if gamma != 0 else np.nan)

    df_sweep = pd.DataFrame({"beta": betas, "R0": r0s, "maxRe": dom_reals})

    # figura: maxRe vs R0 (y=0 line)
    fig = px.line(df_sweep, x="R0", y="maxRe",
                  labels={"R0":"R0 (β/γ)","maxRe":"Mayor parte real autovalores"},
                  title="Tanteo de estabilidad: mayor parte real vs R0")
    fig.update_layout(template="plotly_white")
    # línea umbral y=0
    fig.add_hline(y=0.0, line_dash="dash", line_color="red",
                  annotation_text="Umbral estabilidad (0)", annotation_position="top left")
    # marcar el primer cruce (si existe)
    crosses = df_sweep[df_sweep["maxRe"] >= 0]
    if not crosses.empty:
        first = crosses.iloc[0]
        fig.add_scatter(x=[first["R0"]], y=[first["maxRe"]],
                        mode="markers+text",
                        marker=dict(size=8, color="#ff7f0e"),
                        text=[f"cruce R0≈{first['R0']:.3f}"],
                        textposition="bottom right")
    return fig
