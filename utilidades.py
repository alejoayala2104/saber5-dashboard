def calcular_cuartil_rendimiento(puntaje):
    """Calcula el cuartil (Q1-Q4) según el puntaje de rendimiento académico, clasificandolo en Pésimo, Malo, Regular y Bueno.

    Args:
        puntaje (object): Entero con el puntaje de rendimiento académico.
    """

    if(puntaje<=100):
        cuartil = "Pésimo (Q1)"
    elif(puntaje<=200):
        cuartil = "Malo (Q2)"
    elif(puntaje<=300):
        cuartil = "Regular (Q3)"
    else:
        cuartil = "Bueno (Q4)"
    
    return cuartil

def generar_tooltips_dict(path_documentacion):
    """Genera un diccionario que contiene la descripción de cada columna de una tabla a partir de un csv de documentación.

    Args:
        path_documentacion (str): Ruta al archivo de documentación

    Returns:
        dict: Diccionario con la documentación para vista en tooltips
    """    
    dict_docs = {}
    try:
        archivo = open(path_documentacion,encoding='utf-8')
        for linea in archivo: 
            key, value = linea.strip().split('|')
            dict_docs[key] = value
    except:
        print("El archivo " + path_documentacion + " no existe")
    return dict_docs

def generar_data_grafico_dinamico(df_seleccion, tiene_porcentaje=True):
    """Ajusta un DataFrame y lo modifica para cumplir con el formato de la creación de un gráfico. Posteriomente, dicho DataFrame se transforma en un dict para poderse compartir entre callbacks con dcc.Store.

    Args:
        seleccion (DataFrame): DataFrame con la información a mostrarse en un gráfico

    Returns:
        dict: Diccionario formado a través del DataFrame listo para compartirse entre callbacks
    """    
    if(not tiene_porcentaje):
        df_grafico = df_seleccion.filter(["INSUFICIENTE","MINIMO","SATISFACTORIO","AVANZADO"]).transpose()    
    else:        
        df_grafico = df_seleccion.filter(like="PORCENTAJE").transpose()
    
    df_grafico.reset_index(inplace = True)    
    df_grafico.rename(columns = {'index':'RENDIMIENTO'}, inplace = True)
    df_grafico.rename(columns={df_grafico.columns[1]: 'PORCENTAJE'}, inplace = True)
    dffPorcentajesDict = df_grafico.to_dict('records')

    return dffPorcentajesDict