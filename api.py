import time
from flask import Flask, request, jsonify
from main import *
app = Flask(__name__)
import sys

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return 'Api web service - divisist asistance'
    
@app.route('/api/v1.0/get-notas-materias', methods=['POST'])
def get_notas_materias():
    session = initialize()
    app.logger.info(request.form['usuario'])
    usuario = request.form.get('usuario')
    password = request.form.get('password')
    documento = request.form.get('documento')
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
    if iniciar_sesion(session, payload):    
        nombres_materias = get_nombres_materias(session)
        notas_parciales = get_notas_parciales(session)
        map_result = {}
        i=0
        for materia in nombres_materias:
            map_result[materia] = notas_parciales[i]
            i+=1
        cerrar_sesion(session)
        return jsonify(success=True, result=map_result)
    return jsonify(succes=False)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
