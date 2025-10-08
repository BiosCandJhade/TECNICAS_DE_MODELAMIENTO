import dash
from dash import html, dcc, page_container
app = dash.Dash(__name__, use_pages=True)
app.layout = html.Div(className='app-container', children=[
    html.Div(className='app-header', children=[
        html.H1("Técnicas de Modelamiento Matemático")
    ]),
    html.Div(className='navigation', children=[
        html.Div(className='nav-links', children=[
            dcc.Link(page['name'], href=page['path']) for page in dash.page_registry.values()
        ])
    ]),
    page_container
])
if __name__ == '__main__':
    app.run(debug=True)
