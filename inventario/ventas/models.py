from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone

class Venta(models.Model):
    codigo_venta = models.DecimalField("Codigo de venta", max_digits=20)
    cliente = models.ForeignKey("Cliente", max_length=20)
    fecha_venta = models.DateTimeField("Fecha de la venta", auto_now_add=True)
    total = models.IntegerField("Precio total de la venta", max_length=10)

class ItemVenta(models.Model):
    venta = models.ForeignKey("Venta", on_delete=models.CASCADE, related_name="Items")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE )
    cantidad = models.PositiveIntegerField("Cantidad", default=1)
    precio_unitario = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    sub_total = models.PositiveIntegerField("Subtotal", max_digits=10, decimal_places = 2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} * {self.producto.nombre}"