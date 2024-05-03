from django.urls import path
from .views import * # Importa todas las vistas

urlpatterns = [
    # URL para agregar un libro al sistema
    path('api/agregar_libro/', agregar_libro_al_sistema),
    # URL para buscar libros por parámetro de búsqueda
    path('api/buscar_libro/<str:param>/', buscar_libros),
    # URL para buscar libros por parámetro de búsqueda y categoría
    path('api/buscar_libro/<str:param>/<str:category>/', buscar_libros),
    # URL para realizar un préstamo de libro
    path('api/realizar_prestamo/', realizar_prestamo),
    # URL para registrar la devolución de un libro
    path('api/devolucion/<int:prestamo_id>/', devolucion_libro),
]