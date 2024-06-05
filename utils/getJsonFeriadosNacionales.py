#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Carlos Quiroz
# Retorna en formato json los feriados nacionales de la República Argentina
# https://www.github.com/csq/

import urllib3
import json
import sys
import re
import os

from bs4 import BeautifulSoup

# Año debe ser a partir de 2020 en adelante
ANIO = sys.argv[1]
URL = f'https://www.argentina.gob.ar/interior/feriados-nacionales-{ANIO}'

# Enviar peticion get para obetener la pagina
https = urllib3.PoolManager()
request = https.request('GET', URL)

# Procesar pagina con BeautifulSoup
soup = BeautifulSoup(request.data, 'html.parser')

data = soup.find_all('script', text=re.compile(f'holidays{ANIO}'))

# Verificar que exista datos
if len(data) == 0:
    print('No se encontraron datos')
    exit()

# Obtener los substrings
data = str(data)[str(data).find('holidays' + ANIO + ' = '):str(data).find(';')]
data = data.replace('holidays' + ANIO + ' = ', '')

# Eliminar espacios en blanco
_RE_COMBINE_WHITESPACE = re.compile(r'\s+')
data = _RE_COMBINE_WHITESPACE.sub(' ', data).strip()

# Reemplazar ultima fila para que sea compatible con json
data = data.replace(' }, ]', ' }]')

# Obtener directorio actual
cwd = os.getcwd()

# Obtener directorio padre
parent_dir = os.path.dirname(cwd)

# Crear ruta para el directorio data
data_dir = os.path.join(parent_dir, 'data')

# Crear directorio data si no existe
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Crear ruta para el archivo
path = os.path.join(data_dir, f'feriados_nacionales_{ANIO}.json')

# Guardar datos
with open(path, 'w') as file:
    file.write(data)

# Leer datos JSON desde un archivo
with open(path, 'r') as archivo:
    datos = json.load(archivo)

# Filtrar datos
patron = rf'^\d{{2}}/\d{{2}}/{ANIO}$'

# Eliminar items que no coincidan con el patron
datos = [item for item in datos if re.match(patron, item['date'])]

# Guardar datos filtrados
with open(path, 'w') as file:
    print(f'Guardando archivo: data/feriados_nacionales_{ANIO}.json', file=sys.stderr)
    json.dump(datos, file , indent=4)