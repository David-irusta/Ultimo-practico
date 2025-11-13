from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ClienteForm
from .models import Cliente

class ClienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10
    ordering = ['id']
    permission_required = "cliente.view_cliente"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return super().has_permission() and user.groups.filter(name='Ventas').exists()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.get_queryset().exists():
            messages.info(request, "No hay clientes disponibles.")

        return response

class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy('clientes:cliente_list')
    permission_required = "cliente.add_cliente"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cliente creado correctamente.")
        return response


class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Cliente
    template_name = "clientes/cliente_detail.html"
    context_object_name = "cliente"
    permission_required = "clientes.view_cliente"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:cliente_list")
    permission_required = "ventas.add_venta"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cliente actualizado correctamente.")
        return response

class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("cliente:lista_clientes")
    permission_required = "clientes.delete_cliente"

    def has_permission(self):
        user = self.request.user
        if user.is_superuser or user.is_staff or user.groups.filter(name='Administradores').exists():
            return True
        return (super().has_permission() and self.request.user.groups.filter(name='Ventas').exists())

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
