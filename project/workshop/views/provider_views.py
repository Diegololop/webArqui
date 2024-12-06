from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Provider
from ..forms.provider_forms import ProviderForm
from ..decorators import admin_required

@login_required
def provider_list(request):
    """Lista de proveedores"""
    providers = Provider.objects.all()
    return render(request, 'workshop/providers/provider_list.html', {
        'providers': providers
    })

@login_required
@admin_required
def provider_add(request):
    """Agregar nuevo proveedor"""
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('provider_list')
    else:
        form = ProviderForm()
    
    return render(request, 'workshop/providers/provider_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
@admin_required
def provider_edit(request, provider_id):
    """Editar proveedor existente"""
    provider = get_object_or_404(Provider, id=provider_id)
    
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('provider_list')
    else:
        form = ProviderForm(instance=provider)
    
    return render(request, 'workshop/providers/provider_form.html', {
        'form': form,
        'provider': provider,
        'action': 'Editar'
    })

@login_required
@admin_required
def provider_delete(request, provider_id):
    """Eliminar proveedor"""
    provider = get_object_or_404(Provider, id=provider_id)
    
    if request.method == 'POST':
        provider.delete()
        messages.success(request, 'Proveedor eliminado exitosamente.')
        return redirect('provider_list')
    
    return render(request, 'workshop/providers/provider_confirm_delete.html', {
        'provider': provider
    })