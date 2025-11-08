from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Venta, ItemVenta
from productos.models import Producto, MovimientoStock
from .forms import VentaForm
from django.shortcuts import redirect

class VentaListView(ListView):
    model = Venta
    template_name = "ventas/venta_list.html"
    context_object_name = "ventas"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=search_query) |
                Q(codigo__icontains=search_query)
            )

        return queryset.order_by("-fecha")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context
        
class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("productos:producto_list")

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            venta = form.save(commit= False)
            venta.fecha_venta = timezone.now()
            venta.total = 0
            venta.save()

            total = 0
            for form in formset:
                detalle = form.save(commit=False)
                detalle.venta = venta
                detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                detalle.save()
                total += detalle.subtotal

                # Actualizar el stock del producto
                producto = detalle.producto
                producto.stock -= detalle.cantidad
                producto.save()

                # Registrar el movimiento de stock
                MovimientoStock.objects.create(
                    producto=producto,
                    cantidad=-detalle.cantidad,
                    tipo='VENTA',
                    fecha=timezone.now()
                )
            venta.total = total
            venta.save()
            messages.success(self.request, "Venta registrada exitosamente.")
            return redirect('ventas:venta_detail', pk=venta.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            from .forms import VentaDetalleFormSet
            context['formset'] = VentaDetalleFormSet(self.request.POST)
        else:
            from .forms import VentaDetalleFormSet
            context['formset'] = VentaDetalleFormSet()
        return context


class VentaUpdateView(UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("ventas:venta_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Venta actualizada exitosamente")
        return response
    
    
