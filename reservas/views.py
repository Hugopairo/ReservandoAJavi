# reservas/views.py
from django.http import Http404
from django.shortcuts import render

ESPACIOS = [
    {"id": 1, "nombre": "Aula 12", "tipo": "aula", "aforo": 30},
    {"id": 2, "nombre": "Laboratorio de Física", "tipo": "laboratorio", "aforo": 24},
    {"id": 3, "nombre": "Salón de actos", "tipo": "salon", "aforo": 200},
]


def buscar(pk):
    for espacio in ESPACIOS:
        if espacio["id"] == pk:
            return espacio
    raise Http404("El espacio no existe")


def lista(request):
    return render(request, "reservas/lista.html", {"espacios": ESPACIOS})


def detalle(request, pk):
    return render(request, "reservas/detalle.html", {"espacio": buscar(pk)})
