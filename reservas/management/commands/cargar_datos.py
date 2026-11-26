from datetime import date, time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from reservas.models import Espacio, Reserva

# Datos de prueba del guion (fase 6)

# (nombre de usuario, es personal)
USUARIOS = [
    ("profe1", False),
    ("profe2", False),
    ("conserje", True),
]

# (nombre, tipo, aforo, activo) -> el orden importa: serán los id 1 a 5
ESPACIOS = [
    ("Aula 12", "aula", 30, True),
    ("Laboratorio de Física", "laboratorio", 24, True),
    ("Salón de actos", "salon", 200, True),
    ("Pista polideportiva", "pista", 60, True),
    ("Aula 3", "aula", 25, False),
]

# (espacio, fecha, hora de inicio, hora de fin, usuario, estado, motivo)
RESERVAS = [
    (
        "Aula 12",
        date(2027, 5, 20),
        time(9, 0),
        time(10, 0),
        "profe1",
        "confirmada",
        "Examen de Matemáticas",
    ),
    (
        "Aula 12",
        date(2027, 5, 20),
        time(10, 0),
        time(11, 0),
        "profe2",
        "confirmada",
        "Tutoría de 2.º DAW",
    ),
    (
        "Salón de actos",
        date(2027, 5, 20),
        time(12, 0),
        time(14, 0),
        "profe1",
        "pendiente",
        "Charla de orientación",
    ),
    (
        "Laboratorio de Física",
        date(2027, 5, 24),
        time(8, 30),
        time(10, 20),
        "profe2",
        "confirmada",
        "Práctica de óptica",
    ),
    (
        "Pista polideportiva",
        date(2027, 5, 24),
        time(11, 15),
        time(12, 10),
        "profe1",
        "cancelada",
        "Torneo de recreo",
    ),
    (
        "Aula 12",
        date(2027, 5, 24),
        time(9, 0),
        time(10, 0),
        "profe1",
        "pendiente",
        "Recuperación",
    ),
]


class Command(BaseCommand):
    help = "Borra las reservas y carga los datos de prueba"

    def handle(self, *args, **options):
        # Paso 1: borrar todas las reservas para no duplicarlas al repetir la orden
        Reserva.objects.all().delete()

        # Paso 2: usuarios
        # Diccionario para recuperar luego cada usuario por su nombre
        usuarios = {}
        # primera vuelta: nombre = "profe1", es_personal = False
        for nombre, es_personal in USUARIOS:
            # lo busca por username y, si no existe, lo crea usando también defaults
            usuario, creado = User.objects.get_or_create(
                username=nombre, defaults={"is_staff": es_personal}
            )
            usuario.set_password("Clave.2026")  # guarda la contraseña cifrada
            usuario.save()  # lo guarda en la base de datos
            usuarios[nombre] = usuario  # clave: el nombre; valor: el usuario

        # Paso 3: espacios
        # Diccionario para recuperar luego cada espacio por su nombre
        espacios = {}
        # se crean en el orden de la lista (importa para los id 1 a 5)
        for nombre, tipo, aforo, activo in ESPACIOS:
            # lo busca por nombre: si existe lo actualiza con defaults y si no, lo crea
            # el _ indica que no uso el dato de si se ha creado o no
            espacio, _ = Espacio.objects.update_or_create(
                nombre=nombre, defaults={"tipo": tipo, "aforo": aforo, "activo": activo}
            )
            espacios[nombre] = espacio  # clave: el nombre; valor: el espacio

        # Paso 4: reservas
        # cada fila de RESERVAS se reparte en 7 variables, en el mismo orden
        for (
            espacio_nombre,
            fecha,
            hora_inicio,
            hora_fin,
            usuario_nombre,
            estado,
            motivo,
        ) in RESERVAS:
            # en la lista solo tengo los nombres: saco los objetos de mis diccionarios
            espacio = espacios.get(espacio_nombre)
            usuario = usuarios.get(usuario_nombre)
            # create crea y guarda la reserva (no hay duplicados por el paso 1)
            Reserva.objects.create(
                espacio=espacio,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                usuario=usuario,
                estado=estado,
                motivo=motivo,
            )

        # Paso 5: mensaje final (fuera del for, para que salga una sola vez)
        self.stdout.write("Cargados 5 espacios y 6 reservas")
