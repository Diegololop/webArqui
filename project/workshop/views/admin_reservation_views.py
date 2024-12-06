from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from ..models import Product, Reservation
from ..forms.admin_reservation_forms import AdminReservationForm
from ..decorators import reservation_management_required

@login_required
@reservation_management_required
def admin_reservation_list(request):
    """Vista de lista de reservas para administración"""
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
@reservation_management_required
def admin_reservation_form(request, reservation_id=None):
    """Vista para crear/editar reservas (admin/recepcionista)"""
    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        action = 'Editar'
    else:
        reservation = None
        action = 'Crear'

    if request.method == 'POST':
        form = AdminReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Reserva {action.lower()}da exitosamente.')
            return redirect('admin_reservation_list')
    else:
        form = AdminReservationForm(instance=reservation)

    services = Product.objects.filter(category='service')
    return render(request, 'workshop/admin/reservation_form.html', {
        'form': form,
        'reservation': reservation,
        'action': action,
        'services': services
    })

@login_required
@reservation_management_required
def admin_reservation_delete(request, reservation_id):
    """Vista para eliminar/cancelar reservas"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reserva cancelada exitosamente.')
        return redirect('admin_reservation_list')
    
    return render(request, 'workshop/admin/reservation_confirm_delete.html', {
        'reservation': reservation
    })