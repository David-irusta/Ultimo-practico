from django.db import models

class Cliente(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    apellido = models.CharField("Apellido", max_length=100)
    numero_documento = models.CharField("Numero de documento", max_length=20, unique=True)
    email = models.EmailField("Email", max_length=254, unique=True)
    telefono = models.CharField("Telefono", max_length=20)
    direccion = models.CharField("Direccion", max_length=200)

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.numero_documento}"
