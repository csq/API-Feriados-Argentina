## API de Feriados Nacionales de la República Argentina
API RESTful para obtener información sobre feriados nacionales en Argentina

## Endpoints

* **GET: `/v1/feriados/lista`**  
Devuelve una lista de años disponibles para los que se dispone de datos de feriados

```json
{
  "anios": [
    2024,
    2023,
    2022,
    2021,
    2020
  ]
}
```

* **GET: `/v1/feriados/<int:anio>`**  
Devuelve una lista de feriados nacionales para el año especificado

```json
[
  {
    "date": "01/01/2024",
    "label": "Año Nuevo",
    "type": "inamovible"
  },
  {
    "date": "12/02/2024",
    "label": "Carnaval",
    "type": "inamovible"
  }
  ...
]
```

* **GET: `/v1/feriados/actual/<string:consulta>`**  
Devuelve una lista de feriados nacionales que coinciden con la consulta especificada (por ejemplo, nombre de feriado)

```json
[
  {
    "date": "25/12/2024",
    "label": "Navidad",
    "type": "inamovible"
  }
]
```

* **GET: `/v1/feriados/actual/<int:mes>`**  
Devuelve una lista de feriados nacionales para el mes especificado del año en curso
```json
[
  {
    "date": "07/07/2024",
    "label": "Año Nuevo Islámico (c)",
    "type": "no_laborable"
  },
  {
    "date": "09/07/2024",
    "label": "Día de la Independencia",
    "type": "inamovible"
  }
]
```

* **GET: `/v1/feriados/actual/proximo`**  
Devuelve el feriado nacional más próximo

```json
{
  "date": "16/06/2024",
  "label": "Fiesta del Sacrificio (c)",
  "type": "no_laborable"
}
```

## **Notas**

La API utiliza un directorio `data/` para almacenar archivos JSON que contienen datos de feriados para cada año.

En el directorio `utils/` se encuentra un script que descarga en formato JSON los feriados del año especificado y los guarda en `data/`

Se utiliza el año, mes y día actuales para determinar qué feriados son próximos.

Además se ha implementado manejo de errores utilizando los mecanismos de manejo de errores integrados de Flask.


## Ejecución de la API

Para ejecutar la API, simplemente corre el script utilizando el comando `python app.py`. La API estará disponible en http://localhost:5000.