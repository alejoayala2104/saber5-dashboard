from unicodedata import decimal
import pandas as pd
import csv

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

'''--------------Valores Plausibles--------------'''
valPlauCompleto = pd.read_csv('csv/Valores Plausibles/ValoresPlausibles_Grado5_2017.csv',sep='|',encoding='utf-8',header=0)

'''--------------Estudiantes--------------'''
estudiantesAcad = pd.read_csv('csv/Estudiantes/sbr5_estudiantes_acad.csv',sep='|',encoding='utf-8',header=0)
estudiantesSocio = pd.read_csv('csv/Estudiantes/sbr5_estudiantes_socio.csv',sep='|',encoding='utf-8',header=0)
estudiantesInstu = pd.read_csv('csv/Estudiantes/sbr5_estudiantes_instu.csv',sep='|',encoding='utf-8',header=0)