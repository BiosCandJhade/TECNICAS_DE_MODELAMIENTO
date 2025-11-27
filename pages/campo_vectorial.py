import dash 
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff 

dash.register_page(__name__, path="/Campo_Vectorial", name="Campo_Vectorial")

# COLORES ADAPTADOS AL SISTEMA DEL CURSO (TU CSS SE ENCARGA DEL ESTILO GENERAL)
COLOR_DATOS_PRINCIPAL = '#E000CF'  
COLOR_DATOS_SECUNDARIO = '#00CFFF' 
COLOR_TITULO = '#1e3a8a'           
COLOR_TEXTO_SECUNDARIO = '#1f2937' 
COLOR_FONDO_GRAFICO = '#ffffff'
COLOR_FONDO_PAPEL = '#ffffff'
COLOR_GRID = '#ccc'
COLOR_ZEROLINE = '#38bdf8'         

layout = html.Div([
    
    html.Div([
        html.H2("Campo Vectorial", className="title"),

        html.Div([
            html.Label("Ecuación dx/dt:", className="label"),
            dcc.Input(id="input-fx-c5", type="text", value="y", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Ecuación dy/dt:", className="label"),
            dcc.Input(id="input-fy-c5", type="text", value="-x", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango del eje X:", className="label"),
            dcc.Input(id="input-xmax-c5", type="number", value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango del eje Y:", className="label"),
            dcc.Input(id="input-ymax-c5", type="number", value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Mallado (n):", className="label"),
            dcc.Input(id="input-n-c5", type="number", value=15, className="input-field")
        ], className="input-group"),

        html.Button("Generar campo", id="btn-generar-c5", className="btn-generar"),

        html.Div([
            html.H3("Ejemplos para probar:", className="subtitle"),
            html.Ul([
                html.Li("dx/dt = x, dy/dt = y  (Fuente)"),
                html.Li("dx/dt = -x, dy/dt = -y  (Sumidero)"),
                html.Li("dx/dt = y, dy/dt = -x  (Centro)"),
                html.Li("dx/dt = -y, dy/dt = np.cos(x)"),
            ], className="text-content")
        ], className="content")

    ], className="content"), 

    html.Div([
        html.H2("Visualización del Campo Vectorial", className="title"),
        dcc.Graph(id="grafica-campo-c5", style={"height":"450px", "width":"100%"}),
        html.Div(id="info-campo-c5", className="info-message")
    ], className="content")

], className="page-container")

# ----------------------------------------------
# CALLBACK
# ----------------------------------------------

@callback(
    [Output("grafica-campo-c5", "figure"),
     Output("info-campo-c5", "children")],
    Input("btn-generar-c5", "n_clicks"),
    State("input-fx-c5", "value"),
    State("input-fy-c5", "value"),
    State("input-xmax-c5", "value"),
    State("input-ymax-c5", "value"),
    State("input-n-c5", "value"),
    prevent_initial_call=False
)
def generar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):

    if n > 50:
        n = 50
    if n < 5:
        n = 5
        
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    info_mensaje = ""

    try:
        diccionario = {
            "x": X, "y": Y, "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e 
        }
        fx = eval(fx_str, {}, diccionario)
        fy = eval(fy_str, {}, diccionario)

        mag = np.sqrt(fx**2 + fy**2)
        mag[mag == 0] = 1.0  
        fx = fx / mag
        fy = fy / mag

        info_mensaje = f"Magnitud normalizada del campo. (n = {n})"
        
    except Exception as error: 
        fig_error = go.Figure()
        fig_error.update_layout(
            title=f"Error: {str(error)}",
            paper_bgcolor=COLOR_FONDO_PAPEL,
            plot_bgcolor=COLOR_FONDO_GRAFICO,
            font=dict(color=COLOR_TEXTO_SECUNDARIO),
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig_error, f"Error en las expresiones: {str(error)}"

    fig = ff.create_quiver(
        X, Y, fx, fy,
        scale=1.5 / n,
        arrow_scale=0.3,
        line=dict(color=COLOR_DATOS_SECUNDARIO, width=1.3),
        name='Campo Vectorial'
    )

    fig.update_layout(
        title=dict(
            text=f"<b>dx/dt = {fx_str}  |  dy/dt = {fy_str}</b>",
            x=0.5,
            font=dict(size=17, color=COLOR_TITULO)
        ),
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        showgrid=True, gridcolor=COLOR_GRID,
        zeroline=True, zerolinecolor=COLOR_ZEROLINE,
        range=[-xmax*1.1, xmax*1.1]
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=COLOR_GRID,
        zeroline=True, zerolinecolor=COLOR_ZEROLINE,
        range=[-ymax*1.1, ymax*1.1]
    )

    return fig, info_mensaje
