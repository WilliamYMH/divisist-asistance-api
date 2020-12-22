from bs4 import BeautifulSoup
import requests
import codecs
from .utils import *

def initialize():
    session = requests.Session()
    return session


def iniciar_sesion(session, payload):
    try:
        session.post("https://divisist2.ufps.edu.co",
                     data=payload, verify=False)
        s_page = session.get(
            'https://divisist2.ufps.edu.co/informacion_academica/materias')
        soup = BeautifulSoup(s_page.text, 'html.parser')
        table = soup.find('table').find('tbody')
    except Exception as e:
        print(e)
        return False
    return True


def cerrar_sesion(session):
    try:
        session.get('https://divisist2.ufps.edu.co/index/logout')
    except Exception as e:
        print(e)
        return False
    return True


def get_notas_parciales(session):
    map_eq = {
        0: 'parcial1',
        1: 'parcial2',
        2: 'parcial3',
        3: 'examen',
        4: 'habilitacion',
        5: 'definitiva',
    }
    s_page = session.get(
        'https://divisist2.ufps.edu.co/informacion_academica/materias')
    soup = BeautifulSoup(s_page.text, 'html.parser')
    table = soup.find('table').find('tbody')

    notas_parciales = []
    notas = {}
    for row in table.findAll('tr'):
        col = row.findAll('td', {"class": "td_center"})
        if notas:
            notas_parciales.append(notas)
        notas = {}
        contador = 0
        for i in col:
            nombre = i.findAll('span')
            if(nombre and nombre[0] != '' and nombre[0].contents):
                if(str(nombre[0].contents[0]).strip() != '×'):
                    notas[map_eq.get(contador)] = str(
                        nombre[0].contents[0]).strip()
                    contador += 1

    return notas_parciales

def get_nota(value, materias):
    pass

def get_nombres_materias(session):
    try:
        s_page = session.get(
            'https://divisist2.ufps.edu.co/informacion_academica/materias')
        soup = BeautifulSoup(s_page.text, 'html.parser')
        table = soup.find('table').find('tbody')

        names_materias = []
        for row in table.findAll('tr'):
            col = row.findAll('td')
            for i in col:
                nombre = i.findAll(
                    'h4', {"class": "modal-title", "id": "myModalLabel"})
                if(nombre and nombre[0] != ''):
                    names_materias.append(str(nombre[0].contents[2]).strip())

        return names_materias
    except Exception as e:
        print(e)
        cerrar_sesion(session)

def get_lang_es():
    map_lang = {}
    map_lang['parcial1']='parcial1'
    map_lang['primer parcial']='parcial1'
    map_lang['parcial 1']='parcial1'
    map_lang['primerparcial']='parcial1'
    map_lang['primeroparcial']='parcial1'
    map_lang['1parcial']='parcial1'
    map_lang['1 parcial']='parcial1'
    map_lang['previo1']='parcial1'
    map_lang['primer previo']='parcial1'
    map_lang['previo 1']='parcial1'
    map_lang['primerprevio']='parcial1'
    map_lang['primeroprevio']='parcial1'
    map_lang['1previo']='parcial1'
    map_lang['1 previo']='parcial1'

    map_lang['parcial2']='parcial2'
    map_lang['segundo parcial']='parcial2'
    map_lang['parcial 2']='parcial2'
    map_lang['segundoparcial']='parcial2'
    map_lang['segundparcial']='parcial2'
    map_lang['2parcial']='parcial2'
    map_lang['2 parcial']='parcial2'
    map_lang['previo2']='parcial2'
    map_lang['segundo previo']='parcial2'
    map_lang['previo 2']='parcial2'
    map_lang['segundoprevio']='parcial2'
    map_lang['segundooprevio']='parcial2'
    map_lang['2previo']='parcial2'
    map_lang['2 previo']='parcial2'

    map_lang['parcial3']='parcial3'
    map_lang['tercer parcial']='parcial3'
    map_lang['parcial 3']='parcial3'
    map_lang['tercerparcial']='parcial3'
    map_lang['terceroparcial']='parcial3'
    map_lang['3parcial']='parcial3'
    map_lang['3 parcial']='parcial3'
    map_lang['previo3']='parcial3'
    map_lang['tercer previo']='parcial3'
    map_lang['previo 3']='parcial3'
    map_lang['tercerprevio']='parcial3'
    map_lang['terceroprevio']='parcial3'
    map_lang['3previo']='parcial3'
    map_lang['3 previo']='parcial3'

    map_lang['habilitacionde']='habilitacion'
    map_lang['habilitacion de']='habilitacion'
    map_lang['habilitacion']='habilitacion'

    map_lang['examen']='examen'
    map_lang['examen final']='examen'
    map_lang['examenfinal']='examen'

    map_lang['definitiva']='definitiva'

    return map_lang

def get_tipo_parcial_by_value(value):
    map_lang=get_lang_es()

    value_=value.strip().lower().split(' ')
    for n in range(1, len(value_)):
        res_=map_lang.get(value_[n-1]+value_[n])
        if res_:
            return res_

    for n in range(1, len(value_)):
        res_=map_lang.get(value_[n])
        if res_:
            return res_

    return ''

def get_map_materias(data):
    map_mat={}
    for key in data.keys():
        aux_k=key.split(' ')
        new_val=''
        for n in range(2, len(aux_k)):
            new_val+=aux_k[n]
        map_mat[new_val.lower()]=key
    
    return map_mat
 
def get_key_materia(data, value):
    a,b = 'áéíóúü','aeiouu'
    trans = str.maketrans(a,b)
    value_=value.strip().lower().translate(trans).split(' ')
    map_mat = get_map_materias(data)
    materia = ''
    flag=False
    for n in value_:
        if(flag):
            materia+=n
        if(n=='de'):
            flag=True
    max=0
    key_=''
    for key in map_mat.keys():
        s_=materia+'#'+key
        arr_=[0] * len(s_) 
        getZarr(s_, arr_)
        for x in arr_:
            if x > max:
                max=x
                key_=key
    if key_:
        return map_mat.get(key_)
    return ''

def get_materia_by_value(data, value):
    key_=get_key_materia(data, value)
    tipo_parcial=get_tipo_parcial_by_value(value)

    if key_ and tipo_parcial:
        notas = data.get(key_)
        return notas.get(tipo_parcial)
    return ''  

