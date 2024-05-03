from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Libro, Prestamo, Devolucion
from .serializers import LibroSerializer, PrestamoSerializer
from .utils import handle_errors, EventObserver

# Instancia del observador
event_observer = EventObserver()

def handle_prestamo_event(event):
    # Eventos relacionados con los préstamos
    print(f"Evento de préstamo registrado: {event}")

def handle_devolucion_event(event):
    # Eventos relacionados con las devoluciones
    print(f"Evento de devolución registrado: {event}")

# Se registran los eventos en el observador
event_observer.register_handler(handle_prestamo_event)
event_observer.register_handler(handle_devolucion_event)

@api_view(['POST'])
@handle_errors
def agregar_libro_al_sistema(request):
    # Vista para agregar un nuevo libro 
    if request.method == 'POST':
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@handle_errors
def buscar_libros(request, param, category=None):
    # Vista para buscar libros
    if request.method == 'GET':
        libros = Libro.objects.filter(
            titulo__icontains=param
        ) | Libro.objects.filter(
            autor__icontains=param
        ) | Libro.objects.filter(
            isbn=param
        )

        if category:
            libros = libros.filter(categoria=category)

        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({'error': 'Método no permitido'}, status=405)

@api_view(['POST'])
@handle_errors
def realizar_prestamo(request):
    # Vista para realizar un préstamo
    if request.method == 'POST':
        serializer = PrestamoSerializer(data=request.data)
        if serializer.is_valid():
            libro_id = request.data.get('libro')
            try:
                libro = Libro.objects.get(id=libro_id)
                if not libro.disponible:
                    return Response({'error': 'El libro no está disponible para préstamo'}, status=400)
            except Libro.DoesNotExist:
                return Response({'error': 'El libro no existe'}, status=400)

            prestamo = serializer.save()
            libro.disponible = False
            libro.save()

            # Notificar al observador sobre el nuevo préstamo
            event_observer.notify(f"Nueva solicitud de préstamo: {prestamo}")

            return Response(PrestamoSerializer(prestamo).data, status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['PUT'])
@handle_errors
def devolucion_libro(request, prestamo_id):
    # Vista para registrar la devolución
    if request.method == 'PUT':
        prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
        if prestamo.devuelto:
            return Response({'error': 'El préstamo ya ha sido devuelto'}, status=400)

        devolucion = Devolucion(prestamo=prestamo)
        prestamo.devuelto = True
        prestamo.save()

        # Actualizar el estado del libro a disponible
        prestamo.libro.disponible = True
        prestamo.libro.save()

        devolucion.save()

        # Notificar al observador sobre la devolución
        event_observer.notify(f"Devolución registrada: {prestamo}")

        serializer = PrestamoSerializer(prestamo)
        return Response(serializer.data, status=200)
    else:
        return Response({'error': 'Método no permitido'}, status=405)

