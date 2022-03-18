import dash
import dash_bootstrap_components as dbc
from dash import html,dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io

from vistas import *
from lectura_archivos import *

# Se utilizan elementos BOOTSTRAP, pero al existir la carpeta assets con un archivo css, automáticamente el programa añade y sigue esa hoja de estilos en conjunto con los elementos de BOOTSTRAP.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Kai Saber 5"
app.update_title='Cargando...'

'''=================LAYOUT GENERAL================='''
menu = html.Div(
    children= [
        html.Div(className='kai5-header',children=[
            html.Img(id='grias-logo',
                src='assets/logos/grias_logo.png', alt='GRIAS logo'),
            html.H2(['KAI SABER 5'])
        ]),
        dbc.Nav(
            [
                #'href' es la ruta (url) que va a tener la página.
                dbc.NavLink("Análisis", href="/",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Departamento", href="/departamento",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Zona", href="/zona",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Municipio", href="/municipio",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Entidad territorial", href="/entidadter",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Establecimiento", href="/establecimiento",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Sede", href="/sede",active="exact",class_name='nav-sidebar'),
                dbc.NavLink("Valores plausibles", href="/valplausibles",active="exact",class_name='nav-sidebar'),     
                dbc.NavLink("Estudiantes", href="/estudiantes",active="exact",class_name='nav-sidebar')           
            ],
            vertical=True,
            pills=True,  
            className="menu"
        ),   
    ],
    className="contenedor-menu"
)

content = html.Div(id="page-content",children=[],className="contenedor-pestana")

# Se crea el layout general con los componentes anteriomente creados.
app.layout = html.Div(className='contenedor-general', children=[
    dcc.Location(id="url"),
    menu,
    content
])

"""
Recibe como Input la url de la página clickeada o activa.
    Por ejemplo:
    saber5dashboard.com/departamento, donde /departamento = pathname

Retorna como Output el children que corresponde al contenido de cada pestaña.
"""
@app.callback(
    Output("page-content","children"),
    [Input("url","pathname")]
)

def update_contenido_pagina(pathname):
    """Actualiza el contenido de la pestaña activa, dependiendo de la url activa.

    Args:
        pathname ([str]): [Url de la página activa]

    Returns:
        html: [Componente HTML a mostrar por cada página]
    """    
    if pathname == "/": # Refiere al 'Home' o 'Inicio'.
        header =  html.Div(className='header', children=[
            html.H1(children='Análisis de datos'),
        ])

        inputSeparador = html.Div(
            [
                dbc.Label("Separador"),
                dbc.Input(
                    id='txfsep',
                    placeholder="Por defecto es '|'",
                    type="text",
                    size=22
                )
            ]
        )
        upload = dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastre el archivo o ',
                html.A('Seleccione un archivo')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=True               
        )

        return [
            header,
            html.Div(className='resultado-pestana', children=[
                inputSeparador,
                upload,
                # Mostrará la tabla según el archivo subido.                         
                html.Div(id='output-data-upload'),
                # Mostrará la información del atributo escogido en la tabla.
                html.Div(id='info-atributo')
            ])
        ]
    elif pathname == "/departamento":
        
        # Guarda los datos que se generan en el callback de creación de la tabs para poder utilizarlo en una tab diferente a Tabla.
        dataDeptos = dcc.Store(id='data-depto', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Departamento'),
        ])

        deptoZonasDropdown = html.Div(
            children=[
                dbc.Label("Zona"),
                dcc.Dropdown(
                    id='deptozonas',
                    options=opt_zonas_en_deptos,
                    value='Todos los departamentos',
                    placeholder="Elija una zona..."
                )
            ]
        )

        deptoDeptoDropdown = html.Div(
            children=[
                dbc.Label("Departamento"),
                dcc.Dropdown(
                    id='deptodepto',
                    placeholder="Elija un departamento..."
                )
            ]
        )

        formDeptos = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[deptoZonasDropdown],width=6),

                        dbc.Col(children=[deptoDeptoDropdown],width=6)
                    ],                    
                )   
            ],
            class_name='form-dropdowns'
        )    

        return html.Div([
            header,
            html.Div(className='resultado-pestana', children=[
                dataDeptos,            
                formDeptos,
                inicializar_tabs_comp('depto')
            ])
        ])        
    elif pathname == "/zona":

        # Guarda los datos que se generan en el callback de creación de la tabs para poder utilizarlo en una tab diferente a Tabla.
        dataZona = dcc.Store(id='data-zona', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Zona'),
        ])

        zonasZonasDropdown = html.Div(
            children=[
                dbc.Label("Zona"),
                dcc.Dropdown(
                    id='zonaszonas',
                    options=opt_zonas_en_zonas,
                    value='Todas las zonas',
                    placeholder="Elija una zona..."
                )
            ]
        )

        formZonas = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[zonasZonasDropdown],width=12)
                    ]
                ),
            ],
            class_name='form-dropdowns'
        )  

        return [
            header,
            html.Div(className='resultado-pestana', children=[
                dataZona,            
                formZonas, 
                inicializar_tabs_comp('zona')
            ])
        ]
    elif pathname == "/entidadter":

        # Guarda los datos que se generan en el callback de creación de la tabs para poder utilizarlo en una tab diferente a Tabla.
        dataEnt = dcc.Store(id='data-ent', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Entidad territorial'),
        ])
   
        entDropdown = html.Div(
            children=[
                dbc.Label("Entidad territorial"),
                dcc.Dropdown(
                    id='entdropdown',
                    options=opt_ent_territoriales,
                    value='Todas las entidades territoriales',
                    placeholder="Elija una entidad territorial..."
                )
            ]
        ) 

        tipoentDropdown = html.Div(
            children=[
                dbc.Label("Tipo de entidad territorial"),
                dcc.Dropdown(
                    id='tipoentdropdown',
                    options=[
                        {'label':'Todas las entidades territoriales', 'value': '-1'},
                        {'label':'Departamento', 'value': '0'},
                        {'label':'Etc', 'value': '1'},
                        {'label':'Municipio', 'value': '2'}
                    ],
                    value='-1',
                    placeholder="Elija una el tipo de entidad territorial..."
                )
            ]
        )        
        
        formEnt = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[tipoentDropdown],width=6),

                        dbc.Col(children=[entDropdown],width=6)
                    ],                    
                )   
            ],
            class_name='form-dropdowns'
        )  

        return [
            header,
            html.Div(className='resultado-pestana', children=[
                dataEnt,            
                formEnt,            
                inicializar_tabs_comp('ent')
            ])
        ]
    elif pathname == "/municipio":

        # Guarda los datos que se generan en el callback de creación de la tabs para poder utilizarlo en una tab diferente a Tabla.
        dataEnt = dcc.Store(id='data-mpio', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Municipio'),
        ])
        
        mpiodeptoDropdown = html.Div(
            children=[
                dbc.Label("Departamento"),
                dcc.Dropdown(
                    id='mpioddepto',
                    options=opt_deptos_en_mpios,
                    value='Todos los municipios',
                    placeholder="Elija un departamento..."
                )
            ]
        ) 

        mpiompioDropdown =  html.Div(
            children=[
                dbc.Label("Municipio"),
                dcc.Dropdown(
                    id='mpioddmpio',                    
                    placeholder="Elija un municipio..."
                )
            ]
        ) 

        formMpios = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[mpiodeptoDropdown],width=6),

                        dbc.Col(children=[mpiompioDropdown],width=6)
                    ]
                )   
            ],
            class_name='form-dropdowns'
        ) 

        return [    
            header,           
            html.Div(className='resultado-pestana', children=[
                dataEnt,            
                formMpios,
                inicializar_tabs_comp('mpio')
            ])
        ]
    elif pathname == "/establecimiento":

        # Guarda los datos que se generan en el callback de creación de la tabs para poder utilizarlo en una tab diferente a Tabla.
        dataEst = dcc.Store(id='data-est', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Establecimiento educativo'),
        ])

        estdeptoDropdown = html.Div(
            children=[
                dbc.Label("Departamento"),
                dcc.Dropdown(
                    id='estdepto',
                    options=opt_deptos_en_est,
                    value='Amazonas',
                    placeholder="Elija un departamento..."
                )
            ]
        ) 

        estmpioDropdown = html.Div(
            children=[
                dbc.Label("Municipio"),
                dcc.Dropdown(
                    id='estmpio',
                    placeholder="Elija un municipio..."
                )
            ]
        ) 

        estDropdown = html.Div(
            children=[
                dbc.Label("Establecimiento"),
                dcc.Dropdown(
                    id='estestablmtos',            
                    placeholder="Elija un establecimiento...",
                    optionHeight=50
                )
            ]
        )

        formEst = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[estdeptoDropdown],width=6),

                        dbc.Col(children=[estmpioDropdown],width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col(children=[estDropdown],width=12),
                    ],
                    class_name='another-row'
                )   
            ],
            class_name='form-dropdowns'
        ) 

        return [
            header,  
            html.Div(className='resultado-pestana', children=[
                dataEst,            
                formEst,
                inicializar_tabs_comp('est')
            ])
        ]
    elif pathname == "/sede":
        # Guarda los datos que se generan en el callback de creación de la tabs para poder utilizarlo en una tab diferente a Tabla.
        dataSede= dcc.Store(id='data-sede', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Sede de establecimiento educativo'),
        ])

        sedeDeptoDropdown = html.Div(
            children=[
                dbc.Label("Departamento"),
                dcc.Dropdown(
                    id='estdepto',
                    options=opt_deptos_en_est,
                    value='Amazonas',
                    placeholder="Elija un departamento..."
                )
            ]
        ) 

        sedeMpioDropdown = html.Div(
            children=[
                dbc.Label("Municipio"),
                dcc.Dropdown(
                    id='estmpio',
                    placeholder="Elija un municipio..."
                )
            ]
        ) 

        sedeEstDropdown = html.Div(
            children=[
                dbc.Label("Establecimiento"),
                dcc.Dropdown(
                    id='estestablmtos',           
                    placeholder="Elija un establecimiento...",
                    optionHeight=50
                )
            ]
        )

        sedeSedeDropdown = html.Div(
            children=[
                dbc.Label("Sede"),
                dcc.Dropdown(
                    id='sedesede',            
                    placeholder="Elija un establecimiento...",
                    optionHeight=50
                )
            ]
        )

        sedeJrnadasDropdown = html.Div(
            children=[
                dbc.Label("Jornada"),
                dcc.Dropdown(
                    id='sedejrnadas',            
                    placeholder="Elija una jornada..."
                )
            ]
        ) 

        formSede = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[sedeDeptoDropdown],width=6),
                        dbc.Col(children=[sedeMpioDropdown],width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col(children=[sedeEstDropdown],width=6),
                        dbc.Col(children=[sedeSedeDropdown],width=6),
                    ],
                    class_name='another-row'
                ),
                dbc.Row(
                    children=[
                        dbc.Col(children=[sedeJrnadasDropdown],width=12),
                    ],
                    class_name='another-row'
                ) 
            ],
            class_name='form-dropdowns'
        ) 

        return [
            header,  
            html.Div(className='resultado-pestana', children=[
                dataSede,            
                formSede,
                inicializar_tabs_comp('sede')
            ])
        ]
    elif pathname == "/valplausibles":  

        header =  html.Div(className='header', children=[
            html.H1(children='Valores plausibles'),
        ])        
        
        estdeptoDropdown = html.Div(
            children=[
                dbc.Label("Departamento"),
                dcc.Dropdown(
                    id='estdepto',
                    options=opt_deptos_en_est,
                    value='Amazonas',
                    placeholder="Elija un departamento..."
                )
            ]
        ) 

        estmpioDropdown = html.Div(
            children=[
                dbc.Label("Municipio"),
                dcc.Dropdown(
                    id='estmpio',
                    placeholder="Elija un municipio..."
                )
            ]
        ) 

        estDropdown = html.Div(
            children=[
                dbc.Label("Establecimiento"),
                dcc.Dropdown(
                    id='estestablmtos',            
                    placeholder="Elija un establecimiento...",
                    optionHeight=50
                )
            ]
        )

        formEst = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[estdeptoDropdown],width=6),

                        dbc.Col(children=[estmpioDropdown],width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col(children=[estDropdown],width=12),
                    ],
                    class_name='another-row'
                )   
            ],
            class_name='form-dropdowns'
        ) 

        return [  
            header,
            html.Div(className='resultado-pestana', children=[
                formEst,
                html.Div(id='contenedor-valplau',children=[])
            ])
        ]
    elif pathname == "/estudiantes":         
        header =  html.Div(className='header', children=[
            html.H1(children='Estudiantes'),
        ])

        sedeDeptoDropdown = html.Div(
            children=[
                dbc.Label("Departamento"),
                dcc.Dropdown(
                    id='estdepto',
                    options=opt_deptos_en_est,
                    value='Amazonas',
                    placeholder="Elija un departamento..."
                )
            ]
        ) 

        sedeMpioDropdown = html.Div(
            children=[
                dbc.Label("Municipio"),
                dcc.Dropdown(
                    id='estmpio',
                    placeholder="Elija un municipio..."
                )
            ]
        ) 

        sedeEstDropdown = html.Div(
            children=[
                dbc.Label("Establecimiento"),
                dcc.Dropdown(
                    id='estestablmtos',           
                    placeholder="Elija un establecimiento...",
                    optionHeight=50
                )
            ]
        )

        sedeSedeDropdown = html.Div(
            children=[
                dbc.Label("Sede"),
                dcc.Dropdown(
                    id='sedesede',            
                    placeholder="Elija un establecimiento...",
                    optionHeight=50
                )
            ]
        )
        
        formSede = dbc.Form(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(children=[sedeDeptoDropdown],width=6),
                        dbc.Col(children=[sedeMpioDropdown],width=6)
                    ]
                ),
                dbc.Row(
                    children=[
                        dbc.Col(children=[sedeEstDropdown],width=6),
                        dbc.Col(children=[sedeSedeDropdown],width=6),
                    ],
                    class_name='another-row'
                )                 
            ],
            class_name='form-dropdowns'
        )

        return [
            header,
            html.Div(className='resultado-pestana', children=[ 
                formSede,
                inicializar_tabs_estudiantes()
            ])
        ]
    # Si se intenta acceder a url que no existe, se muestra un mensaje de error.
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

'''=================CALLBACKS EN ANÁLISIS================='''
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              Input('txfsep', 'value'))
def update_output(list_of_contents, list_of_names, list_of_sep):
    """Actualiza el contenido del contenedor según el archivo o archivos subidos en el elemento Upload.

    Args:
        list_of_contents (list): Contenido del archivo o archivos subidos
        list_of_names (list): Nombre del archivo o archivos subidos
        list_of_sep (list): Separador o separadores configurados

    Returns:
        html: Componente HTML que cambia según el archivo cargado en el upload
    """    
    if not list_of_sep:
        list_of_sep = "|"
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, s) for c, n, s in
            zip(list_of_contents, list_of_names, list_of_sep)]
        return children

# Función para lectura de archivos    
def parse_contents(contents, filename, sepr):
    """Lee el archivo subido en el componente Upload con un encoding utf-8.
    Se define una variable global. Si la lectura es exitosa, se inicializa la variable como un DataFame de pandas con los datos del archivo cargado.

    Args:
        contents (bytes): Archivos subido en el componente Upload
        filename (str): Nombre de los archivos subidos
        sepr (str): Caracter del separador del CSV

    Returns:
        html: HTML Div tipo alerta que informa si se logró cargar el archivo.
    """    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        global df 
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            aux = pd.read_csv(io.StringIO(decoded.decode('utf-8')),sep=sepr,na_values='null')
            df = aux
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file            
            aux = pd.read_excel(io.StringIO(decoded.decode('utf-8')),sep=sepr,na_values='null')
            df = aux
    except Exception as e:
        return html.Div([
            dbc.Alert("No se pudo cargar el archivo. Revisar separador", color="danger")
        ])

    # Tabla que muestra los registros del CSV
    tablaArchivo = generar_tabla_general(df,'')
    
    # Tabla que muestra el listado de atributos
    analisisAtributo = generar_analisis_atributos(df)

    return html.Div([
        tablaArchivo,
        html.H2('Análisis'),
        analisisAtributo
    ])

@app.callback(
    Output('grafico-atributo','figure'),
    [Input('datatable-atributo','selected_rows'),
    Input('datatable-atributo','data')]
)
def actualizarGraficoAtributo(atributo_analisis,dataTablaAtributo):
    """Actualiza el gráfico de análisis de atributos dependiendo del atributo seleccionado en la tabla. Solamente permite analizar si el atributo tiene 10 o menos valores distintos.

    Args:
        atributo_analisis (list): Lista de atributos seleccionados
        dataTablaAtributo (DataFrame): Datos(dcc.Store) del atributo seleccionado.

    Returns:
        px.bar: Gráfico de barras con la información de los valores del atributo seleccionado.
    """
    # Se apunta al atributo seleccionado en la primera posición de la lista de atributos seleccionados, y después se filtra el dataframe del archivo subido con dicho atributo seleccionado.
    dictAtributoSelected = dataTablaAtributo[atributo_analisis[0]] 

    # Se obtiene el dataframe del atributo selecconado
    atributoSeleccionado = df[dictAtributoSelected['ATRIBUTO']]
    
    # Muestra los valores unicos con su respectivo count
    dffAtributoGrafico = atributoSeleccionado.value_counts()

    # Se prepara el dataframe para graficarlo
    dffAtributoGrafico = dffAtributoGrafico.to_frame()
    dffAtributoGrafico.reset_index(inplace = True) 
    dffAtributoGrafico.rename(columns = {'index':'VALOR'}, inplace = True)
    dffAtributoGrafico.rename(columns={dffAtributoGrafico.columns[1]: 'COUNT'}, inplace = True)

    figure = px.bar()
    # Se limita a graficar hasta 10 valores distintos
    if atributoSeleccionado.nunique() <= 10:        
        figure = px.bar(
            data_frame=dffAtributoGrafico,
            x = "VALOR",
            y = "COUNT",
            title=atributoSeleccionado.name
        )

    return figure   

'''=================CALLBACKS EN DEPARTAMENTOS================='''
@app.callback(
    Output(component_id='deptodepto', component_property='options'),
    [Input(component_id='deptozonas', component_property='value')]
)
def update_deptodepto(zona_seleccionada):   
    """Actualiza el dropdown de departamentos en 'Departamento' dependiendo de la zona seleccionada.

    Args:
        zona_seleccionada (str): Valor del dropdown de la zona escogida en 'Departamento'

    Returns:
        list of dict: [Departamentos de la zona seleccionada]
    """    
    deptosZonasCopy = deptosZonas[deptosZonas['ZONA']==zona_seleccionada]
    deptosdropdown = [{'label': deptosZonasCopy['DEPARTAMENTO'][i], 'value': deptosZonasCopy['DEPARTAMENTO'][i]} for i in deptosZonasCopy.index]
    return deptosdropdown

@app.callback(
    Output('deptodepto', 'value'),
    [Input('deptodepto', 'options')]
)
def update_dp(deptodepto_options):
    """Selecciona el primer valor del dropdown de departamentos en 'Departamento' después de que este fuese actualizado.

    Args:
        deptodepto_options (list of dict): Opciones del dropdown de departamentos en 'Departamento'

    Returns:
        str: Valor de la primera opción del dropdown de departamentos en 'Departamento'
    """    
    return deptodepto_options[0]['value']
 
@app.callback(
    Output('data-depto','data'),
    Output('content-tabs-vistas-depto','children'),
    [Input('deptodepto', 'value'),
    Input('tabs-comp-depto','active_tab'),
    Input('tabs-vistas-depto','active_tab')]
 )
def actualizar_info_depto(deptodepto,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráfico y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        deptodepto (str): [Valor del dropdown de departamentos]
        tabsCompActiva (str): [Id de la tab de competencias activa]
        tabsVistasActiva (str): [Id del la tab de vistas activa]

    Returns:
        dict: [Datos(dcc.Store) del departamento seleccionado]
        html: [Componente HTML con el contenido de las tabs seleccionadas]
    """    
    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-depto":
        dffCompetencia = deptosLen
    elif tabsCompActiva == "tab-mat-depto":
        dffCompetencia = deptosMat

    # Filtra según el departamento escogido
    seleccion = dffCompetencia[dffCompetencia['DEPARTAMENTO']==deptodepto] 

    # Si se elige 'Todos los departamentos', en la tabla se muestran todos los departamentos.
    if 'Todos los departamentos'==deptodepto:
        df_tabla = dffCompetencia
    else: #Si no, se muestra la seleccion por departamento
        df_tabla = seleccion
    
    # Crea el contenedor que se va a enviar según la tab activa    
    contenedorOutput = generar_cont_tab_activa(tabsVistasActiva,deptodepto,seleccion,df_tabla,'csv/Departamento/deptosdocs.txt','grafico-depto')

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generar_data_grafico_dinamico(seleccion)
    
    return dataGrafico,contenedorOutput
  
@app.callback(
    Output('grafico-depto','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-depto','data')]
)
def actualizar_grafico_depto(tipoGrafico,dataDeptos):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico (str): Valor del dropdown de tipo de gráfico
        dataDeptos (dict): Datos(dcc.Store) del departamento seleccionado

    Returns:
        px.figure: Gráfico con la información seleccionada
    """    
    return generar_grafico_puntajes(dataDeptos,tipoGrafico)

'''=================CALLBACKS EN ZONA================='''

@app.callback(
    Output('data-zona','data'),
    Output('content-tabs-vistas-zona','children'),
    [Input('zonaszonas', 'value'),
    Input('tabs-comp-zona','active_tab'),
    Input('tabs-vistas-zona','active_tab')]
 )
def actualizar_info_zona(zonaszonas,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        zonaszonas (str): Valor del dropdown de zonas en 'Zona'
        tabsCompActiva (str): Id de la tab de competencias activa
        tabsVistasActiva (str): Id del la tab de vistas activa

    Returns:
        dict: Datos(dcc.Store) del departamento seleccionado
        html: Contenedor HTML con el contenido de las tabs seleccionadas
    """    

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-zona":
        dffCompetencia = zonasLen
    elif tabsCompActiva == "tab-mat-zona":
        dffCompetencia = zonasMat

    # Filtra según el departamento escogido
    seleccion = dffCompetencia[dffCompetencia['ZONA']==zonaszonas] 

    # Si se elige 'Todas las zonas', en la tabla se muestran todas las zonas
    if 'Todas las zonas'==zonaszonas:
        df_tabla = dffCompetencia
    else:
        df_tabla = seleccion
    
    # Crea el contenedor que se va a retornar según la tab activa    
    contenedorOutput = generar_cont_tab_activa(tabsVistasActiva,zonaszonas,seleccion,df_tabla,'csv/Zonas/zonasdocs.txt','grafico-zona') 

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generar_data_grafico_dinamico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-zona','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-zona','data')]
)
def actualizar_grafico_zona(tipoGrafico,dataZona):
    """Actualiza el gráfico de la tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico (str): Valor del dropdown del tipo de gráfico
        dataDeptos (type): Datos(dcc.Store) con la información de la zona seleccionada

    Returns:
        html: Contenedor HTML con el gráfico a mostrar
    """    

    return generar_grafico_puntajes(dataZona,tipoGrafico)



'''=================CALLBACKS EN ENTIDAD TERRITORIAL================='''
@app.callback(
    Output('entdropdown', 'options'),
    [Input('tipoentdropdown', 'value')]
)
def update_entdropdown(tipoent_seleccionada):
    """Actualiza el dropdown de entidades territoriales en dependiendo del tipo de entidad seleccionada

    Args:
        tipoent_seleccionada (str): Valor elegido en el dropdown de tipo de entidades territoriales

    Returns:
        list of dict: Entidades territoriales del tipo de entidad sseleccionado
    """ 

    # Se filtra por tipo de entidad
    enterritorialesCSVCopy = enterritorialesCSV[enterritorialesCSV['TIPO']==int(tipoent_seleccionada)]

    # Se crean las opcions del dropdown a mostrarse
    entDp = [{'label': enterritorialesCSVCopy['ENTIDAD'][i], 'value': enterritorialesCSVCopy['ENTIDAD'][i]} for i in enterritorialesCSVCopy.index]
    
    return entDp
    
@app.callback(
    Output('entdropdown', 'value'),
    [Input('entdropdown', 'options')]
)
def update_dp(entdropdown_options):
    """Selecciona la primer entidad territorial según el tipo seleccionado, después de que este fuese actualizado.

    Args:
        entdropdown_options (list of dicts): Lista de opciones del dropdown de entidades territoriales

    Returns:
        str: Valor de la primera opción del dropdown de entidades territoriales
    """    
    return entdropdown_options[0]['value']


@app.callback(
    Output('data-ent','data'),
    Output('content-tabs-vistas-ent','children'),
    [Input('entdropdown', 'value'),
    Input('tabs-comp-ent','active_tab'),
    Input('tabs-vistas-ent','active_tab')]
 )
def actualizar_info_ent(etdropdownvalue,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráfico y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        etdropdownvalue (str): Valor del dropdown de entidad territorial
        tabsCompActiva (str): Id de la tab de competencias activa
        tabsVistasActiva (str): Id del la tab de vistas activa

    Returns:
        dict:Diccionario con los datos de la entidad territorial seleccionado
        html: Contenedor HTML con el children de la tab activa
    """    

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-ent":
        dffCompetencia = entLen
    elif tabsCompActiva == "tab-mat-ent":
        dffCompetencia = entMat

    # Filtra según el departamento escogido
    seleccion = dffCompetencia[dffCompetencia['ENTIDAD']==etdropdownvalue] 

    # Si se elige todos los departamentos, en la tabla se muestran todos los departamentos.
    if 'Todas las entidades territoriales'==etdropdownvalue:
        df_tabla = dffCompetencia
    else:
        df_tabla = seleccion
    
    # Crea el contenedor que se va a enviar según la tab activa
    contenedorOutput = generar_cont_tab_activa(tabsVistasActiva,etdropdownvalue,seleccion,df_tabla,'csv/Entidad Territorial/entdocs.txt','grafico-ent') 

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generar_data_grafico_dinamico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-ent','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-ent','data')]
)
def actualizar_grafico_ent(tipoGrafico,dataEnt):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico (str): Valor del dropdown del tipo de gráfico
        dataEnt (dict): Diccionario con la información de la entidad territorial seleccionada

    Returns:
        html: Contenedor HTML del gráfico a mostrar en la tab de gráfico
    """    

    return generar_grafico_puntajes(dataEnt,tipoGrafico)



'''=================CALLBACKS EN MUNICIPIOS================='''
@app.callback(
    Output(component_id='mpioddmpio', component_property='options'),
    [Input(component_id='mpioddepto', component_property='value')]
)
def update_deptodepto(depto_seleccionado):
    """Actualiza el dropdown de municipios en dependiendo del departamento seleccionado.

    Args:
        depto_seleccionado (str): Valor elegido en el dropdown de departamentos en 'Municipio'

    Returns:
        list of dict: Departamentos de la zona seleccionada
    """
    mpioLenCopy = mpioLen[mpioLen['DEPA_NOMBRE']==depto_seleccionado]
    mpiosdropdown = [{'label': mpioLenCopy['MUNI_NOMBRE'][i], 'value': mpioLenCopy['MUNI_ID'][i]} for i in mpioLenCopy.index]
    return mpiosdropdown
    
@app.callback(
    Output('mpioddmpio', 'value'),
    [Input('mpioddmpio', 'options')]
)
def update_dp(mpioddmpio_options):
    """Selecciona el primer municipio en el dropdown de municipios después de ser actualizado

    Args:
        mpioddmpio_options (list of dicts): Lista de las opciones del dropdown de municipios

    Returns:
        str: Valor del primer municipio en el dropdown de Municipios
    """    
    return mpioddmpio_options[0]['value']

@app.callback(
    Output('data-mpio','data'),
    Output('content-tabs-vistas-mpio','children'),
    [Input('mpioddmpio', 'value'),
    Input('tabs-comp-mpio','active_tab'),
    Input('tabs-vistas-mpio','active_tab')]
 )
def actualizar_info_mpio(mpioddmpiovalue,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráfico y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        mpioddmpiovalue (str): Valor del dropdown de municipios en 'Municipio'      
        tabsCompActiva (str): Id de la tab de competencias activa
        tabsVistasActiva (str): Id del la tab de vistas activa

    Returns:
        dict: Diccionario con los datos del municipio seleccionado
        html: Contenedor HTML con el children de la tab activa
    """    

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-mpio":
        dffCompetencia = mpioLen
    elif tabsCompActiva == "tab-mat-mpio":
        dffCompetencia = mpioMat


    # Se manejó con ids porque hay algunos municipios que tienen el mismo nombre(pero de diferente departamento) y lo único que los diferencia es el id.
    seleccion = dffCompetencia[dffCompetencia['MUNI_ID']==mpioddmpiovalue]
    
    # 0 es el id de 'Todos los municipios'.
    if 0==mpioddmpiovalue:
        df_tabla = dffCompetencia
    else:
        df_tabla = seleccion
    
    # Crea el contenedor que se va a enviar según la tab activa
    contenedorOutput = generar_cont_tab_activa(tabsVistasActiva,seleccion['MUNI_NOMBRE'],seleccion,df_tabla,'csv/Municipios/mpiosdocs.txt','grafico-mpio')

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generar_data_grafico_dinamico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-mpio','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-mpio','data')]
)
def actualizar_grafico_mpio(tipoGrafico,dataMpio):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico (str): Valor del dropdown del tipo de gráfico
        dataMpio (dict): Diccionario con la información del municipio seleccionado

    Returns:
        html: Contenedor HTML del gráfico a mostrar en la tab de gráfico
    """    

    return generar_grafico_puntajes(dataMpio,tipoGrafico)


'''=================CALLBACKS EN ESTABLECIMIENTO================='''
@app.callback(
    Output('estmpio', 'options'),
    [Input('estdepto', 'value')]
)
def update_estmpio(estdeptovalue):
    """Actualiza el dropdown de municipios dependiendo del departamento seleccionado

    Args:
        estdeptovalue (str): Valor del municipio escogido en el dropdown de departamentos en 'Municipio'

    Returns:
        list of dict: Lista de municipios del departamento seleccionado
    """
    estMpiosCopy = estMpios[estMpios['DEPA_NOMBRE']==estdeptovalue]
    estmpiosDropdown = [{'label': estMpiosCopy['MUNI_NOMBRE'][i], 'value': estMpiosCopy['MUNI_ID'][i]} for i in estMpiosCopy.index]
    return estmpiosDropdown
    
@app.callback(
    Output('estmpio', 'value'),
    [Input('estmpio', 'options')]
)
def update_dp(estmpio_options):
    """Selecciona el primer municipio en el dropdown de municipios al ser actualizado

    Args:
        estmpio_options (list of dicts): Lista de las opciones del dropdown de municipios

    Returns:
        str: Valor del primer municipio en el dropdown de Municipios
    """    
    return estmpio_options[0]['value']

@app.callback(
    Output('estestablmtos','options'),
    [Input('estmpio','value')]
)
def actualizar_dpestablecimientos(estmpio_value):
    """Actualiza el dropdown de establecimientos según el municipio seleccionado

    Args:
        estmpio_value (str): Valor del municipio seleccionado

    Returns:
        list of dict: Lista de establecimientos en el municipio seleccionado
    """    
    estInfoCopy = estInfo[estInfo['MUNI_ID']==estmpio_value]
    estDropdown = [{'label': estInfoCopy['NOMBRE'][i], 'value': estInfoCopy['COD_DANE'][i]} for i in estInfoCopy.index]

    return estDropdown

@app.callback(
    Output('estestablmtos', 'value'),
    [Input('estestablmtos', 'options')])
def update_dp(estestablmtos_options):
    """"Selecciona la primera opción del dropdown de establecimientos
    al ser actualizado.

    Args:
        estestablmtos_options (list of dicts): Lista de opciones del dropdown de establecimientos

    Returns:
        str: Valor de la primera opción del dropdown de establecimientos
    """    
    return estestablmtos_options[1]['value']


@app.callback(
    Output('data-est','data'),
    Output('content-tabs-vistas-est','children'),
    [Input('estestablmtos', 'value'),
    Input('tabs-comp-est','active_tab'),
    Input('tabs-vistas-est','active_tab')]
 )
def actualizar_info_est(estestablmtos_value,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        estestablmtos_value (str): Valor del establecimiento escogido
        tabsCompActiva (str): Id de la tab de competencias activa
        tabsVistasActiva (str): Id del la tab de vistas activa

    Returns:
        dict: Diccionario con los datos del establecimiento escogido
        html: Contenedor HTML con el children de la tab activa
    """        

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-est":
        dffCompetencia = estLen
    elif tabsCompActiva == "tab-mat-est":
        dffCompetencia = estMat

    # Se manejó con COD_DANE porque los archivos de competencias solo se pueden conectar por ese atributo
    seleccion = dffCompetencia[dffCompetencia['COD_DANE']==estestablmtos_value]

    nombre = estInfo[estInfo['COD_DANE']==estestablmtos_value]

    # Si el establecimiento no presentó la prueba
    if seleccion.empty:
        return {},html.Div([dbc.Alert("No se registran datos para este establecimiento", color="danger")])
    
    # Crea el contenedor que se va a enviar según la tab activa
    contenedorOutput = generar_cont_tab_activa(tabsVistasActiva,nombre['NOMBRE'],seleccion,seleccion,'csv/Establecimiento/estdocs.txt','grafico-est')

    data_grafico = generar_data_grafico_dinamico(seleccion,False)
    
    return data_grafico,contenedorOutput
          
@app.callback(
    Output('grafico-est','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-est','data')]
)
def actualizar_grafico_est(tipoGrafico,dataEst):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico (str): Valor del dropdown del tipo de gráfico
        dataEnt (type): Diccionario con la información del establecimiento seleccionado

    Returns:
        html: Contenedor HTML del gráfico a mostrar en la tab de gráfico
    """    
    return generar_grafico_puntajes(dataEst,tipoGrafico)



'''=================CALLBACKS EN SEDE================='''
#Actualiza el dropdown de sede según el establecimiento seleccionado.
@app.callback(
    Output('sedesede', 'options'),
    [Input('estestablmtos', 'value')]
)
def actualizar_sede(sedeest_value):
    """Actualiza el dropdown de sedes según el establecimiento escogido.

    Args:
        sedeest_value (str ): Valor del establecimiento escogido

    Returns:
        list of dict: Lista de sedes según el establecimiento escogido 
    """

    # Se filtra las sedes según el establecimiento escogido y se elimina duplicados porque en el archivo existen las mismas sedes con diferentes jornadas. El atributo que identifica a una sede sin importar su jornada es CODIGO_DANE_SEDE
    sedesCompletoCopy = sedesCompleto[sedesCompleto['COD_DANE']==sedeest_value].drop_duplicates('CODIGO_DANE_SEDE')

    # NOMBRE_x es el nombre de la sede
    sedesedeDropdown = [{'label': sedesCompletoCopy['NOMBRE_x'][i], 'value': sedesCompletoCopy['CODIGO_DANE_SEDE'][i]} for i in sedesCompletoCopy.index]

    return sedesedeDropdown   

@app.callback(
    Output('sedejrnadas','options'),
    [Input('sedesede','value')]
)
def actualizar_jornadas(sedesede_value):
    """Actualiza el dropdown de jornadas dependiendo de la sede escogida. El dropdown tiene 3 posibles opciones: Completa, Mañana y Tarde.

    Args:
        sedesede_value (str): Valor de la sede escogida

    Returns:
        list of dict: Lista de jornadas que tiene la sede escogida
    """    

    sedeLenCopy = sedeLen[sedeLen['CODIGO_DANE_SEDE']==sedesede_value]

    jrnadadropdown = []
    for i in sedeLenCopy.index:
        if sedeLenCopy['JORNADA'][i] == 'M':
            dic = {'label': 'Mañana', 'value': sedeLenCopy['ID_SEDE'][i]}
        elif sedeLenCopy['JORNADA'][i] == 'T':
            dic = {'label': 'Tarde', 'value': sedeLenCopy['ID_SEDE'][i]}
        else:
            dic = {'label': 'Completa', 'value': sedeLenCopy['ID_SEDE'][i]}
        jrnadadropdown.append(dic)
    
    return jrnadadropdown    

@app.callback(
    Output('sedesede','value'),
    [Input('sedesede','options')]
)
def update_dp(sedesede_options):
    """Selecciona la primera sede en el dropdown de sedes después de ser actualizado.

    Args:
        sedesede_options (list of dict): Lista de sedes en el dropdown de sedes

    Returns:
        str: Valor de la primera sede en el dropdown de sedes
    """    
    if sedesede_options != []:
        return sedesede_options[0]['value']

@app.callback(
    Output('sedejrnadas','value'),
    [Input('sedejrnadas','options')]
)
def update_dp(sedejrnadas_options):
    """Selecciona la primera jornada en el dropdown de jornadas después de ser actualizado.

    Args:
        sedejrnadas_options (list of dict): Lista de jornada en el dropdown de jornadas

    Returns:
        str: Valor de la primera jornada en el dropdown de jornadas
    """     
    if sedejrnadas_options != []:    
        return sedejrnadas_options[0]['value']
    

@app.callback(
    Output('data-sede','data'),
    Output('content-tabs-vistas-sede','children'),
    [Input('sedejrnadas', 'value'),
    Input('tabs-comp-sede','active_tab'),
    Input('tabs-vistas-sede','active_tab')]
 )
def actualizar_info_est(sedejrnadas_value,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        sedejrnadas_value (str): Valor de la jornada escogida
        tabsCompActiva (str): Id de la tab de competencias activa
        tabsVistasActiva (str): Id del la tab de vistas activa

    Returns:
        dict: Diccionario con los datos del jornada seleccionada
        html: Contenedor HTML con el children de la tab activa
    """        

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-sede":
        dffCompetencia = sedeLen
    elif tabsCompActiva == "tab-mat-sede":
        dffCompetencia = sedeMat

    seleccion = dffCompetencia[dffCompetencia['ID_SEDE']==sedejrnadas_value]

    nombre = sedesCompleto[sedesCompleto['ID_SEDE']==sedejrnadas_value]

    # Si el establecimiento no presentó la prueba
    if seleccion.empty:
        return {},html.Div([dbc.Alert("No se registran datos para este establecimiento", color="danger")])

    # Crea el contenedor que se va a enviar según la tab activa
    contenedorOutput = generar_cont_tab_activa(tabsVistasActiva,nombre['NOMBRE_x'],seleccion,seleccion,'csv/Sede/sedesdocs.txt','grafico-sede')
          
    data_grafico = generar_data_grafico_dinamico(seleccion,False)
    
    return data_grafico,contenedorOutput

@app.callback(
    Output('grafico-sede','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-sede','data')]
)
def actualizar_grafico_sede(tipoGrafico,dataSede):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico (str): Valor del dropdown del tipo de gráfico
        dataEnt (type): Diccionario con la información de la sede seleccionada

    Returns:
        dict: Diccionario con los datos de la sede seleccionada
        html: Contenedor HTML con el children de la tab activa
    """    
    return generar_grafico_puntajes(dataSede,tipoGrafico)


@app.callback(
    Output('contenedor-valplau','children'),
    [Input('estestablmtos', 'value')]
)
def generarTablaValPlau(est_seleccionado):
    """Actualiza la tabla de Valores Plausibles dependiendo del establecimiento seleccionado

    Args:
        est_seleccionado (str): Valor del establecimiento seleccionado

    Returns:
        html: Contenedor con la información de los valores plausibles del establecimiento seleccionado
    """    

    seleccion = valPlauCompleto[valPlauCompleto['COD_DANE']==est_seleccionado]

    if seleccion.empty:
        return {},html.Div([dbc.Alert("No se registran datos para este establecimiento", color="danger")])

    tablaValPlau = generar_tabla_general(seleccion,'csv/Valores Plausibles/valplaudocs.txt')
    
    return tablaValPlau

@app.callback(
    Output('content-tabs-estudiantes','children'),
    [Input('tabs-estudiantes','active_tab'),
    Input('sedesede','value')]
 )
def actualizar_info_estudiantes(componente,sede_seleccionada):
    """Actualiza la tab de Estudiantes según los componentes elegidos (Académico, Institucional o Socioeconómico) y el filtro por sede.

    Args:
        componente (str): Valor del componente escogido como tab activa
        sede_seleccionada (str): Valor de la sede escogida

    Returns:
        hmtl:  Contenedor HTML con la información por tab de los valores escogidos
    """  

    if componente == 'tab-acad':
        seleccion = estudiantesAcad[estudiantesAcad['cole_cod_dane_sede']==sede_seleccionada]
    elif componente == 'tab-instu': 
        seleccion = estudiantesInstu[estudiantesInstu['cole_cod_dane_sede']==sede_seleccionada]
    else:
        seleccion = estudiantesSocio[estudiantesSocio['cole_cod_dane_sede']==sede_seleccionada]

    # Si no hay datos para mostrar.
    if seleccion.empty:
        return {},html.Div([dbc.Alert("No se registran datos para este establecimiento", color="danger")])

    # Crea el contenedor que se va a enviar según la tab activa
    contenedorOutput = generar_tabla_general(seleccion,'csv/Estudiantes/estudiantesdocs.txt')
        
    return contenedorOutput
    
if __name__=='__main__':        
    app.config.suppress_callback_exceptions = True
    # app.enable_dev_tools(
    #     dev_tools_prune_errors=False
    # )
    app.run_server(debug=True,port=3000)