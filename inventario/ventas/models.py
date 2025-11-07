from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone
from cliente.models import Cliente
from productos.models import Producto

class Venta(models.Model):
    codigo = models.IntegerField("Codigo de venta")
    cliente = models.ForeignKey("cliente.Cliente", on_delete=models.CASCADE, max_length=20)
    fecha = models.DateTimeField("Fecha de la venta", auto_now_add=True)
    total = models.IntegerField("Precio total de la venta", default=0)

class ItemVenta(models.Model):
    venta = models.ForeignKey("Venta", on_delete=models.CASCADE, related_name="Items")
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE )
    cantidad = models.PositiveIntegerField("Cantidad", default=1)
    precio_unitario = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    sub_total = models.DecimalField("Subtotal", max_digits=10, decimal_places = 2, editable=False, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} * {self.producto.nombre}"