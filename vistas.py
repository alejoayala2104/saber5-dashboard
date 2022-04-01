import dash_bootstrap_components as dbc
from dash import html,dcc,dash_table
import pandas as pd
import pandasql as ps
import numpy
import plotly.express as px

from utilidades import *
from lectura_archivos import *

'''=================VARIABLES PARA DROPDOWNS================='''
def generar_dp_options(nombre_atributo, nombre_tabla):
    """Genera una lista de opciones (diccionarios) para manejo de dropdowns a través de una consulta SQL.


    Args:
        nombre_atributo (str): Nombre del atributo a listar
        nombre_tabla (str): Nombre de la tabla o archivo CSV a consultar

    Returns:
        list of dict: Lista de opciones generadas para el dropdown
    """    
    
    consultaSQL = f"SELECT DISTINCT {nombre_atributo} FROM {nombre_tabla} ORDER BY {nombre_atributo}"
    consulta = ps.sqldf(consultaSQL, globals())
    opciones_dropdown = [{'label': consulta[nombre_atributo][i], 'value': consulta[nombre_atributo][i]} for i in consulta.index]
    return opciones_dropdown

#Opciones del dropdown de zonas en departamentos
opt_zonas_en_deptos = generar_dp_options('ZONA','deptosZonas')

#Opciones del dropdown de zonas en zonas (es diferente porque este tiene 'Todas las zonas', el anterior tiene 'Todos los departamentos')
opt_zonas_en_zonas = generar_dp_options('ZONA','zonasLen')

#Opciones del dropdown de Entidades territoriales
opt_ent_territoriales = generar_dp_options('ENTIDAD','enterritorialesCSV')

#Opciones del dropdown de departamentos en Municipios (el dp de departamentos en municipios es el mismo que el de departamentos)
opt_deptos_en_mpios = generar_dp_options('DEPA_NOMBRE','mpioLen')

#Opciones del dropdown de departamentos en 'Establecimiento'. Es diferente al que está en Municipios porque aquel tiene 'Todos los municipios'
opt_deptos_en_est = generar_dp_options('DEPA_NOMBRE','estMpios')

#Se mezclan los csv de: sedeLen(tiene id sede), sedeInfo(tiene nombre), estInfo(tiene Mun id)
sedesJoin = pd.merge(sedeLen,sedeInfo[['ID_SEDE','COD_DANE','NOMBRE']],on='ID_SEDE',how='left')
sedesCompleto = pd.merge(sedesJoin,estInfo[['COD_DANE','MUNI_ID','NOMBRE']],on='COD_DANE',how='left')

def inicializar_tabs_vistas(pseudo_id):
    """Inicializa los tabs de vistas (Tabla y Gráfico).
    Se generan vacías y se les asigna un id según el pseudo_id recibido.

    Args:
        pseudo_id (str): Pseudo id para generar el id de los componentes de la tab

    Returns:
        dbc.Card: Tabs de vistas
    """
    return dbc.Card(
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Tabla",
                                tab_id='tab-tabla-{}'.format(pseudo_id),
                                tab_class_name ='tab',
                                active_tab_class_name = 'active-tab'
                            ),
                            dbc.Tab(
                                label="Gráfico",
                                tab_id='tab-grafico-{}'.format(pseudo_id),
                                tab_class_name ='tab',
                                active_tab_class_name = 'active-tab'
                            ),
                        ],
                        id='tabs-vistas-{}'.format(pseudo_id),
                        active_tab='tab-tabla-{}'.format(pseudo_id)
                    )
                ]
            ),
            dbc.CardBody(
                # Corresponde al contenido de la tab de vistas según la vista activa
                html.Div(id='content-tabs-vistas-{}'.format(pseudo_id))
            )
        ]
    )

def inicializar_tabs_comp(pseudo_id):
    """Inicializa los tabs de competencia que contienen las tabs por vistas.
    Se generan vacías y se les asigna un id según el pseudo_id recibido.

    Args:
        pseudo_id (str): Pseudo id para generar el id de los componentes de la tab

    Returns:
        dbc.Card: Tabs de competencias
    """
    tabs_vistas = inicializar_tabs_vistas(pseudo_id)

    tabs_comp = dbc.Card(
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Tabs(
                        [
                            # tab_class_name hace referencia al nombre de la clase para estilizar con css cada tab.
                            dbc.Tab(label="Lenguaje", tab_id='tab-len-{}'.format(pseudo_id), tab_class_name ='tab'),
                            dbc.Tab(label="Matemáticas", tab_id='tab-mat-{}'.format(pseudo_id), tab_class_name ='tab'),
                            dbc.Tab(label="Ciencias naturales", tab_id='tab-nat-{}'.format(pseudo_id), disabled=True, tab_class_name ='tab'),
                            dbc.Tab(label="Competencias ciudadanas", tab_id='tab-ciu-{}'.format(pseudo_id), disabled=True, tab_class_name ='tab'),
                        ],
                        id='tabs-comp-{}'.format(pseudo_id),
                        active_tab='tab-len-{}'.format(pseudo_id),
                    )
                ]
            ),
            dbc.CardBody(
                # Corresponde al contenido de la tab de competencias según la competencia activa
                html.Div(id='content-tabs-comp-{}'.format(pseudo_id), children=tabs_vistas)
            )
        ]
    )
    return tabs_comp 
    
def inicializar_tabs_estudiantes():
    """Inicializa los tabs en Estudiantes con las siguientes pestañas: Académicas, Institucionales y Socioeconómicas.

    Returns:
        dbc.Card: Tabs de estudiantes
    """
    return dbc.Card(
        children=[
            dbc.CardHeader(
                children=[
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Académico",
                                tab_id='tab-acad',
                                tab_class_name ='tab',
                                active_tab_class_name = 'active-tab'
                            ),
                            dbc.Tab(
                                label="Institucional",
                                tab_id='tab-instu',
                                tab_class_name ='tab',
                                active_tab_class_name = 'active-tab'
                            ),
                            dbc.Tab(
                                label="Socioeconómico",
                                tab_id='tab-socio',
                                tab_class_name ='tab',
                                active_tab_class_name = 'active-tab'
                            ),
                        ],
                        id='tabs-estudiantes',
                        active_tab='tab-acad'
                    )
                ]
            ),
            dbc.CardBody(
                html.Div(id='content-tabs-estudiantes')
            )
        ]
    )

def generar_info_general(nombre_seleccion,df_seleccion,variable_analizada='general'):
    """Genera un contenedor HTML con la información general de un dataset de competencias

    Args:
        nombre_seleccion (str): Nombre a mostrarse en la cabecera del contenedor
        df_seleccion (DataFrame): DataFrame con la información de la variable a analizar.
        variable_analizada (str, optional): Variable de análisis (est=Establecimiento y sede= Sede). Defaults to 'general'.

    Returns:
        html: Contenedor HTML con la información general de un DataFrame
    """    

    header =html.H2(className='nombre-seleccion',children=nombre_seleccion)
    num_participantes = html.P()
    promedio = html.P()
    desviacion = html.P()        
    cuartil = html.P() 

    # Se valida si el dataframe tiene promedio. Y se calcula su cuartil
    if ('PUNTAJE_PROMEDIO' in df_seleccion and df_seleccion['PUNTAJE_PROMEDIO'].values.size != 0):
        promedio = html.P('Puntaje promedio: ' + str(*df_seleccion['PUNTAJE_PROMEDIO'].values))

        # Calcula el cuartil según el puntaje numérico. Se debe hacer un parse a int porque Dataframe.values devuelve un nparray.
        cuartil_calculado = calcular_cuartil_rendimiento(int(*df_seleccion['PUNTAJE_PROMEDIO'].values))
        cuartil = html.P('Cuartil: ' + str(cuartil_calculado))
    
    # Se valida si el dataframe tiene desviación
    if ('DESVIACION' in df_seleccion and df_seleccion['DESVIACION'].values.size != 0):
        desviacion = html.P('Desviación: ' + str(*df_seleccion['DESVIACION'].values))


    # En algunas pestañas el nombre de la columna de número de participantes cambia, entonces se genera un html.Div con la información que corresponda.

    if('est' in variable_analizada): 
        num_participantes = html.P('Número de participantes: ' + str(*df_seleccion['PARTICIPANTES'].values))

        promedio = html.P('Puntaje promedio: ' + str(*df_seleccion['PROMEDIO'].values))

        # Calcula el cuartil según el puntaje numérico. Se debe hacer un parse a int porque Dataframe.values devuelve un nparray.
        cuartil_calculado = calcular_cuartil_rendimiento(int(*df_seleccion['PROMEDIO'].values))
        cuartil = html.P('Cuartil: ' + str(cuartil_calculado))

    elif('sede' in variable_analizada):
        num_participantes = html.Div([
            html.P('Número de participantes: ' + str(*df_seleccion['PARTICIPANTES'].values)),
            html.P('Número de evaluados: ' + str(*df_seleccion['EVALUADOS'].values))
        ])
    else:
        # Se valida si el dataframe tiene número de participantes
        if ('N' in df_seleccion and df_seleccion['N'].values.size != 0):
            num_participantes = html.P('Número de participantes: ' + str(*df_seleccion['N'].values))

    info_general = html.Div(className="info-general",children=[
        header,
        num_participantes,
        promedio,
        desviacion,
        cuartil
    ])

    return info_general

def generar_tabla_general(df_datos,path_documentacion):
    """Genera una Dash DataTable para un DataFrame en particular. También agrega un tooltip a cada header del atributo.

    Args:
        df_datos (DataFrame): Datos a mostrar en la tabla
        path_documentacion (str): Ruta al archivo de documentación del significado de las variables del DataFrame

    Returns:
        dash_table.DataTable: Tabla con la información del DataFrame recibido
    """    
    tabla = dash_table.DataTable(
        id = 'tabla-info',
        data=df_datos.to_dict('records'),
        columns=[{'name': i, 'id': i,"selectable": True} for i in df_datos.columns],
        tooltip_header = generar_tooltips_dict(path_documentacion),
        sort_action="native",
        sort_mode="single",
        filter_action='native',
        fixed_rows={'headers': True},
        page_size=7, 
        style_table = {"borderRadius": "10px", "overflow": "hidden"},
        style_cell={
            'fontFamily': '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
            'textAlign': 'left',                        
            'padding':'0.75rem',
            'border':'none',
            'border-bottom':'1px solid rgb(0,0,0,0.1)',
            'borderRadius':'1rem',
            'minWidth': 300, 'maxWidth': 300, 'width': 300
        },
        style_header={
            'background-color': '#008000',
            'color': '#ffffff',
            'text-align': 'left',
            'borderRadius':'1rem',
        }
    )
    return tabla

def inicializar_grafico_puntajes(id_grafico):
    """Inicializa un dcc.Graph y un dropdown para elegir su tipo (Dona,Barras,Linea).

    Args:
        id_grafico (str): Id del gráfico a crear

    Returns:
        html: Contenedor HTML con el gráfico y el dropdown generados
    """    
    tipo_grafico = [
        {'label':'Dona', 'value': 'Dona'},
        {'label':'Barras', 'value': 'Barras'},
        {'label':'Linea', 'value': 'Linea'}
    ]

    return html.Div([
            html.H2(className='nombre-seleccion', children='Gráfico'),

            # Dropdown para elegir el tipo de gráfico
            dcc.Dropdown(id='dropdown-graficos',
                options=tipo_grafico,
                value='Dona',
            ),
            # Gráfico con un id determinado para posterior manejo de datos.
            dcc.Graph(
                id=id_grafico,
                figure={}
            )
    ])

def generar_grafico_puntajes(df_data, tipo_grafico):
    """Genera un gráfico de puntajes de rendimiento según el tipode gráfico seleccionado.

    Args:
        df_data (DataFrame): Datos que mostrará el gráfico
        tipo_grafico (str): Valor del tipo de gráfico escogido

    Returns:
        px.figure: Gráfico RENDIMIENTO/PORCENTAJE según el tipo de gráfico seleccionado.
    """    
    # Se convierte el dict recibido en un DataFrame para cumplir el formato de la creación de gráficos.
    dffPorcentajes = pd.DataFrame.from_dict(df_data)   

    if tipo_grafico == 'Barras':
        figure = px.bar(
            data_frame=dffPorcentajes,      
            x = 'RENDIMIENTO',
            y = 'PORCENTAJE',
            color='RENDIMIENTO' #Indica qué eje tendrá sus barras coloreadas.
        )
        # figure.update_layout(showlegend=False) #Esconder el label de X
        figure.update_xaxes(visible=False) #Esconder los valores de X
    
    elif tipo_grafico == 'Dona':
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

def generar_cont_tab_activa(tipo_vistas_activa,nombre_seleccion,df_seleccion,df_tabla,path_documentacion,id_grafico):
    """Genera el contenido de una tabla activa conteniendo información general del DataFrame recibido y su respectiva tabla de registros.

    Args:
        tipo_vistas_activa (str): Id de la tabla activa
        nombre_seleccion (str): Nombre a mostrarse en la cabecera del contenedor de información
        df_seleccion (DataFrame): DataFrame para calcular la información general
        df_tabla (DataFrame): DataFrame para mostrarse en la tabla
        path_documentacion (str): Ruta del archivo de documentación de los atributos de la tabla
        id_grafico (str): Id del gráfico a inicializar

    Returns:
        html: Contenedor HTML con la información generada
    """    

    if 'tab-tabla' in tipo_vistas_activa:
    
        # Se crea un div con la información general del dataset y una tabla mostrando su contenido.
        contenedor = html.Div(
            children=[
                generar_info_general(nombre_seleccion,df_seleccion,tipo_vistas_activa),
                generar_tabla_general(df_tabla,path_documentacion)
            ])       
    if 'tab-grafico' in tipo_vistas_activa:

        # Se crea el div con el dropdown del tipo de gráfico y el gráfico como componente vacío.
        contenedor = inicializar_grafico_puntajes(id_grafico)  
        
    return contenedor

def generar_analisis_atributos(df):
    """Genera una tabla de análisis de los atributos de un dataframe.

    Args:
        df (DataFrame): Dataframe a analizar

    Returns:
        dash.DataTable: Tabla con el análisis de los atributos
    """    

    columnas = [
            {"name":"ATRIBUTO","id":"ATRIBUTO"},
            {"name":"DISTINTOS","id":"DISTINTOS"},
            {"name":"COUNT","id":"COUNT"},
            {"name":"NULOS","id":"NULOS"},
            {"name":"MODA","id":"MODA"},
            {"name":"TIPO","id":"TIPO"},
            {"name":"PROMEDIO","id":"PROMEDIO"},
            {"name":"MEDIANA","id":"MEDIANA"},
            {"name":"MAXIMO","id":"MAXIMO"},
            {"name":"MINIMO","id":"MINIMO"},
            {"name":"DESVIACION","id":"DESVIACION"}
        ]
    atributos = []   
    for (columnName, columnData) in df.iteritems():
        nulos = columnData.isnull().sum()
        moda = columnData.mode(dropna=True)
        distintos = columnData.nunique()
        
        if moda.empty: #Si no hay moda, significa que todos sus valores son Nulos.
            moda = "-"
        else:
            moda = moda[0]

        promedio = "-"
        mediana = "-"
        maximo = "-"
        minimo = "-"
        desviacion = "-"
               
        #Info para valores numéricos
        tipoDato = columnData.dtypes
        if tipoDato == numpy.int64 or tipoDato == numpy.float64:

            if columnData.count() != 0: #Verificar que al menos tenga 1 valor 
                promedio = round(columnData.mean(),2)
                mediana = round(columnData.median(),2)
                maximo = round(columnData.max(),2)
                minimo = round(columnData.min(),2)
                desviacion = round(columnData.std(),2)       
        
        rowAtributo = {
            "ATRIBUTO":columnName,
            "DISTINTOS":distintos,
            "COUNT":columnData.count(),
            "NULOS":nulos,
            "MODA":moda,
            "TIPO":str(columnData.dtype),

            "PROMEDIO": promedio,
            "MEDIANA": mediana,
            "MAXIMO": maximo,
            "MINIMO": minimo,
            "DESVIACION": desviacion
        }
        atributos.append(rowAtributo)
  
    tablaAtributo = dash_table.DataTable(
            id = 'datatable-atributo',
            data=atributos,
            columns=columnas,
            row_selectable="single",   
            selected_rows=[0],
            sort_action="native",
            sort_mode="multi",
            page_action='native',
            page_size= 7,
            fixed_rows={'headers': True},
            style_as_list_view=True,
            style_table = {
            "borderRadius": "10px",
            'overflowY': 'auto',
            'overflowX': 'auto'
            },
            style_cell={
                'fontFamily': '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                'textAlign': 'left',
                'padding':'0.75rem',
                'border':'none',
                'border-bottom':'1px solid rgb(0,0,0,0.1)',
                'borderRadius':'1rem',
                'minWidth': 300, 'maxWidth': 300, 'width': 300
            },    
            style_header={
                'background-color': '#352b2b',
                'color': '#ffffff',
                'text-align': 'left',
                'borderRadius':'1rem',
            }
        )
    
    return html.Div([
        tablaAtributo,
        html.Br(),
        html.P('Seleccione un atributo en la tabla de análisis. Solo es válido para atributos hasta con 10 valores únicos.'),
        dcc.Graph(id='grafico-atributo'),
    ])