from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Product, WorkOrder, Client, Reservation, UserProfile
from django.db.models import Count, Q

def home(request):
    """Vista principal del sitio"""
    services = Product.objects.filter(category='service')
    context = {
        'services': services,
    }
    return render(request, 'workshop/home.html', context)

@login_required
def dashboard(request):
    """Dashboard personalizado según el rol del usuario"""
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    context = {
        'user_profile': user_profile,
    }
    
    if request.user.is_superuser or (user_profile and user_profile.role == 'admin'):
        context.update({
            'clients': Client.objects.all()[:5],
            'services': Product.objects.filter(category='service'),
            'work_orders': WorkOrder.objects.all()[:5],
            'reservations': Reservation.objects.filter(status='pending'),
        })
    elif user_profile and user_profile.role == 'mechanic':
        # Get work orders for mechanic with counts by status
        work_orders = WorkOrder.objects.filter(mechanic=user_profile)
        status_counts = {
            'pending': work_orders.filter(status='pending').count(),
            'in_progress': work_orders.filter(status='in_progress').count(),
            'completed': work_orders.filter(status='completed').count(),
            'cancelled': work_orders.filter(status='cancelled').count()
        }
        context.update({
            'work_orders': work_orders,
            'status_counts': status_counts
        })
    elif user_profile and user_profile.role == 'receptionist':
        context.update({
            'clients': Client.objects.all()[:5],
            'work_orders': WorkOrder.objects.all()[:5],
            'reservations': Reservation.objects.filter(status='pending'),
        })
    else:
        try:
            client = Client.objects.get(user=request.user)
            context.update({
                'work_orders': WorkOrder.objects.filter(client=client),
                'reservations': Reservation.objects.filter(client=client),
            })
        except Client.DoesNotExist:
            pass
    
    return render(request, 'workshop/dashboard.html', context)

def vehicle_tracking(request):
    """Vista pública para seguimiento de vehículos"""
    work_orders = []
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user)
            work_orders = WorkOrder.objects.filter(client=client)
        except Client.DoesNotExist:
            pass
    
    context = {
        'work_orders': work_orders,
    }
    return render(request, 'workshop/vehicle_tracking.html', context)