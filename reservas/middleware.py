import logging

# este nombre es el configurado en LOGGING (settings.py): escribe en peticiones.log
logger = logging.getLogger("reservas.peticiones")


# Fase 4: middleware que apunta una línea por cada petición
class RegistroPeticionesMiddleware:
    # se ejecuta una vez al arrancar; get_response es el siguiente paso de la cadena
    def __init__(self, get_response):
        self.get_response = get_response

    # se ejecuta en cada petición
    def __call__(self, request):
        # antes de esta línea es la ida; después, la respuesta ya está hecha
        response = self.get_response(request)
        # sin sesión (o sin token válido) se apunta como anonimo
        usuario = request.user.username if request.user.is_authenticated else "anonimo"
        logger.info(f"{request.method} {request.path} {response.status_code} {usuario}")
        return response
