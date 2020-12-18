from bs4 import BeautifulSoup
import requests
import codecs


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
