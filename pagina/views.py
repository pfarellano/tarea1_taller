from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import requests
def home(request):

    lista_tuplas=[]

    respuesta1=requests.get('https://rickandmortyapi.com/api/episode/')
    respuesta1_en_json=respuesta1.json()
    lista1_episodios=respuesta1_en_json['results']
    for elemento in lista1_episodios:
        tupla=(elemento["id"],elemento["name"],elemento["air_date"],elemento["episode"])
        lista_tuplas.append(tupla)
    while respuesta1_en_json["info"]["next"]!="":
        respuesta1 = requests.get('https://rickandmortyapi.com/api/episode/?page=2')
        respuesta1_en_json = respuesta1.json()
        lista1_episodios = respuesta1_en_json['results']
        for elemento in lista1_episodios:
            tupla = (elemento["id"],elemento["name"], elemento["air_date"], elemento["episode"])
            lista_tuplas.append(tupla)


    return render(request, 'home.html', {"lista_tuplas":lista_tuplas})

def episodio(request, id):
    url_total="https://rickandmortyapi.com/api/episode/"+id
    respuesta = requests.get(url_total)
    respuesta_json=respuesta.json()
    nombre= respuesta_json["name"]
    fecha_al_aire= respuesta_json["air_date"]
    episodio=respuesta_json["episode"]
    personajes=respuesta_json["characters"]
    diccionario_personajes={}
    for person in personajes:
        lista_split=person.split("/")
        numero_person=lista_split[-1]
        respuesta2 = requests.get(person)
        respuesta2_json = respuesta2.json()
        nombre_personaje=respuesta2_json["name"]
        diccionario_personajes[nombre_personaje]=numero_person

    return render(request, "episodio.html", {"nombre":nombre,"fecha_al_aire":fecha_al_aire, "episodio":episodio, "personajes":diccionario_personajes})


def personaje(request, ur):
    url_total="https://rickandmortyapi.com/api/character/"+ur
    respuesta = requests.get(url_total)
    respuesta_json = respuesta.json()
    nombre = respuesta_json["name"]
    estado=respuesta_json["status"]
    especie=respuesta_json["species"]
    tipo=respuesta_json["type"]
    genero=respuesta_json["gender"]
    origen=respuesta_json["origin"]["name"]
    numero_origen=0
    if origen=="unknown":
        origen="1"
    else:
        lista_split_origen = respuesta_json["origin"]["url"].split("/")
        numero_origen = lista_split_origen[-1]

    locacion=respuesta_json["location"]["name"]
    lista_split_locacion = respuesta_json["location"]["url"].split("/")
    numero_locacion = lista_split_locacion[-1]
    imagen=respuesta_json["image"]
    episodios=respuesta_json["episode"]
    diccionario_episodios={}
    for epi in episodios:
        lista_split = epi.split("/")
        numero_episodio = lista_split[-1]
        respuesta=requests.get(epi)
        respuesta_json = respuesta.json()
        nombre_episodio = respuesta_json["name"]
        diccionario_episodios[nombre_episodio] = numero_episodio


    return render(request, "personaje.html", {"nombre": nombre, "estado":estado,"especie":especie, "tipo":tipo, "genero":genero, "origen":origen, "numero_origen":numero_origen,"numero_locacion":numero_locacion, "locacion":locacion, "imagen":imagen, "episodios":diccionario_episodios})


def lugar(request, id):
    url_total="https://rickandmortyapi.com/api/location/"+id
    respuesta = requests.get(url_total)
    respuesta_json = respuesta.json()
    nombre = respuesta_json["name"]
    tipo=respuesta_json["type"]
    dimension=respuesta_json["dimension"]
    residentes=respuesta_json["residents"]
    diccionario_residentes={}


    for resi in residentes:
        lista_split = resi.split("/")
        numero_residente= lista_split[-1]
        respuesta=requests.get(resi)
        respuesta_json = respuesta.json()
        nombre_resi = respuesta_json["name"]
        diccionario_residentes[nombre_resi] = numero_residente

    return render(request, "lugar.html", {"nombre": nombre,  "tipo":tipo, "dimension":dimension, "residentes":diccionario_residentes})



def busqueda(request):
    query = request.GET.get('q')

    diccionario_nombres_episodios={}
    todos_los_episodios = requests.get('https://rickandmortyapi.com/api/episode/')
    respuesta_episodios= todos_los_episodios.json()
    lista_episodios=respuesta_episodios["results"]
    for episodio in lista_episodios:
        nombre_episodio=episodio["name"]
        if query in nombre_episodio:
            lista_palabras=episodio["url"].split("/")
            numero_episodio=lista_palabras[-1]
            diccionario_nombres_episodios[nombre_episodio]=numero_episodio
        else:
            continue


    pagina_siguiente_e =respuesta_episodios["info"]["next"]
    while pagina_siguiente_e != "":
        todos_los_episodios = requests.get(pagina_siguiente_e)
        respuesta_episodios=todos_los_episodios.json()
        lista_episodios=respuesta_episodios["results"]
        pagina_siguiente_e = respuesta_episodios["info"]["next"]
        for episodio in lista_episodios:
            nombre_episodio = episodio["name"]
            if query in nombre_episodio:
                lista_palabras = episodio["url"].split("/")
                numero_episodio = lista_palabras[-1]
                diccionario_nombres_episodios[nombre_episodio] = numero_episodio
            else:
                continue




    diccionario_nombres_personajes = {}
    todos_los_personajes = requests.get('https://rickandmortyapi.com/api/character/')
    respuesta_personajes= todos_los_personajes.json()
    lista_personajes = respuesta_personajes["results"]
    for personaje in lista_personajes:
        nombre_personaje = personaje["name"]
        if query in nombre_personaje:
            lista_palabras = personaje["url"].split("/")
            numero_personaje = lista_palabras[-1]
            diccionario_nombres_personajes[nombre_personaje] = numero_personaje
        else:
            continue


    pagina_siguiente_p = respuesta_personajes["info"]["next"]
    while pagina_siguiente_p != "":
        todos_los_personajes = requests.get(pagina_siguiente_p)
        respuesta_personajes = todos_los_personajes.json()
        lista_personajes = respuesta_personajes["results"]
        pagina_siguiente_p = respuesta_personajes["info"]["next"]
        for personaje in lista_personajes:
            nombre_personaje = personaje["name"]
            if query in nombre_personaje:
                lista_palabras = personaje["url"].split("/")
                numero_personaje = lista_palabras[-1]
                diccionario_nombres_personajes[nombre_personaje] = numero_personaje
            else:
                continue





    diccionario_nombres_lugares = {}
    todos_los_lugares = requests.get('https://rickandmortyapi.com/api/location/')
    respuesta_lugares = todos_los_lugares.json()
    lista_lugares = respuesta_lugares["results"]
    for lugar in lista_lugares:
        nombre_lugar = lugar["name"]
        if query in nombre_lugar:
            lista_palabras = lugar["url"].split("/")
            numero_lugar = lista_palabras[-1]
            diccionario_nombres_lugares[nombre_lugar] = numero_lugar
        else:
            continue

    pagina_siguiente_l = respuesta_lugares["info"]["next"]
    while pagina_siguiente_l != "":
        todos_los_lugares = requests.get(pagina_siguiente_l)
        respuesta_lugares = todos_los_lugares.json()
        lista_lugares = respuesta_lugares["results"]
        pagina_siguiente_l = respuesta_lugares["info"]["next"]
        for lugar in lista_lugares:
            nombre_lugar = lugar["name"]
            if query in nombre_lugar:
                lista_palabras = lugar["url"].split("/")
                numero_lugar = lista_palabras[-1]
                diccionario_nombres_lugares[nombre_lugar] = numero_lugar
            else:
                continue





    return render(request, "busqueda.html", {"palabra":query, "episodios":diccionario_nombres_episodios, "personajes":diccionario_nombres_personajes, "lugares":diccionario_nombres_lugares})
