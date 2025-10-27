from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import ClienteForm
from .models import Cliente

class ClienteListView(ListView):
    model = Cliente
    paginated_by = 15

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cliente:lista_clientes")

class ClienteDetailView(DetailView):
    model = Cliente

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cliente:lista_clientes")

class ClienteDeleteView(DeleteView):
    model = Cliente
    success_url = reverse_lazy("cliente:lista_clientes")
