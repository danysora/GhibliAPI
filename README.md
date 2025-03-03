# API de Creación de Usuarios y Consulta de Base de Datos de Ghibli

Esta API permite la creación y gestión de usuarios, así como la consulta de la base de datos de Ghibli.

## Requisitos Previos

* **Python:** Asegúrate de tener Python instalado en tu sistema.
* **MongoDB:** Asegúrate de tener MongoDB instalado y que el servicio esté en ejecución.

## Instalación

1.  **Descarga del Repositorio:** Clona o descarga este repositorio en tu máquina local.
2.  **Acceso al Directorio:** Abre una terminal y navega hasta el directorio raíz del proyecto.
3.  **Entorno Virtual (Recomendado):**
    * Crea un entorno virtual para aislar las dependencias:
        ```bash
        python -m venv env
        ```
    * Activa el entorno virtual:
        * **Windows:** `env\Scripts\activate`
        * **Linux/macOS:** `source env/bin/activate`
4.  **Instalación de Dependencias:** Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configuración de New Relic:**
    * Abre el archivo `newrelic.ini` y reemplaza `LLAVE_AQUI` con tu clave de licencia de New Relic.
    * Puedes obtener tu clave de licencia en [https://newrelic.com/es](https://newrelic.com/es).

## Ejecución

1.  **Ejecutar Uvicorn:** Inicia la API con Uvicorn:
    ```bash
    uvicorn source.app:app --reload
    ```
2.  **Acceso a la API:** La API, por defecto, estará disponible en `http://127.0.0.1:8000`.
3.  **Documentación de la API:** Puedes acceder a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`.
4.  **Pruebas:** Puedes usar la documentación interactiva, Postman, Insomnia o cualquier cliente HTTP para probar los endpoints de la API.

## Endpoints Disponibles

* Creación de usuarios
* Consulta de usuarios
* Consulta de un solo usuario, recibe una ID de usuario.
* Edición de usuario, recibe una ID de usuario.
* Borrado de usuario, recibe una ID de usuario.
* Consulta de categorías en la base de datos de Ghibli, recibe una ID de usuario y una categoría a consultar.
* Consulta de un solo objeto en la base de datos de Ghibli, recibe una ID de usuario, una categoría a consultar y una ID de objeto.

## Estructura del Proyecto

* **`source/`:** Contiene el código fuente de la API.
    * **`newrelic.ini`:** Archivo de configuración de New Relic.
    * **`requirements.txt`:** Lista de dependencias del proyecto.
    * **`app.py`:** Nuestra aplicación principal, encargada de ejecutar la API.
    * **`database.py`:** Para definir y consultar nuestra base de datos.
    * **`models.py`:** Define nuestros modelos de datos.
    * **`routers/`:** Contiene los módulos para el funcionamiento de la API.
        * **`usuarios.py`:** Lógica relacionada con la gestión de usuarios.
        * **`ghibli.py`:** Lógica para consumir la API de Ghibli.

## Monitoreo

* Para monitorear el estado de la API, accede a tu perfil de New Relic, de donde obtuviste la clave de licencia.