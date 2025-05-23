from dash import Dash, html, dcc

# Inicializar la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.Div(children=[
        # Dropdown para seleccionar el usuario
         html.Label('Usuario'),
        dcc.Dropdown(
            options=[
                {'label': 'Paciente 1', 'value': 'P1'},
                {'label': 'Paciente 2', 'value': 'P2'},
                {'label': 'Paciente 3', 'value': 'P3'}
            ],
            value='P1'  # Valor seleccionado por defecto
        ),

        html.Br(), ##Salto de línea en el contenido
        
        # Multi-Select Dropdown para seleccionar colores presionados
        html.Label('Color(es) Presionado(s)'),
        dcc.Dropdown(
            options=[
                {'label': 'Green', 'value': 'Green'},
                {'label': 'Blue', 'value': 'Blue'},
                {'label': 'Yellow', 'value': 'Yellow'},
                {'label': 'Violet', 'value': 'Violet'}
            ],
            value=['Green'],  # Valores seleccionados por defecto
            multi=True
        ),

        html.Br(),
        
        # Radio Items para seleccionar nivel de progreso
        html.Label('Nivel de Progreso'),
        dcc.RadioItems(
            options=[
                {'label': 'Inicial', 'value': 'Inicial'},
                {'label': 'Intermedio', 'value': 'Intermedio'},
                {'label': 'Avanzado', 'value': 'Avanzado'}
            ],
            value='Intermedio'  # Valor seleccionado por defecto
        ),
    ], style={'padding': 10, 'flex': 1}), #define los estilos CSS aplicados al contenedor.
    # El padding establece un espacio alrededor del componente para que se vea más organizado, 
    # y flex se utiliza para que el componente se ajuste dentro de un contenedor flexible

    html.Div(children=[
        # Checklist para información adicional
        html.Label('Información Adicional'),
        dcc.Checklist(
            options=[
                {'label': 'Mostrar Nombre', 'value': 'nombre'},
                {'label': 'Mostrar Tiempo de interacción', 'value': 'interaccion'}
            ],
            value=['nombre', 'interaccion']  # Valores seleccionados por defecto
        ),

        html.Br(),
        
        # Input de texto para comentarios
        html.Label('Comentarios del Usuario'),
        dcc.Input(
            value='El usuario muestra buen progreso en su rehabilitación.',
            type='text',
            #readOnly=True  # Campo de solo lectura
        ),

        html.Br(),
        html.Br(),
        html.Br(),

        # Slider para nivel de intensidad
        html.Label('Número de interacción'),
        dcc.Slider(
            min=0,
            max=10,
            marks={i: str(i) for i in range(0, 11)},
            value=5  # Valor seleccionado por defecto
        ),
    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flexDirection': 'row'})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
