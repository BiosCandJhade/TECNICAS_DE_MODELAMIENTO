"""
import dash
from dash import html, dcc, page_container

app = dash.Dash(__name__, use_pages=False)

app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático"),
    page_container
])

if __name__ == '__main__':
    app.run(debug=True)
"""
"""
import dash
from dash import html,dcc

app = dash.Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.H1("xd"),
	dash.page_container
])
if __name__ == '__main__':
	app.run(debug=True)"""
"""
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
"""
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
