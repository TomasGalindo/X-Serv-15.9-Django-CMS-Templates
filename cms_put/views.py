from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
# Create your views here.
from cms_put.models import Page
from django.template.loader import get_template
from django.template import Context


def login_info(request):
    if request.user.is_authenticated():
        respuesta = "<p>Logged in as " + request.user.username + "<a href='/logout'> Logout </a></p>"
    else:
        respuesta = "<p>Not Logged in. <a href='/login/'> Login </a></p>"
    return respuesta


def writeBase(request):
    respuesta = '<h1>PAGES</h1>'
    lista_paginas = Page.objects.all()
    for pagina in lista_paginas:
        respuesta += "<p><a href='" + pagina.name + "'>"+ pagina.name + "</a></p>"

    template = get_template("hifi_news/index.html")
    c = Context({'title': 'Listado de las paginas que tienes guardadas.', 'content': respuesta, 'login_info': login_info(request)})
    respuesta = template.render(c)

    return HttpResponse(respuesta)

# BUSCANDO A TRAVES DEL IDENTIFICADOR
@csrf_exempt
def pagina(request, nameRecurso):
    if request.method == "GET":
        # Buscar en la base de datos
        try:
            pagina = Page.objects.get(name=nameRecurso)
            # si existe
            respuesta = "Pagina que has pedido: " + pagina.page
        except Page.DoesNotExist:
            # no existe
            respuesta = "<p>No existe la pagina " + nameRecurso + "<p>"
    elif request.method == "PUT":
        if request.user.is_authenticated():
            # busco por el nombre
            # obligo a que no se puedan repetir los recursos
            try:
                Pagina = Page.objects.get(name=nameRecurso)
                # Ya existe la pagina
                respuesta = ("No se puede añadir porque ya existe")
            except Page.DoesNotExist:
                campoPagina = request.body.decode('utf-8')
                pagina = Page(name=nameRecurso, page=campoPagina)
                pagina.save()
                respuesta = "He detectado un PUT, Guardado"
            else:
                respuesta = "NO PUEDES HACERLO"
            
    else:
        respuesta = "NO PUEDES HACER ESTA OPERACION"


    template = get_template("hifi_news/index.html")
    c = Context({'title': 'Listado de las paginas que tienes guardadas.', 'content': respuesta, 'login_info': login_info(request)})
    respuesta = template.render(c)

    return HttpResponse(respuesta)
