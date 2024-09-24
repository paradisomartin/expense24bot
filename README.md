# Expense Tracker Telegram Bot

Este proyecto consiste en un bot de Telegram que permite a los usuarios registrar y listar sus gastos de manera sencilla. El sistema está compuesto por dos servicios principales: Bot Service (Django) y Connector Service (Node.js).

## Requisitos previos

- Docker y Docker Compose
- Una cuenta de Telegram
- Una API key de Cohere

## Configuración inicial

1. Clona este repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_DIRECTORIO>
   ```

2. Crea un archivo `.env` copiando el .env.example y completando con tus datos y API keys.

## Levantando el proyecto

1. Construye y levanta los contenedores:
   ```
   docker-compose up --build
   ```

2. En una nueva terminal, ejecuta el script de gestión para crear las migraciones y aplicarlas:
   ```
   ./manage.sh
   ```
   Selecciona la opción 2 para hacer migraciones y luego la opción 3 para aplicarlas.

3. Crea un superusuario usando el mismo script:
   ```
   ./manage.sh
   ```
   Selecciona la opción 1 y sigue las instrucciones para crear un superusuario.

## Gestión de la lista blanca

El script `manage.sh` ahora incluye una opción para gestionar la lista blanca de usuarios:

1. Ejecuta el script:
  ```
  ./manage.sh
  ```

2. Selecciona la opción 6 para "Gestionar lista blanca".

3. En el submenú, puedes:
  - Agregar un usuario ingresando su Telegram ID.
  - Eliminar un usuario de la lista blanca.
  - Listar todos los usuarios en la lista blanca.


## Uso del bot

1. Inicia una conversación con @expense24bot en Telegram.

2. Para agregar un gasto, simplemente envía un mensaje con la descripción y el monto, por ejemplo:
   ```
   Compré Pizza 20 dólares
   Compré combustible 16 dólares
   ```

3. Para listar tus gastos recientes, envía uno de estos mensajes:
   ```
   listar gastos
   listar expensas
   ```

## Administración

Accede al panel de administración de Django en `http://localhost:8000/admin/` usando las credenciales del superusuario que creaste.

## Notas adicionales

- El bot solo responderá a usuarios que estén en la lista blanca. Asegúrate de agregar los IDs de Telegram de los usuarios autorizados a través del panel de administración.
- Las categorías de gastos se asignan automáticamente basándose en palabras clave en la descripción del gasto.

## Solución de problemas

Si encuentras algún problema al levantar los servicios o usar el bot, asegúrate de:

1. Verificar que todos los servicios estén corriendo correctamente con `docker-compose ps`.
2. Revisar los logs de los servicios con `docker-compose logs`.
3. Asegurarte de que las variables de entorno en el archivo `.env` estén correctamente configuradas.


## Licencia

[MIT License](LICENSE)
