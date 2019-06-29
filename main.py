from flask import Flask, render_template, request, abort, json
from bson.objectid import ObjectId
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import random
# import atexit
# import subprocess

USER_KEYS = ['name', 'last_name', 'occupation', 'follows', 'age']
MAIL_KEYS = ["message", "receptant", "sender"]
MAIL_KEYS_2 = ["lat", "long", "date"]


# Levantamos el servidor de mongo. Esto no es necesario, puede abrir
# una terminal y correr mongod. El DEVNULL hace que no vemos el output
# mongod = subprocess.Popen('mongod', stdout=subprocess.DEVNULL)
# Nos aseguramos que cuando el programa termine, mongod no quede corriendo
# atexit.register(mongod.kill)

# El cliente se levanta en localhost:5432
client = MongoClient('localhost')
# Utilizamos la base de datos 'entidades'
db = client["test"]
# Seleccionamos la colección de usuarios
usuarios = db.users
mensajes = db.mensajes

# Iniciamos la aplicación de flask
app = Flask(__name__)


@app.route('/mail/mail=<string:mid>', methods=['GET'])
def get_mail(mid):
    # title = "Probando"
    # print(list(mensajes.find({}, {'_id': 1})))
    posts = mensajes.find({"_id": ObjectId(mid)}, {'_id': 0})
    post = [u for u in posts]
    if not post:
        post = ["No se encontraron mensajes"]
    return json.jsonify(post)
    # return render_template('user.html',title=title,uid=uid,user=user,
    # posts=posts)


@app.route('/mail/user=<int:uid>', methods=['GET'])
def bandeja(uid):
    # title = "Probando"
    posts = mensajes.find({"sender": uid}, {'_id': 0})
    users = usuarios.find({"uid": uid}, {'_id': 0})
    user = [u for u in users]
    post = [u for u in posts]
    if not post:
        post = ["No se encontraron mensajes"]
    if not user:
        user = ["No se encontro al usuario"]
    lista = user + post
    return json.jsonify(lista)
    # return render_template('user.html',title=title,uid=uid,user=user,
    # posts=posts)


@app.route('/mail/user=<int:uid1>_<int:uid2>', methods=['GET'])
def contacto(uid1, uid2):
    # title = "Probando"
    posts = mensajes.find({"$or": [
        {"$and": [
            {"sender": uid1},
            {"receptant": uid2}]},
        {"$and": [
            {"sender": uid2},
            {"receptant": uid1}]}]},
        {'_id': 0})
    # return render_template('contacto.html',title=title,uid1=uid1,uid2=uid2,
    # posts=posts)
    post = [p for p in posts]
    if not post:
        post = ["No se ha encontrado algún mensaje"]
    return json.jsonify(post)


@app.route("/mail/", methods=['POST'])
def create_mail():
    # sender = int, receiver = int, msj = str
    hoy = datetime.datetime.today()
    fecha = f"{hoy.year}-{hoy.month}-{hoy.day}"

    long, lat = random.uniform(-180, 180), random.uniform(-90, 90)
    # No sabia que poner, asi que aleatorio nomas
    print("aca json", request.json)
    print("aca form", request.form, [u for u in request.form])
    # Request.json nope, pero igual lo dejo
    if request.json:
        data = {key: request.json[key] for key in MAIL_KEYS}
        data["lat"] = lat
        data["long"] = long
        data["date"] = fecha
    elif request.form:
        mail = request.form["message"]
        sender = request.form["sender"]
        receptant = request.form["receptant"]
        data = {"message": mail,
                "sender": int(sender),
                "receptant": int(receptant),
                "lat": lat,
                "long": long,
                "date": fecha}
    else:
        abort(404)
        return json.jsonify(["Algo ha fallado"])
    result = mensajes.insert_one(data)
    print([u for u in mensajes.find({"$and":[{"sender": 2},{"receptant":3}]},
                                    {"_id": 0})])
    if result:
        return json.jsonify(["Se ha creado el mmensaje"])
    else:
        return json.jsonify(["Algo ha fallado"])
    # agrega a mensajes el diccionario con la info necesaria


@app.route('/mail/<string:mid>', methods=['DELETE'])
def delete_mail(mid):
    '''
    Elimina un usuario de la db.
    Se requiere llave uid
    '''

    # esto borra el primer resultado. si hay mas, no los borra
    mensajes.delete_one({"_id": ObjectId(mid)})

    message = f'Mail con id={mid} ha sido eliminado.'

    # Retorno el texto plano de un json
    return json.jsonify({'result': 'success', 'message': message})


@app.route("/buscador1")
def buscador1():
    return render_template("buscador1.html")

#Agregar una o mas frases que si o si deban estar en el mensaje
@app.route("/buscador1", methods = ["POST"])
def buscador11():
    frase = request.form["palabra"]
    id = request.form["id"]
    mensajes.create_index([("message", "text")])
    resultado = []
    for m in mensajes.find({"$text": {"$search": f'\{frase}'}},{"message" : 1}):
        resultado.append(m["message"])
    return json.jsonify(resultado)
    #if id:
        #return json.jsonify("con id")
    #else:
        #return json.jsonify("sin id")


@app.route("/buscador2")
def buscador2():
    return render_template("buscador2.html")


# Agregar una o mas frases que si o si deban estar en el mensaje
@app.route("/buscador2", methods=["POST"])
def buscador22():
    frase = request.form["palabra"]
    id = request.form["id"]
    palabras = str(frase).split()
    resultado = []

    if id:
        msjes = mensajes.find({"sender": int(id)}, {"message": 1})
    else:
        msjes = mensajes.find({}, {"message": 1})

    for m in msjes:
        for p in palabras:
            if p in m["message"]:
                resultado.append(m["message"])
                break

    return json.jsonify(resultado)

@app.route("/buscador3")
def buscador3():
    return render_template("buscador3.html")


#Agregar una o mas frases que si o si deban estar en el mensaje
@app.route("/buscador3", methods = ["POST"])
def buscador33():
    frase = request.form["palabra"]
    id = request.form["id"]
    palabras = str(frase).split()
    resultado = []

    if id:
        msjes = mensajes.find({"sender": int(id)}, {"message": 1})
    else:
        msjes = mensajes.find({}, {"message": 1})

    for m in msjes:
        for p in palabras:
            if p in m["message"]:
                break
        else:
            resultado.append(m["message"])
    return json.jsonify(resultado)

# Agregar una o mas frases que si o si deban estar en el mensaje
@app.route("/search/sms=<string:sms>", defaults={'uid': False}, methods=[
    "GET"])
@app.route("/search/<int:uid>/sms=<string:sms>", methods=["GET"])
def buscador_general(uid, sms):
    if uid:
        id = request.form["id"]
    else:
        id = False
    opcionales = [""]
    prohibidas = [""]
    necesarias = str(sms).split("&&")
    if necesarias[-1]:
        opcionales = str(necesarias[-1]).split("||")
        if opcionales[-1]:
            prohibidas = str(opcionales[-1]).split("¬¬")
    resultado = []
    print("Pasa algo?")
    if id:
        if len(necesarias) >=1 and len(opcionales)>1 and len(prohibidas)>1:
            msjes = mensajes.find({"$and":[{"sender": int(id)},
                                           {"$all": necesarias[:-1]},
                                           {"$in":opcionales[:-1]},
                                           {"$nin":prohibidas[:-1]}]},
                                  {"_id": 0})
        elif len(necesarias) >= 1 and len(opcionales)==1 and len(prohibidas)>1:
            msjes = mensajes.find({"$and": [{"sender": int(id)},
                                            {"$all": necesarias[:-1]},
                                            {"$nin": prohibidas[:-1]}]},
                                  {"_id": 0})
        elif len(necesarias) >= 1 and len(opcionales) > 1 and len(prohibidas) \
                ==1:
            msjes = mensajes.find({"$and": [{"sender": int(id)},
                                            {"$all": necesarias[:-1]},
                                            {"$in": opcionales[:-1]}]},
                                  {"_id": 0})
        elif len(necesarias) >= 1 and len(opcionales) ==1 and len(prohibidas) \
                ==1:
            msjes = mensajes.find({"$and": [{"sender": int(id)},
                                            {"$all": necesarias[:-1]}]},
                                  {"_id": 0})
        else:
            msjes = mensajes.find({}, {"_id": 0})

    # print("se printe", request.form["palabra"])
    #
    # for m in msjes:
    #     for p in palabras:
    #         if p in m["message"]:
    #             break
    #     else:
    #         resultado.append(m["message"])
    resultado = [u for u in msjes]
    return json.jsonify(resultado)


@app.route("/")
def home():
    return "<h1>HELLO</h1>"

# Mapeamos esta función a la ruta '/plot' con el método get.
@app.route("/plot")
def plot():
    # Obtengo todos los usuarios
    users = usuarios.find({}, {"_id": 0})

    # Hago un data frame (tabla poderosa) con la columna 'name' indexada
    df = pd.DataFrame(list(users)).set_index('name')

    # Hago un grafico de pi en base a la edad
    df.plot.pie(y='age')

    # Export la figura para usarla en el html
    pth = os.path.join('static', 'plot.png')
    plt.savefig(pth)

    # Retorna un html "rendereado"
    return render_template('plot.html')


@app.route("/users")
def get_users():
    request.args.get()
    resultados = [u for u in usuarios.find({}, {"_id": 0})]
    # Omitir el _id porque no es json serializable

    return json.jsonify(resultados)


@app.route("/users/<int:uid>")
def get_user(uid):
    users = list(usuarios.find({"uid": uid}, {"_id": 0}))
    return json.jsonify(users)


@app.route("/users", methods=['POST'])
def create_user():
    '''
    Crea un nuevo usuario en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''

    # Si los parámetros son enviados con una request de tipo application/json:
    data = {key: request.json[key] for key in USER_KEYS}

    # Se genera el uid
    count = usuarios.count_documents({})
    data["uid"] = count + 1

    # Insertar retorna un objeto
    result = usuarios.insert_one(data)

    # Creo el mensaje resultado
    if result:
        message = "1 usuario creado"
        success = True
    else:
        message = "No se pudo crear el usuario"
        success = False

    # Retorno el texto plano de un json
    return json.jsonify({'success': success, 'message': message})


@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    '''
    Elimina un usuario de la db.
    Se requiere llave uid
    '''

    # esto borra el primer resultado. si hay mas, no los borra
    usuarios.delete_one({"uid": uid})

    message = f'Usuario con id={uid} ha sido eliminado.'

    # Retorno el texto plano de un json
    return json.jsonify({'result': 'success', 'message': message})


@app.route('/users/many', methods=['DELETE'])
def delete_many_user():
    '''
    Elimina un varios usuarios de la db.
    - Se requiere llave idBulk en el body de la request application/json
    '''

    if not request.json:
        # Solicitud faltan parametros. Codigo 400: Bad request
        abort(400)  # Arrojar error

    all_uids = request.json['uidBulk']

    if not all_uids:
        # Solicitud faltan parametros. Codigo 400: Bad request
        abort(400)  # Arrojar error

    # Esto borra todos los usuarios con el id dentro de la lista
    result = usuarios.delete_many({"uid": {"$in": all_uids}})

    # Creo el mensaje resultado
    message = f'{result.deleted_count} usuarios eliminados.'

    # Retorno el texto plano de un json
    return json.jsonify({'result': 'success', 'message': message})


@app.route("/test")
def test():
    # Obtener un parámero de la URL
    param = request.args.get('name', False)
    print("URL param:", param)

    # Obtener un header
    param2 = request.headers.get('name', False)
    print("Header:", param2)

    # Obtener el body
    body = request.data
    print("Body:", body)

    return "OK"


#if os.name == 'nt':
app.run()
