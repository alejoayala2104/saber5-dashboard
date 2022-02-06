from cProfile import label
from math import pi
from os import sep
from pydoc import classname
from turtle import color
import dash
from dash.html.H1 import H1
from dash.html.H4 import H4
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import numpy
from pandas.core.frame import DataFrame
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import pandasql as ps
import base64
import datetime
import io

from dash import dash_table


#Las siglas de los componentes se ponen dependiendo de 
#la página a la que pertenecen, por ejemplo, si hay un 
#dropdown en la página de departamento que sirva para
#listar los municipios, entonces debería llamarse
#deptoddmpios, donde depto es la página departamentos,
#dd es la sigla de dropdown y mpios es el label del dropdown

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#----------------LECTURA DE ARCHIVOS PLANOS----------------
#-------Zonas---------------
# Lenguaje
zonasLen = pd.read_csv('csv/Zonas/Lenguaje_Grado5_2017_Zonas.csv',sep='|',encoding='utf-8',header=0,decimal='.')
#Matemáticas
zonasMat = pd.read_csv('csv/Zonas/Matematicas_Grado5_2017_Zonas.csv',sep='|',encoding='utf-8',header=0,decimal='.')

deptosZonas = pd.read_csv('csv/deptoszonas.csv',sep='|',encoding='utf-8',header=0,usecols=[1,10])
#-------Departamentos-------
#Lenguaje
deptosLen = pd.read_csv('csv/Departamento/Lenguaje_Grado5_2017_Depto.csv',sep='|',encoding='utf-8',header=0)
#Matemáticas
deptosMat = pd.read_csv('csv/Departamento/Matematicas_Grado5_2017_Depto.csv',sep='|',encoding='utf-8',header=0)

#-------Entidades territoriales-------
enterritorialesCSV = pd.read_csv('csv/entidadesterritoriales.csv',sep='|',encoding='utf-8',header=0,usecols=[0,1,2,3])
#Lenguaje
entLen = pd.read_csv('csv/Entidad Territorial/Lenguaje_Grado5_2017_ETC.csv',sep='|',encoding='utf-8',header=0)
#Matemáticas
entMat = pd.read_csv('csv/Entidad Territorial/Matematicas_Grado5_2017_ETC.csv',sep='|',encoding='utf-8',header=0)

#-------Municipios-------
#Lenguaje
mpioLen = pd.read_csv('csv/Municipios/Lenguaje_Grado5_2017_Municipio.csv',sep='|',encoding='utf-8',header=0)
#Matemáticas
mpioMat = pd.read_csv('csv/Municipios/Matematicas_Grado5_2017_Municipio.csv',sep='|',encoding='utf-8',header=0)

#-------Establecimientos--------
estInfo = pd.read_csv('csv/Establecimiento/Información_Complementaria_2017_EE.csv',sep='|',encoding='utf-8',header=0)
estLen = pd.read_csv('csv/Establecimiento/Lenguaje_Grado5_2017_EE_Completo.csv',sep='|',encoding='utf-8',header=0)
estMat = pd.read_csv('csv/Establecimiento/Matematicas_Grado5_2017_EE_Completo.csv',sep='|',encoding='utf-8',header=0)

#--------Sede---------
sedeInfo = pd.read_csv('csv/Sede/Información_Complementaria_2017_Sede.csv',sep='|',encoding='utf-8',header=0)
sedeLen = pd.read_csv('csv/Sede/Lenguaje_Grado5_2017_Sede.csv',sep='|',encoding='utf-8',header=0)
sedeMat =pd.read_csv('csv/Sede/Matematicas_Grado5_2017_Sede.csv',sep='|',encoding='utf-8',header=0)

#--------Valores Plausibles---------
valPlau = pd.read_csv('csv\Valores Plausibles\ValoresPlausibles_Grado5_2017.csv',sep='|',encoding='utf-8',header=0,nrows=1000)
valPlauDict = valPlau.to_dict('records')
#----------------VARIABLES PARA DROPDOWNS---------------------
#Dp de competencias (global)
compdropdowns=[
                {'label':'Lenguaje', 'value': 'Lenguaje'},
                {'label':'Matemáticas', 'value': 'Matemáticas'}]

#Dp de zonas en departamentos
consultaSQL = """SELECT DISTINCT ZONA FROM deptosZonas """
zonas = ps.sqldf(consultaSQL, locals())
zonasdropdown = [{'label': zonas['ZONA'][i], 'value': zonas['ZONA'][i]} for i in zonas.index]

#Dp de departamentos en departamentos
consultaSQL = """SELECT DISTINCT DEPARTAMENTO FROM deptosZonas """
deptos = ps.sqldf(consultaSQL, locals())
deptosdropdown = [{'label': deptos['DEPARTAMENTO'][i], 'value': deptos['DEPARTAMENTO'][i]} for i in deptos.index] #Forma para generar la lista de diccionarios para el dropdown de Dash

#Dp de zonas en zonas (es diferente porque este tiene todas las zonas, el anterior tiene todos los departamentos)
consultaSQL = """SELECT DISTINCT ZONA FROM zonasLen """
zonaszonas = ps.sqldf(consultaSQL, locals())
zonaszonasdropdown = [{'label': zonaszonas['ZONA'][i], 'value': zonaszonas['ZONA'][i]} for i in zonaszonas.index]

#Dp de Entidades territoriales
consultaSQL = """SELECT DISTINCT ENTIDAD FROM enterritorialesCSV """
enterritoriales = ps.sqldf(consultaSQL, locals())
entdropdown = [{'label': enterritoriales['ENTIDAD'][i], 'value': enterritoriales['ENTIDAD'][i]} for i in enterritoriales.index]

#Dp de departamentos en Municipios
mpioLenCopy = mpioLen[['DEPA_NOMBRE']]
deptosdpenmpios = [{'label': mpioLenCopy['DEPA_NOMBRE'][i], 'value': mpioLenCopy['DEPA_NOMBRE'][i]} for i in mpioLenCopy.index]

#Dp de tipos de Establecimientos educativos
estInfoCopy = estInfo[['NOMBRE','COD_DANE']]
estdropdown = [{'label': estInfoCopy['NOMBRE'][i], 'value': estInfoCopy['COD_DANE'][i]} for i in estInfoCopy.index]

#Dp de jornadas en Sedes
jrndasdropdown=[
                {'label':'Mañana', 'value': 'M'},
                {'label':'Tarde', 'value': 'T'},
                {'label':'Completa', 'value': 'C'}]

#Dp de establecimientos en sedes
sedesTotal = pd.merge(sedeLen,sedeInfo[['ID_SEDE','COD_DANE','NOMBRE']],on='ID_SEDE',how='inner')
sedesTotal = pd.merge(sedesTotal,estInfo[['COD_DANE','NOMBRE']],on='COD_DANE',how='inner')
sedesTotalCopyE = sedesTotal.drop_duplicates('COD_DANE')
estdropdownsedes = [{'label': sedesTotalCopyE['NOMBRE_y'][i], 'value': sedesTotalCopyE['COD_DANE'][i]} for i in sedesTotalCopyE.index]

#Dp de separadores
separadores = [
                {'label':'|', 'value': '|'},
            ]
global separador
global dffPorcentajes
# separador = "|"
#------------DASHBOARD-----------------
menu = html.Div(    
    [
        html.H2("Saber 5", className="display-4"),
        html.Hr(),
        html.P("Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                #exact significa que active=True cuando el pathName sea igual a href
                #href es la ruta que va a tener la página
                dbc.NavLink("Análisis", href="/",active="exact"),
                dbc.NavLink("Departamento", href="/departamento",active="exact"),
                dbc.NavLink("Zona", href="/zona",active="exact"),
                dbc.NavLink("Entidad territorial", href="/entidadter",active="exact"),
                dbc.NavLink("Municipio", href="/municipio",active="exact"),
                dbc.NavLink("Establecimiento", href="/establecimiento",active="exact"),
                dbc.NavLink("Sede", href="/sede",active="exact"),
                dbc.NavLink("Valores plausibles", href="/valplausibles",active="exact"),
            ],
            vertical=True,
            pills=True,  
            className="menu"
        ),   
    ],
    className="contenedor-menu"
)

content = html.Div(id="page-content", children=[],className="contenido-pestana")

app.layout = html.Div([
    dcc.Location(id="url"),
    menu,
    content
])

@app.callback(
    Output("page-content","children"),
    [Input("url","pathname")]
)
#pathname es la direccion de la página, relacionada a href,
#por ejemplo, saber5dashboard.com/departamento, donde 
#/departamento = pathname
def update_contenido_pagina(pathname):
    if pathname == "/":#Si no tiene pathname como tal, se muestra el inicio
        return [
                html.H1('Análisis de datos'),
                html.P('Separador'),
                dcc.Input(
                    id='txfsep',
                    type = "text",
                    placeholder="Ingrese un separador...",                                   
                    size="22",            
                ),  
                html.Hr(id='', className='', children=[]),             
                html.H5(id='h4sep'),
                dcc.Upload(
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
                    # Allow multiple files to be uploaded
                    multiple=True               
                ),                               
                html.Div(id='output-data-upload'),
                html.Div(id='info-atributo'),
        ]
    elif pathname == "/departamento":
        
        # Sirve para guardar los datos que se genera en el callback de creación de la tabla y usarlos en la creación de los gráficos.
        dataDeptos = dcc.Store(id='data-depto', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Departamento'),
        ])

        deptoZonasDropdown = dcc.Dropdown(
            id='deptozonas',
            options=zonasdropdown,
            value='Todos los departamentos',
            placeholder="Elija una zona..."
        )

        deptoDeptoDropdown = dcc.Dropdown(
            id='deptodepto',
            placeholder="Elija un departamento..."
        )

        # Tabs que contiene la tabla y los gráficos.
        tabsVistasDepto = html.Div(id='div-tabs-vistas',children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="Tabla", tab_id="tab-tabla-depto"),
                    dbc.Tab(label="Gráfico", tab_id="tab-grafico-depto"),
                ],
                id="tabs-vistas-depto",
                active_tab="tab-tabla-depto",
            ),
            html.Div(id='content-tabs-vistas-depto'),
        ])

        # Tabs que filtra por compentencia y tiene adentro a tabsVistas
        tabsCompDepto = html.Div(id='div-tabs-comp',children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="Lenguaje", tab_id="tab-len-depto"),
                    dbc.Tab(label="Matemáticas", tab_id="tab-mat-depto"),
                ],
                id="tabs-comp-depto",
                active_tab="tab-len-depto",
            ),
            html.Div(id='content-tabs-comp-depto', children=tabsVistasDepto),
        ])

        return html.Div([
            dataDeptos,
            header,
            deptoZonasDropdown,
            deptoDeptoDropdown,
            tabsCompDepto
        ])
        
    elif pathname == "/zona":

        # Sirve para guardar los datos que se genera en el callback de creación de la tabla y usarlos en la creación de los gráficos.
        dataZona = dcc.Store(id='data-zona', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Zona'),
        ])

        zonasZonasDropdown = dcc.Dropdown(
            id='zonaszonas',
            options=zonaszonasdropdown,
            value='Todas las zonas',
            placeholder="Elija una zona..."
        )

        # Tabs que contiene la tabla y los gráficos.
        tabsVistasZona = html.Div(id='div-tabs-vistas',children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="Tabla", tab_id="tab-tabla-zona"),
                    dbc.Tab(label="Gráfico", tab_id="tab-grafico-zona"),
                ],
                id="tabs-vistas-zona",
                active_tab="tab-tabla-zona",
            ),
            html.Div(id='content-tabs-vistas-zona'),
        ])

        # Tabs que filtra por compentencia y tiene adentro a tabsVistas
        tabsCompZona = html.Div(id='div-tabs-comp',children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="Lenguaje", tab_id="tab-len-zona"),
                    dbc.Tab(label="Matemáticas", tab_id="tab-mat-zona"),
                ],
                id="tabs-comp-zona",
                active_tab="tab-len-zona",
            ),
            html.Div(id='content-tabs-comp-zona', children=tabsVistasZona),
        ])
        return [
            dataZona,
            header,
            zonasZonasDropdown,
            tabsCompZona
        ]
    elif pathname == "/entidadter":
        return [
                html.H1('Entidad Territorial'),
                dcc.Dropdown(
                    id='etdropdown',
                    options=entdropdown,
                    value='Amazonas',
                    placeholder="Elija una entidad territorial..."
                ),
                dcc.Dropdown(
                    id='entcomp',
                    options=compdropdowns,
                    value='Lenguaje',
                    placeholder='Seleccione una competencia...'
                ),                
                html.Div([ #Lo que se muestra al seleccionar la ent.            
                html.H1(id='h1Ent', className='', children=''),
                html.Div(id='divInfoEnt', className='', children=[]),
                dcc.Graph(id='barEnt'),
                dcc.Graph(id='pieEnt'),
                dcc.Graph(id='lineEnt')
                ])
        ]
    elif pathname == "/municipio":
        return [
                html.H1('Municipio'),
                dcc.Dropdown(
                    id='mpiodddepto',
                    options=deptosdpenmpios,
                    value='Antioquia',
                    placeholder="Elija un departamento..."
                ),
                dcc.Dropdown(
                    id='mpioddmpio',                    
                    placeholder="Elija un municipio..."
                ),                
                dcc.Dropdown(
                    id='mpiocomp',
                    options=compdropdowns,
                    value='Lenguaje',
                    placeholder='Seleccione una competencia...'
                ),                
                html.Div([ #Lo que se muestra al seleccionar la ent.            
                html.H1(id='h1Mpio', className='', children=''),
                html.Div(id='divInfoMpio', className='', children=[]),
                dcc.Graph(id='barMpio'),
                dcc.Graph(id='pieMpio'),
                dcc.Graph(id='lineMpio')
                ])
        ]
    elif pathname == "/establecimiento":
        return [
                html.H1('Establecimiento'),
                dcc.Dropdown(
                    id='estestablmtos',
                    options=estdropdown,
                    placeholder="Elija un establecimiento..."
                ),
                dcc.Dropdown(
                    id='estcomp',
                    options=compdropdowns,
                    value='Lenguaje',
                    placeholder="Elija una competencia..."
                ),
                html.Div([ #Lo que se muestra al seleccionar el establecimiento.            
                html.H1(id='h1Est', className='', children=''),
                html.Div(id='divInfoEst', className='', children=[]),
                dcc.Graph(id='barEst'),
                dcc.Graph(id='pieEst'),
                dcc.Graph(id='lineEst')
                ])
        ]
    elif pathname == "/sede":
        return [
                html.H1('Sede'),
                dcc.Dropdown(
                    id='sedeestablmtos',
                    options=estdropdownsedes,
                    placeholder="Elija un establecimiento..."
                ),
                dcc.Dropdown(
                    id='sedesede',
                    placeholder="Elija una sede..."
                ),
                dcc.Dropdown(
                    id='sedejrnadas',
                    options=jrndasdropdown,
                    placeholder="Elija una jornada..."
                ),
                dcc.Dropdown(
                    id='sedecomp',
                    options=compdropdowns,
                    value='Lenguaje',
                    placeholder="Elija una competencia..."
                ),
                html.Div([ #Lo que se muestra al seleccionar la sede.            
                html.H1(id='h1Sede', className='', children=''),
                html.Div(id='divInfoSede', className='', children=[]),
                dcc.Graph(id='barSede'),
                dcc.Graph(id='pieSede'),
                dcc.Graph(id='lineSede')
                ])
        ]
    elif pathname == "/valplausibles":
        return [
                html.H1('Valores plausibles'),
                html.Br(id='', className='', children=[]),
                dash_table.DataTable(
                    id='valplautable',
                    columns= [
                        {"name": i, "id": i}
                        for i in valPlau.columns
                    ],
                    data= valPlauDict,
                    filter_action= "native",
                    sort_action="native",
                    sort_mode="multi",
                    page_size=10,
                    style_data={
                        'whitespace':'normal',
                        'height': 'auto'
                    },
                    virtualization=True
                )               
        ]
    #If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



#------------------------FUNCIONES GENERALES----------------------------
# Crea un contenedor con una tabla y su información general, o un contenedor con gráficos, dependiendo de la tab activa que reciba como parámetro.
def contenedorSegunTabActiva(valueDropdown,seleccion,tablaData,tabsVistasActiva,idGrafico):

    # Retorna el contenedor correspondiente a la tab seleccionada.
    if tabsVistasActiva == 'tab-tabla':

        # Se crea un div con la información general del dataset y una tabla mostrando su contenido.
        contenedorTabla = html.Div([
            html.H2(children=valueDropdown),
            html.Div([
                html.Hr(),
                html.P('Número de participantes: ' + str(*seleccion['N'].values)),
                html.P('Puntaje promedio: ' + str(*seleccion['PUNTAJE_PROMEDIO'].values)),
                html.P('Desviación: ' + str(*seleccion['DESVIACION'].values))
            ]),

            # Creación de la tabla con el dataframe de la competencia escogida.
            dash_table.DataTable(
                id = 'tabla-info',
                data=tablaData.to_dict('records'),
                columns=[{'name': i, 'id': i,"selectable": True} for i in tablaData.columns],
                sort_action="native",
                sort_mode="multi",
                fixed_rows={'headers': True},
                page_size=10, 
                style_cell={
                    'minWidth': 250, 'maxWidth': 250, 'width': 250
                },
            ),
        ])

        return contenedorTabla        
    elif tabsVistasActiva == 'tab-grafico':

        # Se crea el div con el dropdown del tipo de gráfico y el gráfico como componente vacío.
        contenedorGraficos =html.Div([
            html.H2(id='', className='', children='Grafico'),

            # Dropdown para elegir el tipo de gráfico
            dcc.Dropdown(id='dropdown-graficos',
                options=[
                    {'label':'Dona', 'value': 'Dona'},
                    {'label':'Barras', 'value': 'Barras'},
                    {'label':'Linea', 'value': 'Linea'}],
                value='Dona',
            ),
            dcc.Graph(
                id=idGrafico,
                figure={},
            )
        ])
        
        return contenedorGraficos

    
#ajusta el DataFrame recibido para que el gráfico lo entienda. Posteriomente, dicho DataFrame se transforma en dict para cumplir el requerimiento de envío entre callbacks de dcc.Store.
def generarDataParaGrafico(seleccion):
    
    dffPorcentajes = seleccion.filter(like="PORCENTAJE").transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)
    dffPorcentajesDict = dffPorcentajes.to_dict('records')

    return dffPorcentajesDict

#---------------CALLBACKS EN DEPARTAMENTOS------------#
#Actualiza los departamentos según la zona seleccionada.
@app.callback(
    Output(component_id='deptodepto', component_property='options'),
    [Input(component_id='deptozonas', component_property='value')]
)
def update_dp(zona_seleccionada):
    deptosZonasCopy = deptosZonas[deptosZonas['ZONA']==zona_seleccionada]
    deptosdropdown = [{'label': deptosZonasCopy['DEPARTAMENTO'][i], 'value': deptosZonasCopy['DEPARTAMENTO'][i]} for i in deptosZonasCopy.index]
    return deptosdropdown
    
#Actualiza las opciones del dropdown de departamentos (en zonas).
@app.callback(
    dash.dependencies.Output('deptodepto', 'value'),
    [dash.dependencies.Input('deptodepto', 'options')])
def update_dp(deptodepto_options):
    return deptodepto_options[0]['value']
 
# Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.
# Recibe como input el dropdown del departamento seleccionado y la tab activa de tabs comp. También recibe la tab activa de tabs vista.
@app.callback(
    Output('data-depto','data'),
    Output('content-tabs-vistas-depto','children'),
    [Input(component_id='deptodepto', component_property='value'),
    Input('tabs-comp-depto','active_tab'),
    Input('tabs-vistas-depto','active_tab')]
 )
def actualizar_info_depto(deptodepto,tabsCompActiva,tabsVistasActiva):

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-depto":
        dffdeptos = deptosLen
    elif tabsCompActiva == "tab-mat-depto":
        dffdeptos = deptosMat

    # Filtra según el departamento escogido
    seleccion = dffdeptos[dffdeptos['DEPARTAMENTO']==deptodepto] 

    # Si se elige todos los departamentos, en la tabla se muestran todos los departamentos.
    if 'Todos los departamentos'==deptodepto:
        tablaData = dffdeptos
    else:
        tablaData = seleccion

    # Crea el contenedor que se va a enviar según la tab activa
    if tabsVistasActiva == 'tab-tabla-depto':
        contenedorOutput = contenedorSegunTabActiva(deptodepto,seleccion,tablaData,'tab-tabla','grafico-depto')
    elif tabsVistasActiva == 'tab-grafico-depto':
        contenedorOutput = contenedorSegunTabActiva(deptodepto,seleccion,tablaData,'tab-grafico','grafico-depto')   

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generarDataParaGrafico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-depto','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-depto','data')]
)
# Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store
def actualizar_grafico_depto(tipoGrafico,dataDeptos):
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataDeptos)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
        # figure.update_layout(showlegend=False) #Esconder el label de X
        figure.update_xaxes(visible=False) #Esconder los valores de X
    
    elif tipoGrafico == 'Dona':
        figure = px.pie(
            data_frame=dffPorcentajes,
            names ='RENDIMIENTO',
            values = 'PORCENTAJE',
            hole=.3
        )
    else:
        figure = px.line(
            data_frame=dffPorcentajes,
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
        )
    
    return figure

#---------------CALLBACKS EN ZONA---------------------------#
# Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.
# Recibe como input el dropdown del departamento seleccionado y la tab activa de tabs comp. También recibe la tab activa de tabs vista.
@app.callback(
    Output('data-zona','data'),
    Output('content-tabs-vistas-zona','children'),
    [Input('zonaszonas', 'value'),
    Input('tabs-comp-zona','active_tab'),
    Input('tabs-vistas-zona','active_tab')]
 )
def actualizar_info_zona(zonaszonas,tabsCompActiva,tabsVistasActiva):

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-zona":
        dffdeptos = zonasLen
    elif tabsCompActiva == "tab-mat-zona":
        dffdeptos = zonasMat

    # Filtra según el departamento escogido
    seleccion = dffdeptos[dffdeptos['ZONA']==zonaszonas] 

    # Si se elige todos los departamentos, en la tabla se muestran todos los departamentos.
    if 'Todas las zonas'==zonaszonas:
        tablaData = dffdeptos
    else:
        tablaData = seleccion
    
    # Crea el contenedor que se va a enviar según la tab activa
    if tabsVistasActiva == 'tab-tabla-zona':
        contenedorOutput = contenedorSegunTabActiva(zonaszonas,seleccion,tablaData,'tab-tabla','grafico-zona')
    elif tabsVistasActiva == 'tab-grafico-zona':
        contenedorOutput = contenedorSegunTabActiva(zonaszonas,seleccion,tablaData,'tab-grafico','grafico-zona')    

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generarDataParaGrafico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-zona','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-zona','data')]
)
# Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store
def actualizar_grafico_zona(tipoGrafico,dataDeptos):
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataDeptos)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
        # figure.update_layout(showlegend=False) #Esconder el label de X
        figure.update_xaxes(visible=False) #Esconder los valores de X
    
    elif tipoGrafico == 'Dona':
        figure = px.pie(
            data_frame=dffPorcentajes,
            names ='RENDIMIENTO',
            values = 'PORCENTAJE',
            hole=.3
        )
    else:
        figure = px.line(
            data_frame=dffPorcentajes,
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
        )
    
    return figure

#---------------CALLBACKS EN ENTIDAD TERRITORIAL------------#
#Actualiza los gráficos según el departamento seleccionado.
@app.callback(
    Output(component_id='h1Ent', component_property='children'),
    Output(component_id='divInfoEnt', component_property='children'),
    Output(component_id='barEnt', component_property='figure'),
    Output(component_id='pieEnt', component_property='figure'),
    Output(component_id='lineEnt', component_property='figure'),
    [Input(component_id='etdropdown', component_property='value'),
    Input(component_id='entcomp', component_property='value')]
)
def update_graphEnt(etdropdown,entcomp):

    #Copia del dataframe dependiendo de lo que se elija.
    if entcomp == 'Matemáticas':
        dffent = entMat
    else:
        dffent = entLen
   
    selEnt = dffent[dffent['ENTIDAD']==etdropdown] #Se filtra por ENTIDAD
    h1 = html.H2(etdropdown)
       
    div = html.Div([
        html.Hr(),
        html.H3('Número de participantes: ' + str(*selEnt['N'].values)),
        html.H3('Puntaje promedio: ' + str(*selEnt['PUNTAJE_PROMEDIO'].values)),
        html.H3('Desviación: ' + str(*selEnt['DESVIACION'].values))
    ])

    #Se ajusta el dataframe para los gráficos     
    dffPorcentajes = selEnt.filter(like="PORCENTAJE").transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)
    
    #Se configura los gráficos
    barDepto = px.bar(
        data_frame=dffPorcentajes,      
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )
    pieDepto = px.pie(
        data_frame=dffPorcentajes,
        names ='RENDIMIENTO',
        values = 'PORCENTAJE',
        hole=.3
    )
    lineDepto = px.line(
        data_frame=dffPorcentajes,
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )

    return (h1,div,barDepto,pieDepto,lineDepto)


#---------------CALLBACKS EN MUNICIPIOS------------#
#Actualiza los municipios según el departamento seleccionado.
@app.callback(
    Output(component_id='mpioddmpio', component_property='options'),
    [Input(component_id='mpiodddepto', component_property='value')]
)
def update_dp(depto_seleccionado):    
    mpioLenCopyM = mpioLen[mpioLen['DEPA_NOMBRE']==depto_seleccionado] #Si se seleccionó
    mpiosdropdown = [{'label': mpioLenCopyM['MUNI_NOMBRE'][i], 'value': mpioLenCopyM['MUNI_NOMBRE'][i]} for i in mpioLenCopyM.index]
    return mpiosdropdown

#Callback que actualiza las opciones del dropdown de municipios (en departamentos).
@app.callback(
    dash.dependencies.Output('mpiodddepto', 'value'),
    [dash.dependencies.Input('mpiodddepto', 'options')])
def update_dp(mpioddmpio_options):
    return mpioddmpio_options[0]['value']

#Callback que actualiza las opciones del dropdown de municipios (en departamentos).
@app.callback(
    dash.dependencies.Output('mpioddmpio', 'value'),
    [dash.dependencies.Input('mpioddmpio', 'options')])
def update_dp(mpioddmpio_options):
    return mpioddmpio_options[0]['value']

#Actualiza los gráficos según el departamento seleccionado.
@app.callback(
    Output(component_id='h1Mpio', component_property='children'),
    Output(component_id='divInfoMpio', component_property='children'),
    Output(component_id='barMpio', component_property='figure'),
    Output(component_id='pieMpio', component_property='figure'),
    Output(component_id='lineMpio', component_property='figure'),
    [Input(component_id='mpiodddepto', component_property='value'),
    Input(component_id='mpioddmpio', component_property='value'),
    Input(component_id='mpiocomp', component_property='value')]
)
def update_graphMpios(mpiodddepto,mpioddmpio,mpiocomp):

    #Copia del dataframe dependiendo de lo que se elija.
    if mpiocomp == 'Matemáticas':
        dffmpios = mpioMat
    else:
        dffmpios = mpioLen
   
    #Se filtra por municipio y departamento      
    selMpio = dffmpios[(dffmpios['MUNI_NOMBRE']==mpioddmpio) & (dffmpios['DEPA_NOMBRE']==mpiodddepto)] #Si se seleccionó
    
    if selMpio.empty: #Si no encuentra valores de dicho municipio.
        return dashboard_vacio()
    
    h1 = html.H2(mpioddmpio)        
    div = html.Div([
        html.Hr(),
        html.H3('Número de participantes: ' + str(*selMpio['N'].values)),
        html.H3('Puntaje promedio: ' + str(*selMpio['PUNTAJE_PROMEDIO'].values)),
        html.H3('Desviación: ' + str(*selMpio['DESVIACION'].values))
    ])

    #Se ajusta el dataframe para los gráficos     
    dffPorcentajes = selMpio.filter(like="PORCENTAJE").transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)
    
    #Se configura los gráficos
    barMpio = px.bar(
        data_frame=dffPorcentajes,      
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )
    pieMpio = px.pie(
        data_frame=dffPorcentajes,
        names ='RENDIMIENTO',
        values = 'PORCENTAJE',
        hole=.3
    )
    lineMpio = px.line(
        data_frame=dffPorcentajes,
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )

    return (h1,div,barMpio,pieMpio,lineMpio)


#--------------------CALLBACKS EN ESTABLECIMIENTOS--------------
#Selecciona el primero del dropdown de establecimientos
@app.callback(
    dash.dependencies.Output('estestablmtos', 'value'),
    [dash.dependencies.Input('estestablmtos', 'options')])
def update_dp(deptodepto_options):
    return deptodepto_options[0]['value']

#Actualiza los gráficos según el establecimiento seleccionado.
@app.callback(
    Output(component_id='h1Est', component_property='children'),
    Output(component_id='divInfoEst', component_property='children'),
    Output(component_id='barEst', component_property='figure'),
    Output(component_id='pieEst', component_property='figure'),
    Output(component_id='lineEst', component_property='figure'),
    [Input(component_id='estestablmtos', component_property='value'),    
    Input(component_id='estcomp', component_property='value')]
)
def update_graphEst(estestablmtos,estcomp):
    #Copia del dataframe dependiendo de lo que se elija.
    if estcomp == 'Matemáticas':
        dffest = estMat
    else:
        dffest = estLen   
         
    selEst = dffest[dffest['COD_DANE']==estestablmtos] #Si se seleccionó
     
    h1 = html.H2()
    div = html.Div([
        html.Hr(),
        html.H3('Código DANE: ' + str(*selEst['COD_DANE'].values)),
        html.H3('Número de participantes: ' + str(*selEst['PARTICIPANTES'].values)),
        html.H3('Puntaje promedio: ' + str(*selEst['PROMEDIO'].values)),
        html.H3('Desviación: ' + str(*selEst['DESVIACION'].values))
    ])

    #Se ajusta el dataframe para los gráficos     
    dffPorcentajes = selEst.filter(["INSUFICIENTE","MINIMO","SATISFACTORIO","AVANZADO"]).transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)
    #Se configura los gráficos
    barEst = px.bar(
        data_frame=dffPorcentajes,      
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )
    pieEst = px.pie(
        data_frame=dffPorcentajes,
        names ='RENDIMIENTO',
        values = 'PORCENTAJE',
        hole=.3
    )
    lineEst = px.line(
        data_frame=dffPorcentajes,
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )

    return (h1,div,barEst,pieEst,lineEst)

#-------------CALLBACKS EN SEDE---------------
#Actualiza el dropdown de sede según el establecimiento seleccionado.
@app.callback(
    Output(component_id='sedesede', component_property='options'),
    [Input(component_id='sedeestablmtos', component_property='value')]
)
def update_dp(est_seleccionado):
    #Filtra aquellos que tengan el codigo dane del establecimiento seleccionado,
    #y elimina repetidos porque todas las jornadas tienen el mismo codigo dane.
    sedesTotalCopyS = sedesTotal[sedesTotal['COD_DANE']==est_seleccionado].drop_duplicates('CODIGO_DANE_SEDE')    
    #NOMBRE_x es el nombre de la sede y se pone como valor de cada opción el CODIGO_DANE_SEDE
    sededropdown = [{'label': sedesTotalCopyS['NOMBRE_x'][i], 'value': sedesTotalCopyS['CODIGO_DANE_SEDE'][i]} for i in sedesTotalCopyS.index]
    return sededropdown

#Actualiza el dropdown de jornada según la sede seleccionada.
@app.callback(
    Output(component_id='sedejrnadas', component_property='options'),
    [Input(component_id='sedesede', component_property='value')]
)
def update_dp(sede_seleccionada):
    #Filtra la sede según el CODIGO_DANE_SEDE seleccionado
    sedesTotalCopyJ = sedesTotal[sedesTotal['CODIGO_DANE_SEDE']==sede_seleccionada]
    #Se asocia que cada jornada tiene su propio ID_SEDE, entonces aquel se elige como valor
    #para conectar los gráficos con el csv.
    # jrnadadropdown = [{'label': sedesTotalCopyJ['JORNADA'][i], 'value': sedesTotalCopyJ['ID_SEDE'][i]} for i in sedesTotalCopyJ.index]
    jrnadadropdown = []
    for i in sedesTotalCopyJ.index:
        if sedesTotalCopyJ['JORNADA'][i] == 'M':
            dic = {'label': 'Mañana', 'value': sedesTotalCopyJ['ID_SEDE'][i]}
        elif sedesTotalCopyJ['JORNADA'][i] == 'T':
            dic = {'label': 'Tarde', 'value': sedesTotalCopyJ['ID_SEDE'][i]}
        else:
            dic = {'label': 'Completa', 'value': sedesTotalCopyJ['ID_SEDE'][i]}
        jrnadadropdown.append(dic)
    return jrnadadropdown


#Selecciona el primero del dropdown de establecimientos en Sede
@app.callback(
    dash.dependencies.Output('sedeestablmtos', 'value'),
    [dash.dependencies.Input('sedeestablmtos', 'options')])
def update_dp(deptodepto_options):
    return deptodepto_options[0]['value']

#Selecciona el primero del dropdown de sedes en Sede
@app.callback(
    dash.dependencies.Output('sedesede', 'value'),
    [dash.dependencies.Input('sedesede', 'options')])
def update_dp(deptodepto_options):
    return deptodepto_options[0]['value']

#Selecciona el primero del dropdown de jornadas en Sede
@app.callback(
    dash.dependencies.Output('sedejrnadas', 'value'),
    [dash.dependencies.Input('sedejrnadas', 'options')])
def update_dp(deptodepto_options):
    return deptodepto_options[0]['value']

#Actualiza los gráficos según el establecimiento seleccionado.
@app.callback(
    Output(component_id='h1Sede', component_property='children'),
    Output(component_id='divInfoSede', component_property='children'),
    Output(component_id='barSede', component_property='figure'),
    Output(component_id='pieSede', component_property='figure'),
    Output(component_id='lineSede', component_property='figure'),
    [Input(component_id='sedejrnadas', component_property='value'),   
    Input(component_id='sedecomp', component_property='value')]
)
#sedejrnadas tiene el ID_SEDE, porque dependiendo de la jornada, el id de la sede cambia.
def update_graphSede(sedejrnadas,sedecomp):
    #Copia del dataframe dependiendo de lo que se elija.
    if sedecomp == 'Matemáticas':
        dffsede = sedeMat
    else:
        dffsede = sedeLen   
    selSede = dffsede[dffsede['ID_SEDE']==sedejrnadas] #Si se seleccionó
    
    if selSede.empty:
        h1 = html.H2("")
        div = html.Div([
            html.Hr(),
            html.H3("La sede seleccionada no tiene registros para dicha jornada")
        ])
        barSede = px.bar()
        pieSede = px.pie()
        lineSede = px.line()

        return (h1,div,barSede,pieSede,lineSede)
    h1 = html.H2("")
    div = html.Div([
        html.Hr(),
        html.H3('Código DANE: ' + str(*selSede['CODIGO_DANE_SEDE'].values)),
        html.H3('Número de participantes: ' + str(*selSede['PARTICIPANTES'].values)),
    ])

    #Se ajusta el dataframe para los gráficos     
    dffPorcentajes = selSede.filter(["INSUFICIENTE","MINIMO","SATISFACTORIO","AVANZADO"]).transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)
    #Se configura los gráficos
    barSede = px.bar(
        data_frame=dffPorcentajes,      
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )
    pieSede = px.pie(
        data_frame=dffPorcentajes,
        names ='RENDIMIENTO',
        values = 'PORCENTAJE',
        hole=.3
    )
    lineSede = px.line(
        data_frame=dffPorcentajes,
        x = 'RENDIMIENTO',
        y = 'PORCENTAJE',
    )

    return (h1,div,barSede,pieSede,lineSede)


#------------CALL BACKS INICIO-----------------------
#Actualiza el div de la tabla.
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              Input('txfsep', 'value'),)
def update_output(list_of_contents, list_of_names, list_of_sep):
    if not list_of_sep:
        list_of_sep = "|"
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, s) for c, n, s in
            zip(list_of_contents, list_of_names, list_of_sep)]
        return children

#Selecciona el atributo de la tabla y muestra su info
@app.callback(Output('info-atributo','children'),             
              Input('datatable-main','selected_columns'))
def actualizar_info_atributo(selected_columns):
    copiadf= df
    nulos = ""
    moda = ""
    distintos = ""
    tipoDato = ""
    promedio = "No es valor numérico"
    mediana = "No es valor numérico"
    max = "No es valor numérico"
    min = "No es valor numérico"
    if selected_columns:
        nulos =  copiadf[selected_columns[0]].isna().sum()
        modadf = copiadf[selected_columns[0]].mode() #Devuelve una Series
        if not modadf.empty: moda = modadf[0]
        distintos = copiadf[selected_columns[0]].nunique()
        tipoDato = copiadf[selected_columns[0]].dtypes        
        if tipoDato == numpy.int64:
            promedio = copiadf[selected_columns[0]].mean()
            mediana = copiadf[selected_columns[0]].median()
            max = copiadf[selected_columns[0]].max()
            min = copiadf[selected_columns[0]].min()

    children = [ #Este es el html Div que se retorna a info-atributo       
        html.Div([
            html.H6(["Count: {}".format(len(str(copiadf.index)))]),
            html.H6(["Nulos: {}".format(str(nulos))]),
            html.H6(["Distintos: {}".format(str(distintos))]),
            html.H6(["Tipo de dato: {}".format(str(tipoDato))]),
            html.H6(["Moda: {}".format(str(moda))]),
            html.H6(["Promedio: {}".format(str(promedio))]),
            html.H6(["Mediana: {}".format(str(mediana))]),
            html.H6(["Máximo: {}".format(str(max))]),
            html.H6(["Mínimo: {}".format(str(min))]),
        ]),
                
    ]
    return children


# Función para lectura de archivos    
def parse_contents(contents, filename, sepr):
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
        print(e)
        return html.Div([
            'No se pudo cargar el archivo.'
        ])

    return html.Div([
        # count_row = df.shape[0]  # Gives number of rows
        # count_col = df.shape[1]  # Gives number of columns
        # html.Div('Count: ' + str(df.shape[0])), #Numero de registros

        dash_table.DataTable(
            id = 'datatable-main',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i,"selectable": True} for i in df.columns],
            column_selectable="single",  # allow users to select 'multi' or 'single' columns            
            selected_columns=[],        # ids of columns that user selects            
            filter_action= "native",
            sort_action="native",
            sort_mode="multi",
            page_current= 0,
            page_size= 10,
            style_data={
                'whitespace':'normal',
            },            
            virtualization=True
        ),
  
        html.Hr(),  # horizontal line
    ])

#Actualiza el separador
@app.callback(Output('h4sep', 'children'),
              Input('txfsep', 'value'))
def update_sep(txfsep):
    if not txfsep:
        separador = "'|' (por defecto)"       
    else:
        separador = str(txfsep)

    return html.H6(id='', className='', children='Separador = ' + separador),


#Utilidades
#Función que retorna elementos html comunes pero vacíos.
def dashboard_vacio():
    h1 = html.H2("")
    div = html.Div([
        html.Hr(),
        html.H3("La selección no tiene valores en el registro.")
    ])
    bar = px.bar()
    pie = px.pie()
    line = px.line()

    return (h1,div,bar,pie,line)

def quitar_tildes(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


if __name__=='__main__':        
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True, port=3000)
