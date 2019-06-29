# ENTREGA 4

#### Integrantes: Germán Johow, Lucas Álamos, Santiago Hitze, Felipe Garcia
#### Grupo 4-9

## Release
En la carpeta "release" podemos encontrar lo que sería la aplicación:
- El archivo main.py, el cual contiene todas las consultas que se piden para esta entrega
- usuarios.json, que es el archivo utilizado como base de datos para los usuarios
- messages.json, que es el archivo utilizado como base de datos para los mensajes
- Pipfile, que contiene los elementos a descargar/instalar que se necesitan para trabajar

## Correr la entrega

Para correr el programa, desde la consola (una vez importados los datos por mongo) se corren los comandos pipenv install, luego pipenv shell y finalmente python main.py que finalmente corre nuestro programa python que queda corriendo para acceder al servidor que en este caso es el localhost.

# Consultas:

## Para las consultas con [GET]

### Consulta 1: La ruta debe ser http://127.0.0.1:5000/mail/mail=<string:mid> con el mid obtenido gracias a ObjectId (libreria bson.objectid). El mid que se obtiene a partir de ObjectId no son directamente numeros enteros, si no que hexadecimales. Por ejemplo en el browser se busca :
- http://127.0.0.1:5000/mail/mail=5cfef14057f0ebce8b657f52
- http://127.0.0.1:5000/mail/mail=5cfef14057f0ebce8b657f46
- http://127.0.0.1:5000/mail/mail=5cfef14057f0ebce8b657f43
finalmente se cambia los ultimos dos digitos del mid, ejemplo mid= 5cfef14057f0ebce8b657f43

### Consulta 2: Para esta consulta se pone en el browser http://127.0.0.1:5000/mail/user=<int:uid>. Por ejemplo:
- http://127.0.0.1:5000/mail/user=1
- http://127.0.0.1:5000/mail/user=2

### Consulta 3: Para esta consulta el browser es http://127.0.0.1:5000/mail/user=<int:uid1>_<int:uid2>. Por ejemplo:
- http://127.0.0.1:5000/mail/user=1_2 que hace referencia a los mensajes enviados entre el usuario con uid 1 y el usuario con uid 2.


### CONSULTA 4: Agregar una o mas frases que si o si deben estar en el mensaje:
- http://127.0.0.1:5000/buscador1
El usuario puede ingresar una frase y se devuelve todos los mensajes que tengan esa frase en su contenido.

### CONSULTA 5: Agregar una o mas palabras que deseablemente deben estar, pero no necesariamente:
- http://127.0.0.1:5000/buscador2
El usuario puede ingresar distintas palabras separadas por espacio y se devuelven todos los mensajes que tengan alguna de esas palabrasn en su contenido. Ademas se puede filtrar por id

### CONSULTA 6: Agregar un conjunto de palabras que no pueden estar en el mensaje.
- http://127.0.0.1:5000/buscador3
El usuario puede ingresar distintas palabras separadas por espacio y se devuelven todos los mensajes que no tengan ninguna de dichas palabras en su contenido. Ademas se puede filtrar por id

### Consulta Post: Crear un mensaje
- http://localhost:5000/mail/
Se puede crear un mensaje enviando un form data con una valor string relacionado a la key "message" y  valores integer a las keys "sender" y "receptant" (todas necesarias

### Consulta Delete: Eliminar mensaje: Elimina un mensaje de la base de datos
- http://localhost:5000/mail/<string:mid>
Con el mismo tipo de Id mencionado para la consulta 1