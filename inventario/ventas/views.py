from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import transaction 
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Venta, ItemVenta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import MovimientoStock
from .forms import VentaForm
from django.shortcuts import redirect


class VentaPDFView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ItemVenta
    template_name = "ventas/venta_pdf.html"
    context_object_name = "items_venta"
    permission_required = "ventas.view_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

    def get_queryset(self):
        venta_id = self.kwargs['pk']
        return ItemVenta.objects.filter(venta__id=venta_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta_id = self.kwargs['pk']
        context['venta'] = Venta.objects.get(id=venta_id)
        return context

class VentaListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Venta
    template_name = "ventas/venta_list.html"
    context_object_name = "ventas"
    paginate_by = 5
    permission_required = "ventas.view_venta"
        
    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())


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
        
class VentaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("productos:producto_list")
    permission_required = "ventas.add_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

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
                if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                    continue
                detalle = form.save(commit=False)
                detalle.venta = venta
                detalle.sub_total = detalle.cantidad * detalle.precio_unitario
                detalle.save()
                total += detalle.sub_total
                producto= detalle.producto
                if producto.stock < detalle.cantidad:
                    messages.error(self.request, f"No hay suficiente stock para el producto {producto.nombre}.")
                    venta.delete()
                    return self.render_to_response(self.get_context_data(form=form))
                if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                    continue

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
            messages.success(self.request, "Venta creada exitosamente.")
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

class VentaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("ventas:venta_list") # Esta URL de éxito final se usará si todo va bien
    permission_required = "ventas.change_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        # Permiso adicional para el grupo 'Ventas'
        return super().has_permission() and self.request.user.groups.filter(name='Ventas').exists()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Venta actualizada exitosamente.")
        return response   

class VentaDetailView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = ItemVenta
    template_name = "ventas/venta_detail.html"
    context_object_name = "items_venta"
    permission_required = "ventas.view_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

    def get_queryset(self):
        venta_id = self.kwargs['pk']
        return ItemVenta.objects.filter(venta__id=venta_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta_id = self.kwargs['pk']
        context['venta'] = Venta.objects.get(id=venta_id)
        return context
    
class VentaDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Venta
    template_name = "ventas/venta_confirm_delete.html"
    success_url = reverse_lazy("ventas:venta_list")
    permission_required = "ventas.delete_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

    def delete(self, request, *args, **kwargs):
        venta = self.get_object()
        items_venta = ItemVenta.objects.filter(venta=venta)

        for item in items_venta:
            producto = item.producto
            producto.stock += item.cantidad
            producto.save()

            MovimientoStock.objects.create(
                producto=producto,
                cantidad=item.cantidad,
                tipo='ANULACION_VENTA',
                fecha=timezone.now()
            )

        messages.success(self.request, "Venta eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)
    
    
