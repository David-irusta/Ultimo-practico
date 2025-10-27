from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Producto, Venta, MovimientoStock
from .forms import VentaForm

class VentaListView(ListView):
    model = Producto
    template_name = "ventas/venta_list.html"
    context_object_name = "productos"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(codigo__icontains=search_query)
            )

        return queryset.order_by("nombre")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context
    
    
class VentaDetailView(DetailView):
    model = Venta
    template_name = "ventas/venta_detail.html"
    context_object_name = "producto"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movimientos = getattr(self.object, "movimientos", None)
        if movimientos:
            context["movimientos"] = movimientos.all()[:10]
        else:
            context["movimientos"] = []
        return context
        
class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("productos:producto_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Crear el detalle de venta y actualizar stock
        items = form.cleaned_data.get('items', [])
        for item in items:
            VentaDetailView.objects.create(
                venta=self.object,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['producto'].precio
            )
            
            # Registrar movimiento de stock (salida)
            MovimientoStock.objects.create(
                producto=item['producto'],
                tipo="salida",
                cantidad=item['cantidad'],
                motivo="Venta #" + str(self.object.id),
                fecha=timezone.now(),
                usuario=self.request.user.username if self.request.user.is_authenticated else "Sistema"
            )

        messages.success(self.request, "Venta registrada exitosamente")
        return response
    
    def agregar_carrito(self, request, *args, **kwargs):
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))
        producto = Producto.objects.get(id=producto_id)

        carrito = request.session.get("carrito", {})
        if producto_id in carrito:
            carrito[producto_id] += cantidad
        else:
            carrito[producto_id] = cantidad

        request.session["carrito"] = carrito
        messages.success(request, f"Producto {producto.nombre} agregado al carrito.")
        return self.get(request, *args, **kwargs)
    
    def ver_carrito(self, request, *args, **kwargs):
        carrito = request.session.get("carrito", {})
        productos = []
        total = 0
        for producto_id, cantidad in carrito.items():
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            productos.append({
                "producto": producto,
                "cantidad": cantidad,
                "subtotal": subtotal
            })
            total += subtotal

        context = {
            "productos": productos,
            "total": total
        }
        return render(request, "ventas/venta_list.html", context)