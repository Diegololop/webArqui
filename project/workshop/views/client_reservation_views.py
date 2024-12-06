from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Product, Reservation, Client
from ..forms.client_reservation_forms import ClientReservationForm

def client_reservation_form(request):
    """Vista de reservas para clientes"""
    if request.method == 'POST':
        form = ClientReservationForm(request.POST)
        services = request.POST.getlist('services')
        
        if not services:
            messages.error(request, 'Debe seleccionar al menos un servicio.')
            return redirect('client_reservation_form')

        if form.is_valid():
            # Obtener servicios seleccionados
            selected_services = Product.objects.filter(id__in=services)
            
            # Calcular totales
            total_duration = sum(service.duration or 0 for service in selected_services)
            total_price = sum(service.price for service in selected_services)

            # Obtener o crear cliente
            if request.user.is_authenticated and hasattr(request.user, 'client'):
                client = request.user.client
            else:
                # Validar campos adicionales para cliente no registrado
                required_fields = ['first_name', 'last_name', 'email', 'phone', 'rut']
                if not all(form.cleaned_data.get(field) for field in required_fields):
                    messages.error(request, 'Todos los campos son requeridos para clientes no registrados.')
                    return redirect('client_reservation_form')

                # Crear usuario
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=User.objects.make_random_password()
                )

                # Crear cliente
                client = Client.objects.create(
                    user=user,
                    rut=form.cleaned_data['rut'],
                    phone=form.cleaned_data['phone'],
                    address="Pendiente"
                )

            # Crear reserva
            reservation = Reservation.objects.create(
                client=client,
                service_date=form.cleaned_data['service_date'],
                description=form.cleaned_data.get('description', ''),
                total_duration=total_duration,
                total_price=total_price,
                status='pending'
            )
            reservation.services.set(selected_services)

            messages.success(request, 'Reserva creada exitosamente.')
            if not request.user.is_authenticated:
                messages.info(request, 'Para ver su reserva, active su cuenta con el email y RUT proporcionados.')
                return redirect('activate_account')
            return redirect('dashboard')
    else:
        form = ClientReservationForm()

    return render(request, 'workshop/client_reservation_form.html', {
        'form': form,
        'services': Product.objects.filter(category='service')
    })