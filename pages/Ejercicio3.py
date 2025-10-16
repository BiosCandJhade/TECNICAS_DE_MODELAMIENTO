# Ejercicio3.py
import dash
from dash import html, dcc, callback, Input, Output, State
from dash import dash_table
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.integrate import solve_ivp

dash.register_page(__name__, path="/Semana2", name="Sistema Acoplado")

# ---- Sistema por defecto ----
DEFAULTS = {
    "r": 1.0,       # tasa crecimiento de x
    "kx": 50.0,     # capacidad de carga de x
    "b": 0.02,      # coeficiente depredación
    "a": 0.5,       # tasa máxima de conversión para y
    "n": 10.0,      # constante semisaturación (Holling II)
    "m": 0.1,       # mortalidad de y
    "x0": 10.0,
    "y0": 2.0,
    "tmax": 200.0,
    "npts": 2000
}

def rhs(t, z, r, kx, b, a, n, m):
    x, y = z
    dx = r * x * (1 - x / kx) - b * x * y
    dy = -m * y + (a * x * y) / (n + x)
    return [dx, dy]

def equilibria(r, kx, b, a, n, m):
    E = []
    E.append(("E0", 0.0, 0.0))
    E.append(("E1", kx, 0.0))
    interior = None
    if a > m:
        x_star = (m * n) / (a - m)
        y_star = r * (1 - x_star / kx) / b
        interior = (x_star, y_star)
        if y_star > 0 and x_star > 0:
            E.append(("E*", x_star, y_star))
    return E, interior

def jacobian(x, y, r, kx, b, a, n, m):
    # f_x, f_y, g_x, g_y
    f_x = r - 2 * r * x / kx - b * y
    f_y = -b * x
    g_x = a * n * y / (n + x)**2
    g_y = -m + a * x / (n + x)
    J = np.array([[f_x, f_y],
                  [g_x, g_y]])
    return J

# ---- Layout ----
layout = html.Div([
    html.Div(className="app-header", children=[html.H1("Sistema acoplado (logístico + Holling II)")]),
    html.Div(style={"display":"flex","gap":"20px"}, children=[
        html.Div(style={"flex":"0 0 360px","padding":"10px","border":"1px solid #ddd"}, children=[
            html.H3("Parámetros"),
            html.Label("r (crecimiento x)"),
            dcc.Input(id="r", type="number", value=DEFAULTS["r"], step=0.01),
            html.Br(),
            html.Label("k_x (capacidad carga)"),
            dcc.Input(id="kx", type="number", value=DEFAULTS["kx"], step=1.0),
            html.Br(),
            html.Label("b (depredación)"),
            dcc.Input(id="b", type="number", value=DEFAULTS["b"], step=0.001),
            html.Br(),
            html.Label("a (máx. conversión y)"),
            dcc.Input(id="a", type="number", value=DEFAULTS["a"], step=0.01),
            html.Br(),
            html.Label("n (semisaturación)"),
            dcc.Input(id="n", type="number", value=DEFAULTS["n"], step=0.1),
            html.Br(),
            html.Label("m (mortalidad y)"),
            dcc.Input(id="m", type="number", value=DEFAULTS["m"], step=0.01),
            html.Hr(),
            html.H3("Condiciones iniciales"),
            html.Label("x0"),
            dcc.Input(id="x0", type="number", value=DEFAULTS["x0"], step=0.1),
            html.Br(),
            html.Label("y0"),
            dcc.Input(id="y0", type="number", value=DEFAULTS["y0"], step=0.1),
            html.Hr(),
            html.Label("Tiempo máximo (tmax)"),
            dcc.Input(id="tmax", type="number", value=DEFAULTS["tmax"], step=1.0),
            html.Br(),
            html.Label("Puntos (npts)"),
            dcc.Input(id="npts", type="number", value=DEFAULTS["npts"], step=100),
            html.Br(), html.Br(),
            html.Button("Simular", id="simular", n_clicks=0, style={"width":"100%"}),
            html.Div(id="warnings", style={"color":"darkred","marginTop":"8px"})
        ]),
        html.Div(style={"flex":"1","padding":"10px"}, children=[
            dcc.Tabs(id="tabs", value="tab-time", children=[
                dcc.Tab(label="Series temporales", value="tab-time"),
                dcc.Tab(label="Plano fase", value="tab-phase"),
                dcc.Tab(label="Equilibrios y Jacobiana", value="tab-eq"),
            ]),
            html.Div(id="tab-content")
        ])
    ])
])

# ---- Callbacks ----
@callback(
    Output("tab-content", "children"),
    Output("warnings", "children"),
    Input("simular", "n_clicks"),
    Input("tabs", "value"),
    State("r", "value"),
    State("kx", "value"),
    State("b", "value"),
    State("a", "value"),
    State("n", "value"),
    State("m", "value"),
    State("x0", "value"),
    State("y0", "value"),
    State("tmax", "value"),
    State("npts", "value"),
)
def run_sim(n_clicks, active_tab, r, kx, b, a, n, m, x0, y0, tmax, npts):
    warn = ""
    try:
        r, kx, b, a, n, m = map(float, (r, kx, b, a, n, m))
        x0, y0 = float(x0), float(y0)
        tmax = float(tmax)
        npts = int(max(100, int(npts)))
    except Exception as e:
        return html.Div("Parámetros inválidos."), "Parámetros inválidos."

    E_list, interior = equilibria(r, kx, b, a, n, m)
    t_eval = np.linspace(0, tmax, npts)
    sol = solve_ivp(rhs, [0, tmax], [x0, y0], t_eval=t_eval, args=(r, kx, b, a, n, m), method="RK45", rtol=1e-6)
    df_ts = pd.DataFrame({"t": sol.t, "x": sol.y[0], "y": sol.y[1]})
    fig_time = px.line(df_ts, x="t", y=["x","y"], labels={"value":"Abundancia","variable":"Variable","t":"Tiempo"},
                       title="Series temporales (x, y)")
    fig_time.update_traces(mode="lines")
    fig_phase = px.line(df_ts, x="x", y="y", title="Plano fase (trayectoria desde condición inicial)")
    eq_x = [e[1] for e in E_list]
    eq_y = [e[2] for e in E_list]
    names = [e[0] for e in E_list]
    fig_phase.add_scatter(x=eq_x, y=eq_y, mode="markers+text", text=names, textposition="top center", marker=dict(size=8))

    rows = []
    for name, xe, ye in E_list:
        J = jacobian(xe, ye, r, kx, b, a, n, m)
        tr = np.trace(J)
        det = np.linalg.det(J)
        eigs = np.linalg.eigvals(J)
        eigs_str = ", ".join([f"{eig:.4g}" for eig in eigs])
        rows.append({
            "Equilibrio": name,
            "x*": float(xe),
            "y*": float(ye),
            "tr(J)": float(tr),
            "det(J)": float(det),
            "autovalores": eigs_str
        })

    df_eq = pd.DataFrame(rows)

    if active_tab == "tab-phase":
        content = html.Div([
            dcc.Graph(figure=fig_phase, style={"height":"640px"}),
            html.H4("Vector campo aproximado (malla)"),
            html.P("Se muestran las trayectorias y los puntos de equilibrio.")
        ])
    elif active_tab == "tab-eq":
        content = html.Div([
            html.H3("Equilibrios y propiedades locales"),
            dash_table.DataTable(
                data=df_eq.to_dict("records"),
                columns=[{"name":c, "id":c} for c in df_eq.columns],
                style_table={"overflowX":"auto"},
                style_cell={"textAlign":"left","minWidth":"120px"}
            ),
            html.Hr(),
            html.H4("Condiciones"),
            html.Ul([
                html.Li("Interior E* existe si a > m y y* > 0."),
                html.Li("y* positiva requiere x* < kx.")
            ])
        ])
    else:
        content = html.Div([
            dcc.Graph(figure=fig_time, style={"height":"420px"}),
            html.H4("Tabla de equilibrio"),
            dash_table.DataTable(
                data=df_eq.to_dict("records"),
                columns=[{"name":c, "id":c} for c in df_eq.columns],
                style_table={"overflowX":"auto"},
                style_cell={"textAlign":"left","minWidth":"120px"}
            )
        ])

    if interior is None:
        warn = "No existe equilibrio interior E* (se requiere a > m)."
    else:
        xstar, ystar = interior
        if ystar <= 0 or xstar <= 0 or xstar >= kx:
            warn = f"Equilibrio interior calculado x*={xstar:.4g}, y*={ystar:.4g}. Puede no ser biológicamente válido (y*<=0 o x*>=kx)."

    return content, warn
