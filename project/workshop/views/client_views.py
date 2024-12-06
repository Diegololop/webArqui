from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Client
from ..forms.client_forms import ClientForm
from ..decorators import client_management_required

@login_required
@client_management_required
def client_list(request):
    """Vista de lista de clientes"""
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'workshop/admin/client_list.html', {
        'clients': clients
    })

@login_required
@client_management_required
def client_add(request):
    """Agregar nuevo cliente"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('client_list')
    else:
        form = ClientForm()
    
    return render(request, 'workshop/admin/client_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
@client_management_required
def client_edit(request, client_id):
    """Editar cliente existente"""
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'workshop/admin/client_form.html', {
        'form': form,
        'client': client,
        'action': 'Editar'
    })

@login_required
@client_management_required
def client_delete(request, client_id):
    """Eliminar cliente"""
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.user.delete()  # This will also delete the client due to CASCADE
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('client_list')
    
    return render(request, 'workshop/admin/client_confirm_delete.html', {
        'client': client
    })