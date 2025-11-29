import dash
from dash import html, dcc, Input, Output
import requests
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/cripto", name="Criptomonedas")

# -------------------------------------------------------
# API COINGECKO – FUNCIONES
# -------------------------------------------------------

def obtener_monedas_disponibles():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        r = requests.get(url, timeout=10)
        coins = r.json()

        common = ["bitcoin", "ethereum", "solana", "dogecoin", "cardano", "litecoin", "xrp"]

        filtered = [c for c in coins if c["id"] in common]

        return [
            {"label": f"{c['id'].capitalize()} ({c['symbol'].upper()})", "value": c["id"]}
            for c in filtered
        ]
    except:
        return []


def obtener_precio(coin_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    params = {
        "vs_currency": "usd",
        "days": days
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "prices" not in data:
        return pd.DataFrame(columns=["timestamp", "price", "coin"])

    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


# -------------------------------------------------------
# LAYOUT
# -------------------------------------------------------

layout = html.Div(className="app-container", children=[

    html.Div(className="app-header", children=[
        html.H1("Precios de Criptomonedas – CoinGecko API")
    ]),

    html.Div(children=[

        html.Label("Selecciona criptomonedas:", style={"font-size": "18px"}),
        dcc.Dropdown(
            id="coin_selector",
            options=obtener_monedas_disponibles(),
            multi=True,
            placeholder="Ejemplo: Bitcoin, Ethereum...",
        ),

        html.Br(),

        html.Label("Rango de días:", style={"font-size": "18px"}),
        dcc.Slider(
            id="days_slider",
            min=1,
            max=30,
            step=1,
            value=7,
            marks={i: str(i) for i in range(1, 31)},
            tooltip={"placement": "bottom", "always_visible": True}
        ),

        html.Br(),
        dcc.Graph(id="crypto_graph", style={"height": "600px"})
    ])
])


# -------------------------------------------------------
# CALLBACK
# -------------------------------------------------------

@dash.callback(
    Output("crypto_graph", "figure"),
    Input("coin_selector", "value"),
    Input("days_slider", "value"),
)
def actualizar_grafico(selected_coins, days):
    if not selected_coins:
        return px.line(title="Selecciona criptomonedas para visualizar el gráfico")

    df_total = pd.DataFrame()

    for coin in selected_coins:
        df = obtener_precio(coin, days)
        if df.empty:
            continue
        df["coin"] = coin
        df_total = pd.concat([df_total, df], ignore_index=True)

    if df_total.empty:
        return px.line(title="No hay datos disponibles para las criptomonedas seleccionadas.")

    fig = px.line(
        df_total,
        x="timestamp",
        y="price",
        color="coin",
        title="Historial de precios (USD)",
        line_shape="linear"
    )

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Precio en USD",
        legend_title="Criptomoneda",
        template="plotly_dark"
    )

    return fig
