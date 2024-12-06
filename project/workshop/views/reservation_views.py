from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import Product, Reservation, Client, BusinessHours
from ..forms.reservation_forms import ReservationModelForm
from ..decorators import receptionist_required

def client_reservation_form(request):
    # Asumiendo que ya tienes la instancia de reserva que se está creando
    reservation = Reservation(client=request.user.client, service_date=request.POST['service_date'], description=request.POST.get('description', ''))
    
    # Guarda la reserva para asignarle un id
    reservation.save()

    # Ahora, agrega los servicios al campo ManyToMany
    reservation.services.set(request.POST.getlist('services'))  # 'services' es el nombre del campo en tu formulario

    # Guarda de nuevo para persistir la relación ManyToMany
    reservation.save()

    return redirect('some_view')

@login_required
@receptionist_required
def reservation_list(request):
    """Vista de lista de reservas"""
    search_date = request.GET.get('date')
    reservations = Reservation.objects.all().order_by('-service_date')
    
    if search_date:
        try:
            date = datetime.strptime(search_date, '%Y-%m-%d').date()
            reservations = reservations.filter(service_date__date=date)
        except ValueError:
            messages.error(request, 'Formato de fecha inválido')
    
    return render(request, 'workshop/admin/reservation_list.html', {
        'reservations': reservations,
        'search_date': search_date
    })

@login_required
@receptionist_required
def reservation_form(request, reservation_id=None):
    """Vista para crear/editar reservas (admin/recepcionista)"""
    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        action = 'Editar'
    else:
        reservation = None
        action = 'Crear'

    if request.method == 'POST':
        form = ReservationModelForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Reserva {action.lower()}da exitosamente.')
            return redirect('reservation_list')
    else:
        form = ReservationModelForm(instance=reservation)

    return render(request, 'workshop/admin/reservation_form.html', {
        'form': form,
        'reservation': reservation,
        'action': action,
        'services': Product.objects.filter(category='service')
    })

@login_required
@receptionist_required
def reservation_delete(request, reservation_id):
    """Vista para eliminar/cancelar reservas"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reserva cancelada exitosamente.')
        return redirect('reservation_list')
    
    return render(request, 'workshop/admin/reservation_confirm_delete.html', {
        'reservation': reservation
    })

def get_time_slots(request):
    """API para obtener horarios disponibles"""
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Fecha requerida'}, status=400)
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        business_hours = BusinessHours.objects.get(day=date.weekday())
        
        if business_hours.is_closed:
            return JsonResponse({'slots': [], 'message': 'Cerrado este día'})
        
        # Generar slots cada 30 minutos
        slots = []
        current_time = datetime.combine(date, business_hours.open_time)
        end_time = datetime.combine(date, business_hours.close_time)
        
        while current_time < end_time:
            slot_time = current_time.strftime('%H:%M')
            # Verificar disponibilidad
            is_available = not Reservation.objects.filter(
                service_date__date=date,
                service_date__hour=current_time.hour,
                service_date__minute=current_time.minute
            ).exists()
            
            slots.append({
                'time': slot_time,
                'available': is_available,
                'reason': 'Horario ocupado' if not is_available else None
            })
            current_time += timedelta(minutes=30)
        
        return JsonResponse({'slots': slots})
    except (ValueError, BusinessHours.DoesNotExist):
        return JsonResponse({'error': 'Error al obtener horarios'}, status=400)