from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import UserProfile
from ..forms.employee_forms import EmployeeCreationForm, EmployeeEditForm
from ..decorators import admin_required

@login_required
@admin_required
def employee_list(request):
    employees = UserProfile.objects.exclude(role='client')
    return render(request, 'workshop/admin/employee_list.html', {
        'employees': employees
    })

@login_required
@admin_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado exitosamente.')
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()
    
    return render(request, 'workshop/admin/employee_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
@admin_required
def employee_edit(request, employee_id):
    employee = get_object_or_404(UserProfile, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            # Update user data first
            user = employee.user
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            # Then update profile
            employee.phone = form.cleaned_data['phone']
            employee.role = form.cleaned_data['role']
            employee.save()
            
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('employee_list')
    else:
        form = EmployeeEditForm(instance=employee, initial={
            'username': employee.user.username,
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'email': employee.user.email
        })
    
    return render(request, 'workshop/admin/employee_form.html', {
        'form': form,
        'employee': employee,
        'action': 'Editar'
    })

@login_required
@admin_required
def employee_delete(request, employee_id):
    employee = get_object_or_404(UserProfile, id=employee_id)
    
    if request.method == 'POST':
        employee.user.delete()  # This will also delete the profile due to CASCADE
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('employee_list')
    
    return render(request, 'workshop/admin/employee_confirm_delete.html', {
        'employee': employee
    })