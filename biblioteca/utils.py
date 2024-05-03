from functools import wraps
from rest_framework.response import Response

# Definición del decorador para manejar errores
def handle_errors(func):
    @wraps(func)  # Preserva los metadatos de la función original
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Ejecuta la función original
        except Exception as e:
            # Devuelve una respuesta de error con el mensaje de la excepción
            return Response({'error': str(e)}, status=400)
    return wrapper

# Clase para el observador de eventos
class EventObserver:
    def __init__(self):
        self.handlers = []  # Lista para almacenar los manejadores de eventos

    # Método para registrar un nuevo manejador de eventos
    def register_handler(self, handler):
        self.handlers.append(handler)

    # Método para notificar a todos los manejadores registrados cuando ocurre un evento
    def notify(self, event):
        for handler in self.handlers:
            handler(event)