import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div([

    # --- SECCIÓN PRINCIPAL ---
    html.Section(className='profile-section', children=[
        html.Div(className='profile-card', children=[
            html.Img(
                src='/assets/toni.png',
                alt='Cristopher Catalán Barrientos',
                className='profile-photo'
            ),
            html.Div(className='profile-info', children=[
                html.H1("Cristopher Antoni Catalán Barrientos", className='profile-name'),
                html.P("Estudiante de Computación Científica – UNMSM", className='profile-role'),
                html.Hr(className='profile-line'),
                dcc.Markdown("""
                Enfocado en el desarrollo de software modular y reproducible con impacto social, 
                integrando herramientas computacionales para el estudio riguroso de fenómenos 
                científicos, educativos y clínicos. Aplica modelos matemáticos, algoritmos inteligentes 
                y entornos automatizados para facilitar la comprensión, simulación y análisis de sistemas complejos.
                """, className='profile-desc', mathjax=True),
                #html.Div(className='profile-tags', children=[
                #    html.Span("Python", className='tag'),
                #    html.Span("Herramientas Office", className='tag'),
                #    html.Span("Html, Js, Css", className='tag'),
                #    html.Span("Modelamiento Matemático", className='tag')
                #]),
            ])
        ])
    ]),

    # --- SOBRE MÍ ---
    html.Section(className='about-section', children=[
        html.H2("Sobre mí"),
        dcc.Markdown("""
            Soy estudiante de Computación Científica, enfocado en el diseño de soluciones reproducibles y 
            escalables mediante el uso de modelos matemáticos, algoritmos inteligentes y programación científica. 
            Me especializo en aplicar técnicas de optimización numérica, modelamiento simbólico y automatización 
            para abordar problemas complejos en ciencia, tecnología y educación, siempre buscando precisión estructural, 
            claridad narrativa y utilidad social.
        """, mathjax=True),
    ]),

    # --- HABILIDADES ---
    html.Section(className='skills-section', children=[
        html.H2("Habilidades"),
        html.Ul([
            html.Li("Programación en Python"),
            html.Li("Análisis y visualización de datos"),
            html.Li("Aprendizaje automático"),
            html.Li("Modelamiento matemático y simulación simbólica"),
            html.Li("Optimización numérica y algoritmos inteligentes"),
            html.Li("Automatización de entornos y flujos de trabajo"),
            html.Li("Diseño de interfaces con Dash y CSS responsivo"),
            html.Li("Backend con Flask, SQL y Docker"),
            html.Li("Control de versiones con Git y GitHub"),
            html.Li("Uso de herramientas y metodologías modernas"),
            html.Li("Pensamiento lógico y resolución de problemas"),
            html.Li("Trabajo en equipo y comunicación técnica")
        ])
    ])
])
