# TopicosDeTelematica

READ ME

4 funcionalidades
Para ejecutar el código, en la terminal se debe situar en la carpeta correspondiente
-Py main.py

Le aparecerá el siguiente mensaje:

Bienvenido, seleccione lo necesario. 
1. Server. 
2. Client.

Lo primero debes activar el server escribiendo (1) y te confirmara la conexión con el siguiente mensaje.

('127.0.0.1', 64819) Conectado exitosamente.

PARTE A INICIO
Al conectarte al servidor, activas otra terminal e ingresas el mismo comando
-Py main.py

Le aparecerá el siguiente mensaje:

Bienvenido, seleccione lo necesario. 
1. Server. 
2. Client.

Seleccionara ya la parte del cliente para comenzar a seleccionar las funcionalidades (2) donde se inicializara la conexión con el server.
Bienvenido al server, seleccione alguna de las siguientes opciones.
1. Enviar una GET request.
2. Enviar una POST request.
3. Recibir un archivo tipo PDF.
4. Enviar un archivo.

PARTE A FIN
Ya lo que tu desees solo es seguir el ciclo.

Al seleccionar (1) enviara un GET

Le aparecera un mensaje de HTML 

Se enviará este mensaje y en el servidor imprimirá un mensaje de confirmación:

Se ha recibido una HTTP-Request de GET desde ('127.0.0.1', 64819)   
Se ha enviado una HTTP-Response

Se cierra el client. El servidor quedara activo y volver al paso de.
Activar otra terminal e ingresas el mismo comando
-Py main.py

(LE APARECERA PARTE A PAG 1)
Al seleccionar (3) le aparecerá que debe hacer:
Ingrese el nombre del archivo que desea descargar.
Ingresas el nombre

El servidor buscará el archivo y lo subirá.

NOTA
El archivo tiene que estar en el servidor en la carpeta para realizar la operación


Se cierra el client. El servidor quedara activo y volver al paso de.
Activar otra terminal e ingresas el mismo comando
-Py main.py

(LE APARECERA PARTE A PAG 1)
Al seleccionar (4) le aparecerá que debe hacer:
Ingrese el nombre del archivo que desea subir.
Ingresas el nombre

NOTA
El archivo tiene que estar en el cliente para realizar la operación de subir al servidor lo que está en el cliente


NOTA EL 3 Y EL 4
Presenta fallos en Windows
En Linux funciona perfectamente
