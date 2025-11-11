from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import ClienteForm
from .models import Cliente

class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.get_queryset().exists():
            messages.info(request, "No hay clientes disponibles.")

        return response

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy('clientes:cliente_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cliente creado correctamente.")
        return response


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "clientes/cliente_detail.html"
    context_object_name = "cliente"

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:cliente_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cliente actualizado correctamente.")
        return response

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("cliente:lista_clientes")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
