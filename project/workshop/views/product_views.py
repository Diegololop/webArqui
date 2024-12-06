from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product
from ..forms.product_forms import ProductForm
from ..decorators import admin_required

@login_required
@admin_required
def product_list(request):
    """Vista de lista de productos"""
    products = Product.objects.filter(category='product')
    return render(request, 'workshop/admin/product_list.html', {
        'products': products
    })

@login_required
@admin_required
def product_add(request):
    """Agregar nuevo producto"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = 'product'
            product.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('product_list')
    else:
        form = ProductForm(initial={'category': 'product'})
    
    return render(request, 'workshop/admin/product_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
@admin_required
def product_edit(request, product_id):
    """Editar producto existente"""
    product = get_object_or_404(Product, id=product_id, category='product')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'workshop/admin/product_form.html', {
        'form': form,
        'product': product,
        'action': 'Editar'
    })

@login_required
@admin_required
def product_delete(request, product_id):
    """Eliminar producto"""
    product = get_object_or_404(Product, id=product_id, category='product')
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('product_list')
    
    return render(request, 'workshop/admin/product_confirm_delete.html', {
        'product': product
    })