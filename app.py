import dash
from dash import html, dcc, page_container

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server

# Construir enlaces ordenando para que /inicio vaya primero
pages = list(dash.page_registry.values())
pages_sorted = sorted(pages, key=lambda p: (0 if p.get("path") == "/" else 1, p.get("name","")))

links = []
for p in pages_sorted:
    links.append(
        dcc.Link(p.get("name", p["path"]), href=p["path"], style={"margin":"0 10px"})
    )

app.layout = html.Div(className='app-container', children=[
    html.Div(className='app-header', children=[ html.H1("Técnicas de Modelamiento Matemático") ]),
    html.Div(className='navigation', children=[ html.Div(className='nav-links', children=links) ]),
    page_container
])

if __name__ == "__main__":
    app.run(debug=True)
