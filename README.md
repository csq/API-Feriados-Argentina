## API de Feriados Nacionales de la República Argentina
API RESTful para obtener información sobre feriados nacionales en Argentina

## Enpoints
`/`
Devuelve un mensaje de bienvenida

`/v1/feriados/lista`
Devuelve una lista de años disponibles para los que se dispone de datos de feriados

`/v1/feriados/<int:anio>`
Devuelve una lista de feriados nacionales para el año especificado

`/v1/feriados/actual/<string:consulta>`
Devuelve una lista de feriados nacionales que coinciden con la consulta especificada (por ejemplo, nombre de feriado)

`/v1/feriados/actual/<int:mes>`
Devuelve una lista de feriados nacionales para el mes especificado del año en curso

`/v1/feriados/actual/proximo`
Devuelve el feriado nacional más próximo


*Notas*

    La API utiliza un directorio data/ para almacenar archivos JSON que contienen datos de feriados para cada año.

    En el directorio utils/ se encuentra un script que descarga en formato json los feriados del año especificado y los guarda en data/

    Se utiliza el año, mes y día actuales para determinar qué feriados son próximos.

    Además se ha implementado manejo de errores utilizando los mecanismos de manejo de errores integrados de Flask.

## Ejecutar la API

Simplemente ejecute el script utilizando python app.py. La API estará disponible en http://localhost:5000.