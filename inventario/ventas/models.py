from django.db import models
from django.utils import timezone
from productos.models import Producto
from cliente.models import Cliente

class Venta(models.Model):
    codigo = models.CharField("Codigo de venta", max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateTimeField("Fecha de venta", default=timezone.now)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.codigo} - {self.fecha.date()} - {self.total}"
    
class ItemVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField("Cantidad")
    precio_unitario = models.DecimalField("Precio unitario", max_digits=10, decimal_places=2)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} x {self.precio_unitario}"
    
class MovimientoStock(models.Model):

    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos_stock')
    cantidad = models.IntegerField("Cantidad")
    fecha = models.DateTimeField("Fecha del movimiento", default=timezone.now)
    tipo = models.CharField("Tipo de movimiento", max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')])
    usuario = models.CharField("Usuario", max_length=50)
    motivo = models.CharField("Motivo", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Movimiento de stock"
        verbose_name_plural = "Movimiento de stocks"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad} - {self.fecha.date()}"
