# Sistema de Gestión de Biblioteca

Este proyecto es un sistema de gestión de biblioteca desarrollado con Django y Django REST Framework.

## Instalación

1. Clona este repositorio en tu máquina local:

    ```
    git clone <url_del_repositorio>
    ```

2. Navega al directorio del proyecto:

    ```
    cd nombre_del_directorio
    ```

3. Instala las dependencias necesarias:

    ```
    pip install -r requirements.txt
    ```

## Configuración

1. Tener instalado Python y pip en el sistema.

2. Configura un entorno virtual (opcional pero recomendado):

    ```
    python -m venv venv
    ```

3. Activa el entorno virtual:

    - En Windows:

        ```
        venv\Scripts\activate
        ```

    - En macOS y Linux:

        ```
        source venv/bin/activate
        ```

4. Al utilizar la propia base de datos que generan los proyectos en Django (sqlite3)
    no es necesario hacer otras configuraciones a la misma.

## Uso

- Teniendo el entorno virtual activado se deben de realizar las migraciones:

    ```
    python manage.py makemigrations
    ```
  
- Migrar esos datos a la base de datos:

    ```
    python manage.py migrate
    ```

- Ejecuta el servidor de Django:

    ```
    python manage.py runserver
    ```

- Accede a la aplicación mediante la URL [http://localhost:8000](http://localhost:8000).

## Implementación de requisitos

1. Agregar un libro al sistema:
- Se implementa en la vista agregar_libro_al_sistema utilizando el método POST del API.
- Los datos del libro se reciben en el cuerpo de la solicitud y se validan utilizando el serializador LibroSerializer.
- Si los datos son válidos, se guarda el libro en la base de datos y se devuelve una respuesta exitosa.

2. Buscar libros por parámetro:
- Se implementa en la vista buscar_libros utilizando el método GET del API.
- La vista acepta un parámetro de búsqueda (param) y, opcionalmente, una categoría (category).
- Los libros se filtran según el título, autor o ISBN que coincida con el parámetro de búsqueda.
- Si se proporciona una categoría, se filtran los libros por esa categoría.
- Los resultados se devuelven en formato JSON utilizando el serializador LibroSerializer.

3. Realizar un préstamo de libro:
- Se implementa en la vista realizar_prestamo utilizando el método POST del API.
- Los datos del préstamo se reciben en el cuerpo de la solicitud y se validan utilizando el serializador PrestamoSerializer.
- Se verifica si el libro solicitado está disponible.
- Si el libro está disponible, se guarda el préstamo en la base de datos, se marca el libro como no disponible y se devuelve una respuesta exitosa.

4. Registrar la devolución de un libro:
- Se implementa en la vista devolucion_libro utilizando el método PUT del API.
- Se recibe el ID del préstamo como parte de la URL.
- Se busca el préstamo correspondiente en la base de datos.
- Si el préstamo no ha sido devuelto, se registra la devolución actualizando el estado del préstamo y del libro, y se devuelve una respuesta exitosa.

## Patrones de Diseño

- El sistema maneja errores mediante el decorador @handle_errors.
- El sistema registra eventos relacionados con préstamos y devoluciones mediante el observador EventObserver.

## API REST

## Agregar un libro

### Request
`POST /api/agregar_libro/`

    curl -i -H 'Accept: application/json' -X POST -d '{
    "isbn": "isbn",
    "titulo": "titulo",
    "autor": "autor",
    "ano_publicacion": 2008,
    "categoria": "categoria"
    }' http://127.0.0.1:8000/api/agregar_libro/

### Response
    HTTP/1.1 201 Created
    Content-Type: application/json

    {
    "id": 1,
    "isbn": "isbn",
    "titulo": "titulo",
    "autor": "autor",
    "ano_publicacion": 2008,
    "categoria": "categoria"
    }

## Buscar Libros

### Request
`GET /api/buscar_libro/<str:param>/`

    curl -i -H 'Accept: application/json' http://127.0.0.1:8000/api/buscar_libro/<str:param>/

### Response
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
        {
            "id": 1,
            "isbn": "isbn",
            "titulo": "titulo",
            "autor": "autor",
            "ano_publicacion": 2008,
            "categoria": "categoria"
        }
    ]

### Request
`GET /api/buscar_libro/<str:param>/<str:category>/`

    curl -i -H 'Accept: application/json' http://127.0.0.1:8000/api/buscar_libro/<str:param>/<str:category>/

### Response
    HTTP/1.1 200 OK
    Content-Type: application/json

    [
        {
            "id": 1,
            "isbn": "isbn",
            "titulo": "titulo",
            "autor": "autor",
            "ano_publicacion": 2008,
            "categoria": "categoria"
        }
    ]

## Realizar Préstamo

### Request
`POST /api/realizar_prestamo/`

    curl -i -H 'Accept: application/json' -X POST -d '{
    "fecha_devolucion": "2024-10-23",
    "usuario": 1,
    "libro": 1
    }' http://127.0.0.1:8000/api/realizar_prestamo/

### Response
    HTTP/1.1 201 Created
    Content-Type: application/json

    {
    "id": 1,
    "fecha_prestamo": "2024-05-03",
    "fecha_devolucion": "2024-10-23",
    "devuelto": false,
    "usuario": 1,
    "libro": 1
    }

## Realizar Devolución

### Request
`PUT /api/devolucion/<int:prestamo_id>/`

    curl -i -H 'Accept: application/json' -X PUT -d http://127.0.0.1:8000/api/devolucion/<int:prestamo_id>/

### Response
    HTTP/1.1 200 OK
    Content-Type: application/json

    {
    "id": 1,
    "fecha_prestamo": "2024-05-03",
    "fecha_devolucion": "2024-10-23",
    "devuelto": true,
    "usuario": 1,
    "libro": 1
    }

## Créditos

Desarrollado por [Ing.Jorge Luis Batista Rodríguez](https://github.com/JorgeLBatista).


- **Versión 1.0.0 (03/05/2024):** Versión inicial del sistema de gestión de biblioteca.