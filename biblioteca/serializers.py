from rest_framework import serializers
from .models import Libro, Prestamo

# Serializador para el modelo Libro
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id','isbn', 'titulo', 'autor', 'ano_publicacion', 'categoria']

# Serializador para el modelo Prestamo
class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'



