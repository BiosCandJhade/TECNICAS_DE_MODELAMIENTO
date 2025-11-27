import dash
from dash import html, dcc, page_container

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)

server = app.server

# ----------------------------------------------------------
# ORDENAR PÁGINAS: "inicio" debe aparecer primero
# ----------------------------------------------------------
pages = list(dash.page_registry.values())

# si una página usa path="/" o name="inicio", va primero
def prioridad(p):
    path = p.get("path")
    name = p.get("name", "").lower()

    if path == "/" or name == "inicio":
        return 0
    return 1

pages_sorted = sorted(pages, key=lambda p: (prioridad(p), p.get("name", "")))

# ----------------------------------------------------------
# Construir enlaces
# ----------------------------------------------------------
links = [
    dcc.Link(
        p.get("name", p["path"]),
        href=p["path"],
        style={"margin": "0 10px"}
    )
    for p in pages_sorted
]

# ----------------------------------------------------------
# LAYOUT PRINCIPAL UNIFICADO CON TU CSS
# ----------------------------------------------------------
app.layout = html.Div(className="app-container", children=[

    html.Div(className="app-header", children=[
        html.H1("Técnicas de Modelamiento Matemático")
    ]),

    html.Div(className="navigation", children=[
        html.Div(className="nav-links", children=links)
    ]),

    page_container
])

# ----------------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
