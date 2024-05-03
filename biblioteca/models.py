from django.db import models
from django.contrib.auth.models import User


class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=13)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    ano_publicacion = models.IntegerField()
    categoria = models.CharField(max_length=50)

    #Campo para saber la disponibilidad del libro
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_devolucion = models.DateField()

    # Campo adicional para marcar si el libro ha sido devuelto
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario}"


class Devolucion(models.Model):
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE)
    fecha_devolucion = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Devolución de {self.prestamo.libro.titulo} por {self.prestamo.usuario}"
