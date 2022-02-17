from unicodedata import decimal
import dash
import dash_bootstrap_components as dbc
from dash import html,dcc,dash_table
import numpy
from pandas.core.frame import DataFrame
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import pandasql as ps
import base64
import io

# Se utilizan elementos BOOSTRAP, pero al existir la carpeta assets con un archivo css, automáticamente el programa añade y sigue esa hoja de estilos en conjunto con los elementos de BOOSTRAP.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

'''=================LECTURA DE ARCHIVOS PLANOS================='''

'''--------------Zonas--------------'''
# Lenguaje
zonasLen = pd.read_csv('csv/Zonas/Lenguaje_Grado5_2017_Zonas.csv',sep='|',encoding='utf-8',header=0,decimal='.')
# Matemáticas
zonasMat = pd.read_csv('csv/Zonas/Matematicas_Grado5_2017_Zonas.csv',sep='|',encoding='utf-8',header=0,decimal='.')
# Tiene 'Todos los departamentos'. Se usa para generar los dropdowns en Departamentos.
deptosZonas = pd.read_csv('csv/deptoszonas.csv',sep='|',encoding='utf-8',header=0,usecols=[1,10])

'''--------------Departamentos--------------'''
# Lenguaje
deptosLen = pd.read_csv('csv/Departamento/Lenguaje_Grado5_2017_Depto.csv',sep='|',encoding='utf-8',header=0)
# Matemáticas
deptosMat = pd.read_csv('csv/Departamento/Matematicas_Grado5_2017_Depto.csv',sep='|',encoding='utf-8',header=0)

'''--------------Entidades territoriales--------------'''
# Se utiliza para generar el dropdown de entidades territoriales.
enterritorialesCSV = pd.read_csv('csv/entidadesterritoriales.csv',sep='|',encoding='utf-8',header=0,usecols=[0,1,2,3])
# Lenguaje
entLen = pd.read_csv('csv/Entidad Territorial/Lenguaje_Grado5_2017_ETC.csv',sep='|',encoding='utf-8',header=0)
# Matemáticas
entMat = pd.read_csv('csv/Entidad Territorial/Matematicas_Grado5_2017_ETC.csv',sep='|',encoding='utf-8',header=0)

'''--------------Municipios--------------'''
# Lenguaje
mpioLen = pd.read_csv('csv/Municipios/Lenguaje_Grado5_2017_Municipio.csv',sep='|',encoding='utf-8',header=0,decimal='.')
# Matemáticas
mpioMat = pd.read_csv('csv/Municipios/Matematicas_Grado5_2017_Municipio.csv',sep='|',encoding='utf-8',header=0,decimal='.')

'''--------------Establecimientos--------------'''
# Se utiliza el csv de lenguaje municipios para poder conectar el id del municipio con el departamento y el cod dane del establecimiento
estMpios = pd.read_csv('csv/Establecimiento/Lenguaje_Grado5_2017_Municipio.csv',sep='|',encoding='utf-8',header=0, decimal=',')
# Se utiliza para generar el dropdown de Establecimientos.
estInfo = pd.read_csv('csv/Establecimiento/Información_Complementaria_2017_EE.csv',sep='|',encoding='utf-8',header=0)
# Lenguaje
estLen = pd.read_csv('csv/Establecimiento/Lenguaje_Grado5_2017_EE_Completo.csv',sep='|',encoding='utf-8',header=0)
# Matemáticas
estMat = pd.read_csv('csv/Establecimiento/Matematicas_Grado5_2017_EE_Completo.csv',sep='|',encoding='utf-8',header=0)

'''--------------Sede--------------'''
# Se utiliza para generar los dropdown de Sede.
sedeInfo = pd.read_csv('csv/Sede/Información_Complementaria_2017_Sede.csv',sep='|',encoding='utf-8',header=0)
# Lenguaje
sedeLen = pd.read_csv('csv/Sede/Lenguaje_Grado5_2017_Sede.csv',sep='|',encoding='utf-8',header=0)
# Matemáticas
sedeMat =pd.read_csv('csv/Sede/Matematicas_Grado5_2017_Sede.csv',sep='|',encoding='utf-8',header=0)

'''--------------Valores plausibles--------------'''
valPlau = pd.read_csv('csv\Valores Plausibles\ValoresPlausibles_Grado5_2017.csv',sep='|',encoding='utf-8',header=0,nrows=1000)
valPlauDict = valPlau.to_dict('records')


'''=================VARIABLES PARA DROPDOWNS================='''
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
deptosdropdown = [{'label': deptos['DEPARTAMENTO'][i], 'value': deptos['DEPARTAMENTO'][i]} for i in deptos.index]

#Dp de zonas en zonas (es diferente porque este tiene 'Todas las zonas', el anterior tiene 'Todos los departamentos')
consultaSQL = """SELECT DISTINCT ZONA FROM zonasLen """
zonaszonas = ps.sqldf(consultaSQL, locals())
zonaszonasdropdown = [{'label': zonaszonas['ZONA'][i], 'value': zonaszonas['ZONA'][i]} for i in zonaszonas.index]

#Dp de Entidades territoriales
consultaSQL = """SELECT DISTINCT ENTIDAD FROM enterritorialesCSV """
enterritoriales = ps.sqldf(consultaSQL, locals())
entdropdown = [{'label': enterritoriales['ENTIDAD'][i], 'value': enterritoriales['ENTIDAD'][i]} for i in enterritoriales.index]
#Dp de Tipo de entidades territoriales
tipoentdropdown=[    
                {'label':'Todas las entidades territoriales', 'value': '-1'},
                {'label':'Departamento', 'value': '0'},
                {'label':'Etc', 'value': '1'},
                {'label':'Municipio', 'value': '2'}]
                
#Dp de departamentos en Municipios (el dp de departamentos en municipios es el mismo que el de departamentos)
mpioLenCopy = mpioLen[['DEPA_NOMBRE']].drop_duplicates()
deptosdpenmpios = [{'label': mpioLenCopy['DEPA_NOMBRE'][i], 'value': mpioLenCopy['DEPA_NOMBRE'][i]} for i in mpioLenCopy.index]

#Dp de departamentos en 'Establecimiento'
estMpiosCopy = estMpios[['DEPA_NOMBRE']].drop_duplicates()
estDeptosDropdown = [{'label': estMpiosCopy['DEPA_NOMBRE'][i], 'value': estMpiosCopy['DEPA_NOMBRE'][i]} for i in estMpiosCopy.index]

#Dp de tipos de Establecimientos educativos
estInfoCopy = estInfo[['COD_DANE','MUNI_ID','NOMBRE']]
# estdropdown = [{'label': estInfoCopy['NOMBRE'][i], 'value': estInfoCopy['COD_DANE'][i]} for i in estInfoCopy.index]

#Dp de jornadas en Sedes
jrndasdropdown=[
                {'label':'Mañana', 'value': 'M'},
                {'label':'Tarde', 'value': 'T'},
                {'label':'Completa', 'value': 'C'}]

#Dp de establecimientos en sedes
sedesTotal = pd.merge(sedeLen,sedeInfo[['ID_SEDE','COD_DANE','NOMBRE']],on='ID_SEDE',how='inner')
sedesTotal = pd.merge(sedesTotal,estInfo[['COD_DANE','NOMBRE']],on='COD_DANE',how='inner')
sedesTotalCopyE = sedesTotal.drop_duplicates('COD_DANE')

#Se mezclan los csv de: sedeLen(tiene id sede), sedeInfo(tiene nombre), estInfo(tiene Mun id)
sedesJoin = pd.merge(sedeLen,sedeInfo[['ID_SEDE','COD_DANE','NOMBRE']],on='ID_SEDE',how='left')
sedesCompleto = pd.merge(sedesJoin,estInfo[['COD_DANE','MUNI_ID','NOMBRE']],on='COD_DANE',how='left')


'''=================LAYOUT GENERAL================='''
menu = html.Div(    
    [
        html.H2("Saber 5", className="display-4"),
        html.Hr(),
        html.P("Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                #'exact' es igual a active=True -> Cuando el pathName sea igual a href.
                #'href' es la ruta (url) que va a tener la página.
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

# Se crea el layout general con los componentes anteriomente creados.
app.layout = html.Div([
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
        [children]: [Contenido a mostrar por cada página]
    """    
    if pathname == "/": # Refiere al 'Home' o 'Inicio'.

        header = html.H1(id='', className='', children='Análisis de datos')

        inputSeparador = dcc.Input(
            id='txfsep',
            type = "text",
            placeholder="Ingrese un separador...",                                   
            size="22",            
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
            inputSeparador,
            html.P('Separador'),                
            html.Hr(), #Linea horizontal            
            html.H5(id='h4sep'),

            upload,                 
            # Mostrará la tabla según el archivo subido.                         
            html.Div(id='output-data-upload'),
            # Mostrará la información del atributo escogido en la tabla.
            html.Div(id='info-atributo'),
        ]
    elif pathname == "/departamento":
        
        # Guarda los datos que se generan en el callback de creación de la tabs.
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

        return html.Div([
            dataDeptos,
            header,
            deptoZonasDropdown,
            deptoDeptoDropdown,
            inicializarTabs('depto')
        ])        
    elif pathname == "/zona":

        # Guarda los datos que se generan en el callback de creación de la tabs.
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

        return [
            dataZona,
            header,
            zonasZonasDropdown, 
            inicializarTabs('zona')
        ]
    elif pathname == "/entidadter":

        # Guarda los datos que se generan en el callback de creación de la tabs.
        dataEnt = dcc.Store(id='data-ent', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Entidad territorial'),
        ])

        tipoentDropdown =dcc.Dropdown(
            id='tipoentdropdown',
            options=tipoentdropdown,
            value='-1',
            placeholder="Elija una el tipo de entidad territorial..."
        )

        entDropdown = dcc.Dropdown(
            id='entdropdown',
            options=entdropdown,
            value='Todas las entidades territoriales',
            placeholder="Elija una entidad territorial..."
        )

        return [
            dataEnt,
            header,
            tipoentDropdown,
            entDropdown,            
            inicializarTabs('ent')
        ]
    elif pathname == "/municipio":

        # Guarda los datos que se generan en el callback de creación de la tabs.
        dataEnt = dcc.Store(id='data-mpio', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Municipio'),
        ])
        
        mpiodeptoDropdown = dcc.Dropdown(
            id='mpioddepto',
            options=deptosdpenmpios,
            value='Todos los municipios',
            placeholder="Elija un departamento..."
        )

        mpiompioDropdown = dcc.Dropdown(
            id='mpioddmpio',                    
            placeholder="Elija un municipio..."
        )

        return [               
            dataEnt,
            header,
            mpiodeptoDropdown,
            mpiompioDropdown,
            inicializarTabs('mpio')
        ]
    elif pathname == "/establecimiento":

        # Guarda los datos que se generan en el callback de creación de la tabs.
        dataEst = dcc.Store(id='data-est', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Establecimiento educativo'),
        ])

        estdeptoDropdown = dcc.Dropdown(
            id='estdepto',
            options=estDeptosDropdown,
            value='Antioquia',
            placeholder="Elija un departamento..."
        )

        estmpioDropdown = dcc.Dropdown(
            id='estmpio',
            placeholder="Elija un municipio..."
        )

        estDropdown = dcc.Dropdown(
            id='estestablmtos',            
            placeholder="Elija un establecimiento..."
        )

        return [  
            dataEst,
            header,
            estdeptoDropdown,
            estmpioDropdown,
            estDropdown,
            inicializarTabs('est')
        ]
    elif pathname == "/sede":
        # Guarda los datos que se generan en el callback de creación de la tabs.
        dataSede= dcc.Store(id='data-sede', storage_type='local')

        header =  html.Div(className='header', children=[
            html.H1(children='Sede de establecimiento educativo'),
        ])

        estdeptoDropdown = dcc.Dropdown(
            id='estdepto',
            options=estDeptosDropdown,
            value='Antioquia',
            placeholder="Elija un departamento..."
        )

        estmpioDropdown = dcc.Dropdown(
            id='estmpio',
            placeholder="Elija un municipio..."
        )

        estDropdown = dcc.Dropdown(
            id='sedeest',           
            placeholder="Elija un establecimiento..."
        )

        sedesedeDropdown = dcc.Dropdown(
            id='sedesede',            
            placeholder="Elija un establecimiento..."
        )

        sedejrnadasDropdown = dcc.Dropdown(
            id='sedejrnadas',            
            placeholder="Elija una jornada..."
        )

        return [  
            dataSede,
            header,
            estdeptoDropdown,
            estmpioDropdown,
            estDropdown,
            sedesedeDropdown,
            sedejrnadasDropdown,
            inicializarTabs('sede')
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

    # Si se intenta acceder a url que no existe, se muestra un mensaje de error.
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


'''=================FUNCIONES GENERALES================='''

def inicializarTabs(pseudo_id):

    # Tabs que contiene la tabla y los gráficos.
    tabsVistas = html.Div(id='div-tabs-vistas',children=[
        dbc.Tabs(
            [
                dbc.Tab(label="Tabla", tab_id='tab-tabla-{}'.format(pseudo_id)),
                dbc.Tab(label="Gráfico", tab_id='tab-grafico-{}'.format(pseudo_id)),
            ],
            id='tabs-vistas-{}'.format(pseudo_id),
            active_tab='tab-tabla-{}'.format(pseudo_id),
        ),
        html.Div(id='content-tabs-vistas-{}'.format(pseudo_id)),
    ])

    # Tabs que filtra por compentencia y tiene adentro a tabsVistas
    tabsComp = html.Div(id='div-tabs-comp',children=[
        dbc.Tabs(
            [
                dbc.Tab(label="Lenguaje", tab_id='tab-len-{}'.format(pseudo_id)),
                dbc.Tab(label="Matemáticas", tab_id='tab-mat-{}'.format(pseudo_id)),
                dbc.Tab(label="Ciencias naturales", tab_id='tab-nat-{}'.format(pseudo_id), disabled=True),
                dbc.Tab(label="Competencias ciudadanas", tab_id='tab-ciu-{}'.format(pseudo_id), disabled=True),
            ],
            id='tabs-comp-{}'.format(pseudo_id),
            active_tab='tab-len-{}'.format(pseudo_id),
        ),
        html.Div(id='content-tabs-comp-{}'.format(pseudo_id), children=tabsVistas),
    ])

    return tabsComp    


def contenedorSegunTabActiva(valueDropdown,seleccion,tablaData,tabsVistasActiva,idGrafico):
    """[Crea un contenedor con una tabla y su información general o uno con gráficos, dependiendo de la tab activa que reciba como parámetro.]

    Args:
        valueDropdown ([str]): [Valor para mostrar como título en el panel de Tabla]
        seleccion ([DataFrame]): [DataFrame con la información de valueDropdown]
        tablaData ([DataFrame]): [DataFrame con la información a mostrar en la tabla]
        tabsVistasActiva ([str]): [Nombre de la tab activa en el panel de Vistas]
        idGrafico ([str]): [Nombre del gráfico a crearse]

    Returns:
        [html.Div]: [Contenedor a mostrarse en el panel de Vistas según la tab activa.]
    """   
    contenedor = html.Div([])     
    if tabsVistasActiva == 'tab-tabla':

        # Calcular cuartil
        puntaje = int(*seleccion['PUNTAJE_PROMEDIO'].values)
        if(puntaje<=100):
            cuartil = "Pésimo (Q1)"
        elif(puntaje<=200):
            cuartil = "Malo (Q2)"
        elif(puntaje<=300):
            cuartil = "Regular (Q3)"
        else:
            cuartil = "Bueno (Q4)"

        
        # Se crea un div con la información general del dataset y una tabla mostrando su contenido.
        contenedorTabla = html.Div([
            html.H2(children=valueDropdown),
            html.Div([
                html.Hr(),
                html.P('Número de participantes: ' + str(*seleccion['N'].values)),
                html.P('Puntaje promedio: ' + str(*seleccion['PUNTAJE_PROMEDIO'].values)),
                html.P('Desviación: ' + str(*seleccion['DESVIACION'].values)),
                html.P('Cuartil: ' + cuartil)
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

        contenedor = contenedorTabla        
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
        
        # Retorna el contenedor correspondiente a la tab seleccionada.
        contenedor = contenedorGraficos  
    return contenedor

def generarDataParaGrafico(seleccion):
    """[Ajusta un DataFrame y lo modifica para cumplir con el formato de la creación de un gráfico. Posteriomente, dicho DataFrame se transforma en un dict para poderse compartir entre callbacks con dcc.Store.]

    Args:
        seleccion ([DataFrame]): [DataFrame con la información a mostrarse en un gráfico]

    Returns:
        [dict]: [Diccionario formado a través del DataFrame listo para compartirse entre callbacks]
    """    
    
    dffPorcentajes = seleccion.filter(like="PORCENTAJE").transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)
    dffPorcentajesDict = dffPorcentajes.to_dict('records')

    return dffPorcentajesDict


'''=================CALLBACKS EN ANÁLISIS================='''
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
    desviacion = "No es un valor numérico"
    if selected_columns:
        nulos =  copiadf[selected_columns[0]].isna().sum()
        modadf = copiadf[selected_columns[0]].mode() #Devuelve una Series
        if not modadf.empty: moda = modadf[0]
        distintos = copiadf[selected_columns[0]].nunique()
        tipoDato = copiadf[selected_columns[0]].dtypes        
        if tipoDato == numpy.int64 or tipoDato == numpy.float64:
            promedio = copiadf[selected_columns[0]].mean()
            mediana = copiadf[selected_columns[0]].median()
            max = copiadf[selected_columns[0]].max()
            min = copiadf[selected_columns[0]].min()
            desviacion = copiadf[selected_columns[0]].std()

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
            html.H6(["Desviación: {}".format(str(desviacion))]),
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
        dash_table.DataTable(
            id = 'datatable-main',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i,"selectable": True} for i in df.columns],
            column_selectable="single",           
            selected_columns=[],
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
  
        html.Hr(),
    ])

#Actualiza el separador
@app.callback(
    Output('h4sep', 'children'),
    [Input('txfsep', 'value')]
)
def update_sep(txfsep):
    if not txfsep:
        separador = "'|'"       
    else:
        separador = str(txfsep)

    return html.H6(id='', className='', children='Separador = ' + separador)


'''=================CALLBACKS EN DEPARTAMENTOS================='''
@app.callback(
    Output(component_id='deptodepto', component_property='options'),
    [Input(component_id='deptozonas', component_property='value')]
)
def update_deptodepto(zona_seleccionada):
    """Actualiza el dropdown de departamentos en 'Departamento' dependiendo de la zona seleccionada.

    Args:
        zona_seleccionada ([str]): [Valor elegido en el dropdown de zonas en 'Departamento']

    Returns:
        [list of dict]: [Departamentos de la zona seleccionada]
    """    
    deptosZonasCopy = deptosZonas[deptosZonas['ZONA']==zona_seleccionada]
    deptosdropdown = [{'label': deptosZonasCopy['DEPARTAMENTO'][i], 'value': deptosZonasCopy['DEPARTAMENTO'][i]} for i in deptosZonasCopy.index]
    return deptosdropdown
    
@app.callback(
    Output('deptodepto', 'value'),
    [Input('deptodepto', 'options')]
)
def update_dp(deptodepto_options):
    """Selecciona el primer Departamento en el dropdown de departamentos en 'Departamento' después de que este fuese actualizado.

    Args:
        deptodepto_options ([type]): [description]

    Returns:
        [str]: [Primer departamento del dropdown de departamentos en 'Departamento']
    """    
    return deptodepto_options[0]['value']
 
@app.callback(
    Output('data-depto','data'),
    Output('content-tabs-vistas-depto','children'),
    [Input(component_id='deptodepto', component_property='value'),
    Input('tabs-comp-depto','active_tab'),
    Input('tabs-vistas-depto','active_tab')]
 )
def actualizar_info_depto(deptodepto,tabsCompActiva,tabsVistasActiva):
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        deptodepto ([str]): [Valor del dropdown de departamentos]
        tabsCompActiva ([str]): [Id de la tab de competencias activa]
        tabsVistasActiva ([str]): [Id del la tab de vistas activa]

    Returns:
        [dict]: [Diccionario con los datos del departamento seleccionado]
        [htmldiv]: [Contenedor con el children de la tab activa]
    """    
    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-depto":
        dffCompetencia = deptosLen
    elif tabsCompActiva == "tab-mat-depto":
        dffCompetencia = deptosMat

    # Filtra según el departamento escogido
    seleccion = dffCompetencia[dffCompetencia['DEPARTAMENTO']==deptodepto] 

    # Si se elige todos los departamentos, en la tabla se muestran todos los departamentos.
    if 'Todos los departamentos'==deptodepto:
        tablaData = dffCompetencia
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
def actualizar_grafico_depto(tipoGrafico,dataDeptos):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico ([str]): [Valor del dropdown del tipo de gráfico]
        dataDeptos ([dict]): [Diccionario con la información del departamento seleccionado]

    Returns:
        [htmldiv]: [Contenedor del gráfico a mostrar en la tab de gráfico]
    """    
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
        zonaszonas ([str]): [Valor del dropdown de zonas en 'Zona']
        tabsCompActiva ([str]): [Id de la tab de competencias activa]
        tabsVistasActiva ([str]): [Id del la tab de vistas activa]

    Returns:
        [dict]: [Diccionario con los datos del departamento seleccionado]
        [htmldiv]: [Contenedor con el children de la tab activa]
    """    

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-zona":
        dffCompetencia = zonasLen
    elif tabsCompActiva == "tab-mat-zona":
        dffCompetencia = zonasMat

    # Filtra según el departamento escogido
    seleccion = dffCompetencia[dffCompetencia['ZONA']==zonaszonas] 

    # Si se elige todos los departamentos, en la tabla se muestran todos los departamentos.
    if 'Todas las zonas'==zonaszonas:
        tablaData = dffCompetencia
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
def actualizar_grafico_zona(tipoGrafico,dataDeptos):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico ([str]): [Valor del dropdown del tipo de gráfico]
        dataDeptos ([type]): [Diccionario con la información de la zona seleccionada]

    Returns:
        [htmldiv]: [Contenedor del gráfico a mostrar en la tab de gráfico]
    """    
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataDeptos)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
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


'''=================CALLBACKS EN ENTIDAD TERRITORIAL================='''
@app.callback(
    Output('entdropdown', 'options'),
    [Input('tipoentdropdown', 'value')]
)
def update_entdropdown(tipoent_seleccionada):
    """Actualiza el dropdown de entidades territoriales en dependiendo del tipo seleccionado.

    Args:
        tipoent_seleccionada ([str]): [Valor elegido en el dropdown de tipo de entidades territoriales] 

    Returns:
        [list of dict]: [Entidades territoriales del tipo seleccionado]
    """ 

    enterritorialesCSVCopy = enterritorialesCSV[enterritorialesCSV['TIPO']==int(tipoent_seleccionada)]

    entDp = [{'label': enterritorialesCSVCopy['ENTIDAD'][i], 'value': enterritorialesCSVCopy['ENTIDAD'][i]} for i in enterritorialesCSVCopy.index]
    
    return entDp
    
@app.callback(
    Output('entdropdown', 'value'),
    [Input('entdropdown', 'options')]
)
def update_dp(entdropdown_options):
    """Selecciona la primer entidad territorial según el tipo seleccionado, después de que este fuese actualizado.

    Args:
        entdropdown_options ([list of dicts]): [Lista nombres de entidades territoriales]

    Returns:
        [str]: [Primer entidad territorial del dropdown actualizado]
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
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        entdropdown ([str]): [Valor del dropdown de entidad territorial]
        tabsCompActiva ([str]): [Id de la tab de competencias activa]
        tabsVistasActiva ([str]): [Id del la tab de vistas activa]

    Returns:
        [dict]: [Diccionario con los datos de la entidad territorial seleccionado]
        [htmldiv]: [Contenedor con el children de la tab activa]
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
        tablaData = dffCompetencia
    else:
        tablaData = seleccion
    
    # Crea el contenedor que se va a enviar según la tab activa
    if tabsVistasActiva == 'tab-tabla-ent':
        contenedorOutput = contenedorSegunTabActiva(etdropdownvalue,seleccion,tablaData,'tab-tabla','grafico-ent')
    elif tabsVistasActiva == 'tab-grafico-ent':
        contenedorOutput = contenedorSegunTabActiva(etdropdownvalue,seleccion,tablaData,'tab-grafico','grafico-ent')

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generarDataParaGrafico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-ent','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-ent','data')]
)
def actualizar_grafico_ent(tipoGrafico,dataEnt):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico ([str]): [Valor del dropdown del tipo de gráfico]
        dataEnt ([type]): [Diccionario con la información de la entidad territorial seleccionada]

    Returns:
        [htmldiv]: [Contenedor del gráfico a mostrar en la tab de gráfico]
    """    
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataEnt)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
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


'''=================CALLBACKS EN MUNICIPIOS================='''
@app.callback(
    Output(component_id='mpioddmpio', component_property='options'),
    [Input(component_id='mpioddepto', component_property='value')]
)
def update_deptodepto(depto_seleccionado):
    """Actualiza el dropdown de municipios en dependiendo del departamento seleccionado.

    Args:
        depto_seleccionado ([str]): [Valor elegido en el dropdown de departamentos en 'Municipio']

    Returns:
        [list of dict]: [Departamentos de la zona seleccionada]
    """
    mpioLenCopy = mpioLen[mpioLen['DEPA_NOMBRE']==depto_seleccionado]
    mpiosdropdown = [{'label': mpioLenCopy['MUNI_NOMBRE'][i], 'value': mpioLenCopy['MUNI_ID'][i]} for i in mpioLenCopy.index]
    return mpiosdropdown
    
@app.callback(
    Output('mpioddmpio', 'value'),
    [Input('mpioddmpio', 'options')]
)
def update_dp(mpioddmpio_options):
    """Selecciona el primer municipio en el dropdown de municipios después de que este fuese actualizado.

    Args:
        mpioddmpio_options ([list of dicts]): [Lista de las opciones del dropdown de municipios]

    Returns:
        [str]: [Primer municipio del dropdown de municipios actualizado']
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
    """Actualiza el contenido del tabs vistas dependiendo de si se elige tabla o gráficos y dependiendo de si se eligió Lenguaje o Matemáticas.

    Args:
        mpioddmpiovalue ([str]): [Valor del dropdown de municipios en 'Municipio']       
        tabsCompActiva ([str]): [Id de la tab de competencias activa]
        tabsVistasActiva ([str]): [Id del la tab de vistas activa]

    Returns:
        [dict]: [Diccionario con los datos del municipio seleccionado]
        [htmldiv]: [Contenedor con el children de la tab activa]
    """    

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-mpio":
        dffCompetencia = mpioLen
    elif tabsCompActiva == "tab-mat-mpio":
        dffCompetencia = mpioMat


    # Se manejó con ids porque hay algunos municipios que tienen el mismo nombre(pero de diferente departamento) y lo único que los diferencia es el id.
    seleccion = dffCompetencia[dffCompetencia['MUNI_ID']==mpioddmpiovalue]
    
    # Es 0 porque ese es el id de Todos los municipios.
    if 0==mpioddmpiovalue:
        tablaData = dffCompetencia
    else:
        tablaData = seleccion
    
    # Crea el contenedor que se va a enviar según la tab activa
    if tabsVistasActiva == 'tab-tabla-mpio':
        contenedorOutput = contenedorSegunTabActiva(seleccion['MUNI_NOMBRE'],seleccion,tablaData,'tab-tabla','grafico-mpio')
    elif tabsVistasActiva == 'tab-grafico-mpio':
        contenedorOutput = contenedorSegunTabActiva(mpioddmpiovalue,seleccion,tablaData,'tab-grafico','grafico-mpio')

    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dataGrafico = generarDataParaGrafico(seleccion)
    
    return dataGrafico,contenedorOutput
          
@app.callback(
    Output('grafico-mpio','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-mpio','data')]
)
def actualizar_grafico_mpio(tipoGrafico,dataMpio):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico ([str]): [Valor del dropdown del tipo de gráfico]
        dataEnt ([type]): [Diccionario con la información de la entidad territorial seleccionada]

    Returns:
        [htmldiv]: [Contenedor del gráfico a mostrar en la tab de gráfico]
    """    
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataMpio)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
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



'''=================CALLBACKS EN ESTABLECIMIENTO================='''
@app.callback(
    Output('estmpio', 'options'),
    [Input('estdepto', 'value')]
)
def update_estmpio(estdeptovalue):
    """Actualiza el dropdown de municipios en dependiendo del departamento seleccionado.

    Args:
        depto_seleccionado ([str]): [Valor elegido en el dropdown de departamentos en 'Municipio']

    Returns:
        [list of dict]: [Departamentos de la zona seleccionada]
    """
    estMpiosCopy = estMpios[estMpios['DEPA_NOMBRE']==estdeptovalue]
    estmpiosDropdown = [{'label': estMpiosCopy['MUNI_NOMBRE'][i], 'value': estMpiosCopy['MUNI_ID'][i]} for i in estMpiosCopy.index]
    return estmpiosDropdown
    
@app.callback(
    Output('estmpio', 'value'),
    [Input('estmpio', 'options')]
)
def update_dp(estmpio_options):
    """Selecciona el primer municipio en el dropdown de municipios después de que este fuese actualizado.

    Args:
        mpioddmpio_options ([list of dicts]): [Lista de las opciones del dropdown de municipios]

    Returns:
        [str]: [Primer municipio del dropdown de municipios actualizado']
    """    
    return estmpio_options[0]['value']

@app.callback(
    Output('estestablmtos','options'),
    [Input('estmpio','value')]
)
def actualizar_dpestablecimientos(estmpio_value):
    estInfoCopy2 = estInfo[estInfo['MUNI_ID']==estmpio_value]
    estDropdown = [{'label': estInfoCopy2['NOMBRE'][i], 'value': estInfoCopy2['COD_DANE'][i]} for i in estInfoCopy2.index]

    return estDropdown

@app.callback(
    Output('estestablmtos', 'value'),
    [Input('estestablmtos', 'options')])
def update_dp(estestablmtos_options):
    return estestablmtos_options[0]['value']


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
        mpioddmpiovalue ([str]): [Valor del dropdown de municipios en 'Municipio']       
        tabsCompActiva ([str]): [Id de la tab de competencias activa]
        tabsVistasActiva ([str]): [Id del la tab de vistas activa]

    Returns:
        [dict]: [Diccionario con los datos del municipio seleccionado]
        [htmldiv]: [Contenedor con el children de la tab activa]
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
        return {},html.Div(['No se registran datos para este establecimiento'])
    
    # Devuelve un contenedor dependiendo de la competencia seleccionada
    if tabsVistasActiva == 'tab-tabla-est':

        # Calcular cuartil
        puntaje = int(*seleccion['PROMEDIO'].values)
        if(puntaje<=100):
            cuartil = "Pésimo (Q1)"
        elif(puntaje<=200):
            cuartil = "Malo (Q2)"
        elif(puntaje<=300):
            cuartil = "Regular (Q3)"
        else:
            cuartil = "Bueno (Q4)"
    
        # Se crea un div con la información general del dataset y una tabla mostrando su contenido.
        contenedorTabla = html.Div([
            html.H2(children=nombre['NOMBRE']),
            html.Div([
                html.Hr(),
                html.P('Número de participantes: ' + str(*seleccion['PARTICIPANTES'].values)),
                html.P('Puntaje promedio: ' + str(*seleccion['PROMEDIO'].values)),
                html.P('Desviación: ' + str(*seleccion['DESVIACION'].values)),
                html.P('Cuartil: ' + cuartil)
            ]),

            # Creación de la tabla con el dataframe de la competencia escogida.
            dash_table.DataTable(
                id = 'tabla-info',
                data=seleccion.to_dict('records'),
                columns=[{'name': i, 'id': i,"selectable": True} for i in seleccion.columns],
                sort_action="native",
                sort_mode="multi",
                fixed_rows={'headers': True},
                page_size=10, 
                style_cell={
                    'minWidth': 250, 'maxWidth': 250, 'width': 250
                },
            ),
        ])

        contenedor = contenedorTabla        
    elif tabsVistasActiva == 'tab-grafico-est':

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
                id='grafico-est',
                figure={},
            )
        ])
        
        # Retorna el contenedor correspondiente a la tab seleccionada.
        contenedor = contenedorGraficos  
      
    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dffPorcentajes = seleccion.filter(["INSUFICIENTE","MINIMO","SATISFACTORIO","AVANZADO"]).transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'PORCENTAJE'}, inplace = True)   

    dataGrafico = dffPorcentajes.to_dict('records')
    
    return dataGrafico,contenedor
          
@app.callback(
    Output('grafico-est','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-est','data')]
)
def actualizar_grafico_est(tipoGrafico,dataEst):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico ([str]): [Valor del dropdown del tipo de gráfico]
        dataEnt ([type]): [Diccionario con la información de la entidad territorial seleccionada]

    Returns:
        [htmldiv]: [Contenedor del gráfico a mostrar en la tab de gráfico]
    """    
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataEst)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
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


'''=================CALLBACKS EN SEDE================='''
@app.callback(
    Output('sedeest','options'),
    [Input('estmpio','value')]
)
def actualizar_establecimientos(estmpio_value):

    # Se filtra por el municipio seleccionado y después se elimina los duplicados porque sino saldrían todas las sedes. Se hace drop duplicates en COD_DANE porque es el indicador único de un establecimiento.
    sedesCompletoCopy = sedesCompleto[sedesCompleto['MUNI_ID']==estmpio_value].drop_duplicates('COD_DANE')

    # NOMBRE_y es el nombre del establecimiento
    sedeestDropdown = [{'label': sedesCompletoCopy['NOMBRE_y'][i], 'value': sedesCompletoCopy['COD_DANE'][i]} for i in sedesCompletoCopy.index]

    return sedeestDropdown


#Actualiza el dropdown de sede según el establecimiento seleccionado.
@app.callback(
    Output('sedesede', 'options'),
    [Input('sedeest', 'value')]
)
def actualizar_sede(sedeest_value):

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
    Output('sedeest','value'),
    [Input('sedeest','options')]
)
def update_dp(sedeest_options):
    return sedeest_options[0]['value']

@app.callback(
    Output('sedesede','value'),
    [Input('sedesede','options')]
)
def update_dp(sedesede_options):
    return sedesede_options[0]['value']

@app.callback(
    Output('sedejrnadas','value'),
    [Input('sedejrnadas','options')]
)
def update_dp(sedejrnadas_options):
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
        mpioddmpiovalue ([str]): [Valor del dropdown de municipios en 'Municipio']       
        tabsCompActiva ([str]): [Id de la tab de competencias activa]
        tabsVistasActiva ([str]): [Id del la tab de vistas activa]

    Returns:
        [dict]: [Diccionario con los datos del municipio seleccionado]
        [htmldiv]: [Contenedor con el children de la tab activa]
    """        

    #Copia de los dataframes dependiendo de la competencia elegida.
    if tabsCompActiva == "tab-len-sede":
        dffCompetencia = sedeLen
    elif tabsCompActiva == "tab-mat-sede":
        dffCompetencia = sedeMat

    # Se manejó con COD_DANE porque los archivos de competencias solo se pueden conectar por ese atributo
    seleccion = dffCompetencia[dffCompetencia['ID_SEDE']==sedejrnadas_value]

    nombre = sedesCompleto[sedesCompleto['ID_SEDE']==sedejrnadas_value]

    # Si el establecimiento no presentó la prueba
    if seleccion.empty:
        return {},html.Div(['No se registran datos para este establecimiento'])
    
    # Devuelve un contenedor dependiendo de la competencia seleccionada
    if tabsVistasActiva == 'tab-tabla-sede':
    
        # Se crea un div con la información general del dataset y una tabla mostrando su contenido.
        contenedorTabla = html.Div([
            html.H2(children=nombre['NOMBRE_x']),
            html.Div([
                html.Hr(),
                html.P('Número de participantes: ' + str(*seleccion['PARTICIPANTES'].values)),
                html.P('Número de evaluados: ' + str(*seleccion['EVALUADOS'].values))
            ]),

            # Creación de la tabla con el dataframe de la competencia escogida.
            dash_table.DataTable(
                id = 'tabla-info',
                data=seleccion.to_dict('records'),
                columns=[{'name': i, 'id': i,"selectable": True} for i in seleccion.columns],
                sort_action="native",
                sort_mode="multi",
                fixed_rows={'headers': True},
                page_size=10, 
                style_cell={
                    'minWidth': 250, 'maxWidth': 250, 'width': 250
                },
            ),
        ])

        contenedor = contenedorTabla        
    elif tabsVistasActiva == 'tab-grafico-sede':

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
                id='grafico-sede',
                figure={},
            )
        ])
        
        # Retorna el contenedor correspondiente a la tab seleccionada.
        contenedor = contenedorGraficos  
      
    # Genera un dict que será enviado al callback de actualizar gráfico a través del Output de dcc.Store
    dffPorcentajes = seleccion.filter(["INSUFICIENTE","MINIMO","SATISFACTORIO","AVANZADO"]).transpose()    
    dffPorcentajes.reset_index(inplace = True)    
    dffPorcentajes.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    dffPorcentajes.rename(columns={dffPorcentajes.columns[1]: 'NUMERO DE ESTUDIANTES'}, inplace = True)   

    dataGrafico = dffPorcentajes.to_dict('records')
    
    return dataGrafico,contenedor
          
@app.callback(
    Output('grafico-sede','figure'),
    [Input('dropdown-graficos','value'),
    Input('data-sede','data')]
)
def actualizar_grafico_est(tipoGrafico,dataEst):
    """Actualiza el gráfico de la Tab, dependiendo del tipo de gráfico que se haya seleccionado en el dropdown. Recibe el dict necesario para crear la figura a través del input del dcc.Store

    Args:
        tipoGrafico ([str]): [Valor del dropdown del tipo de gráfico]
        dataEnt ([type]): [Diccionario con la información de la entidad territorial seleccionada]

    Returns:
        [htmldiv]: [Contenedor del gráfico a mostrar en la tab de gráfico]
    """    
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(dataEst)   

    if tipoGrafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'NUMERO DE ESTUDIANTES',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
        figure.update_xaxes(visible=False) #Esconder los valores de X
    
    elif tipoGrafico == 'Dona':
        figure = px.pie(
            data_frame=dffPorcentajes,
            names ='RENDIMIENTO',
            values = 'NUMERO DE ESTUDIANTES',
            hole=.3
        )
    else:
        figure = px.line(
            data_frame=dffPorcentajes,
            x = 'RENDIMIENTO',
            y = 'NUMERO DE ESTUDIANTES',
        )
    
    return figure


if __name__=='__main__':        
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True, port=3000)
