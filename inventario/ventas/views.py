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
        codigo = self.request.GET.get("codigo")
        if codigo:
            queryset = queryset.filter(codigo__icontains=codigo)

        if search_query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=search_query) |
                Q(codigo__icontains=search_query)
            )

        return queryset.order_by("-fecha")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        context["search_query"] = self.request.GET.get("search", "")
        return context
        
class VentaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("ventas:venta_list")
    permission_required = "ventas.add_venta"
    paginate_by = 5

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return super().has_permission() and self.request.user.groups.filter(name='Ventas').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import VentaDetalleFormSet
        if self.request.POST:
            context['formset'] = VentaDetalleFormSet(self.request.POST)
        else:
            context['formset'] = VentaDetalleFormSet()
        
        # Agregar variable para el template
        context['modo_edicion'] = False
        context['titulo'] = 'Crear Venta'
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if form.is_valid() and formset.is_valid():
            # Guardar la venta primero
            self.object = form.save()
            # Luego guardar los items del formset
            formset.instance = self.object
            formset.save()
            self.object.calcular_total()
            
            messages.success(self.request, "Venta creada exitosamente.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class VentaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"
    success_url = reverse_lazy("ventas:venta_list")
    permission_required = "ventas.change_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return super().has_permission() and self.request.user.groups.filter(name='Ventas').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import VentaDetalleFormSet
        if self.request.POST:
            context['formset'] = VentaDetalleFormSet(
                self.request.POST, 
                instance=self.object  # ⚠️ IMPORTANTE: agregar instance aquí también
            )
        else:
            context['formset'] = VentaDetalleFormSet(
                instance=self.object  # ⚠️ IMPORTANTE: agregar instance
            )
        
        # Agregar variable para controlar el botón en el template
        context['modo_edicion'] = True
        context['titulo'] = f'Editar Venta #{self.object.codigo}'
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        # Validar tanto el form como el formset
        if form.is_valid() and formset.is_valid():
            # Guardar la venta primero
            self.object = form.save()
            
            # Luego guardar los items del formset
            formset.instance = self.object  # ⚠️ IMPORTANTE: asignar la instancia
            formset.save()
            self.object.calcular_total()
            
            messages.success(self.request, "Venta actualizada exitosamente.")
            return super().form_valid(form)
        else:
            # Si hay errores, mostrar el form con errores
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrige los errores en el formulario.")
        return super().form_invalid(form)

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
    
    
