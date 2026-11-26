from rest_framework import permissions


# Fase 10: un permiso devuelve True (se permite) o False (se deniega)
class EsPersonalOSoloLectura(permissions.BasePermission):
    # se ejecuta en todas las peticiones, también en las altas (aún no hay objeto)
    def has_permission(self, request, view):
        # SAFE_METHODS son las de lectura: GET, HEAD y OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # para escribir: identificado y del personal
        return request.user.is_authenticated and request.user.is_staff


# permiso sobre una reserva concreta
class EsPropietarioOSoloLectura(permissions.BasePermission):
    # obj es la reserva; solo se ejecuta cuando hay un objeto (ver, modificar, borrar)
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # solo su propietario puede modificarla o borrarla
        return obj.usuario == request.user
