import time
from flask import Flask, render_template, request, jsonify, make_response, session
from flask_cors import CORS, cross_origin
import os
from .main import *
from flask_session import Session
import redis

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.before_request
def session_management():
  session.permanent = True

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return 'Api web service - divisist asistance'

@app.route("/api/v1.0/login", methods=['OPTIONS', 'POST'])
@cross_origin()
def login():
    session.clear()
    if request.method == 'POST':
        usuario = request.json.get('usuario')
        password = request.json.get('password')
        documento = request.json.get('documento')
        documento2 = '*'*len(documento)
        payload = {
            'login':'1', 
            'miip':'',
            'miipreal':'',
            'usuario':usuario,
            'documento2':documento2,
            'password':password,
            'documento':documento,
        }
        session_ = initialize()
        if iniciar_sesion(session_, payload):  
            session["usuario"] = usuario
            session["password"] = password
            session["documento"] = documento
            session["auth"] = 1
            cerrar_sesion(session_)
            return jsonify(succes=True)
        
        session["auth"] = 0
        return jsonify(succes=False)

@app.route("/api/v1.0/logout", methods=['POST'])
def logout():
    session.clear()
    session["user"] = "unknown"
    session["auth"] = 0
    return jsonify(succes=True)


@app.route('/api/v1.0/get-notas-materias', methods=['GET'])
def get_notas_materias():
    try:
        usuario = session["usuario"]
        password = session["password"]
        documento = session["documento"]
        auth = session["auth"]
    except:
        auth = 0
    if auth == 0:
        return jsonify(succes=False)
         
    session_ = initialize()
    documento2 = '*'*len(documento)
    payload = {
        'login':'1', 
        'miip':'',
        'miipreal':'',
        'usuario':usuario,
        'documento2':documento2,
        'password':password,
        'documento':documento,
    }
    if iniciar_sesion(session_, payload):    
        nombres_materias = get_nombres_materias(session_)
        notas_parciales = get_notas_parciales(session_)
        map_result = {}
        i=0
        for materia in nombres_materias:
            map_result[materia] = notas_parciales[i]
            i+=1
        cerrar_sesion(session_)
        return jsonify(success=True, result=map_result)
    return jsonify(succes=False)

@app.route("/api/v1.0/get-nota-by-voice", methods=['POST'])
def get_nota_by_voice():
    data = request.json.get('data')
    value = request.json.get('value')    
    res = get_materia_by_value(data, value)
    if res:
        return jsonify(succes=True, result=res)
    return jsonify(succes=False)


if __name__ == '__main__':
    #secret key
    app.secret_key = os.environ.get('SECRET_KEY')
    CORS(app, support_credentials=True)

    #config session
    SESSION_TYPE = 'redis'
    app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
    sess = Session()
    sess.init_app(app)
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
