from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, F, Max, Q, Case, When, FloatField
from django.db.models.functions import  TruncDay, TruncDate
from django.utils import timezone
from datetime import timedelta
from ..models import WorkOrder, Reservation, Product, Client
from ..decorators import admin_required


@login_required
@admin_required
def dashboard_reports(request):
    """Vista principal de informes y estadísticas"""
    # Obtener período de tiempo (último mes por defecto)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    # Estadísticas generales
    total_clients = Client.objects.count()
    active_work_orders = WorkOrder.objects.filter(status__in=['pending', 'in_progress']).count()
    completed_work_orders = WorkOrder.objects.filter(status='completed').count()
    pending_reservations = Reservation.objects.filter(status='pending').count()

    # Servicios más populares
    popular_services = Product.objects.filter(
        category='service',
        bookings__created_at__range=[start_date, end_date]
    ).annotate(
        total_reservations=Count('bookings')
    ).order_by('-total_reservations')[:5]

    # Ingresos diarios
    daily_income = WorkOrder.objects.filter(
        status='completed',
        created_at__range=[start_date, end_date]
    ).annotate(
        day=TruncDate('created_at')
    ).values('day').annotate(
        total=Sum('total_cost')
    ).order_by('day')

    # Tasa de conversión de reservas
    total_reservations = Reservation.objects.filter(
        created_at__range=[start_date, end_date]
    ).count()
    
    converted_reservations = WorkOrder.objects.filter(
        created_at__range=[start_date, end_date]
    ).count()

    conversion_rate = (converted_reservations / total_reservations * 100) if total_reservations > 0 else 0

    # Tiempo promedio de servicio
    avg_service_time = WorkOrder.objects.filter(
        status='completed',
        created_at__range=[start_date, end_date]
    ).aggregate(
        avg_time=Avg(F('updated_at') - F('created_at'))
    )['avg_time']

    daily_income = [
    {
        'day': item['day'].strftime('%Y-%m-%d'),  # Convierte la fecha a cadena 'YYYY-MM-DD'
        'total': float(item['total'])  # Convierte el valor de Decimal a flotante
    }
    for item in daily_income
]

    context = {
        'total_clients': total_clients,
        'active_work_orders': active_work_orders,
        'completed_work_orders': completed_work_orders,
        'pending_reservations': pending_reservations,
        'popular_services': popular_services,
        'daily_income': list(daily_income),  # Asegúrate de pasar daily_income al contexto
        'conversion_rate': round(conversion_rate, 2),
        'avg_service_time': avg_service_time,
    }

    return render(request, 'workshop/admin/reports/dashboard_reports.html', context)



@login_required
@admin_required
def service_performance_report(request):
    """Informe detallado del rendimiento de servicios"""
    # Obtener servicios con métricas
    services = Product.objects.filter(category='service').annotate(
        total_reservations=Count('bookings'),
        total_revenue=Sum('bookings__total_price', default=0),
        completed_bookings=Count(
            'bookings',
            filter=Q(bookings__status='confirmed')
        ),
        completion_rate=Case(
            When(total_reservations__gt=0, 
                 then=F('completed_bookings') * 100.0 / F('total_reservations')),
            default=0,
            output_field=FloatField()
        )
    ).order_by('-total_reservations')

    # Calcular el máximo de reservas para el gráfico de rendimiento
    max_reservations = services.aggregate(max_res=Max('total_reservations'))['max_res'] or 1
    
    # Protect against potential None values
    labels = [service.name or 'Unnamed Service' for service in services]
    reservations_data = [service.total_reservations or 0 for service in services]
    revenue_data = [
        (service.total_revenue or 0) / 10000 
        for service in services
    ]

    context = {
        'services': services,
        'labels': labels,
        'reservations_data': reservations_data,
        'revenue_data': revenue_data,
        'max_reservations': max_reservations
    }

    return render(request, 'workshop/admin/reports/service_performance.html', context)

from django.core.serializers.json import DjangoJSONEncoder

import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
@admin_required
def financial_report(request):
    """Informe financiero detallado diario"""
    # Ingresos diarios
    daily_income = WorkOrder.objects.filter(
        status='completed'
    ).annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(
        total=Sum('total_cost')
    ).order_by('day')

    # Redondear los ingresos diarios a enteros y formatear la fecha
    for item in daily_income:
        item['total'] = round(item['total'])  # Redondear a enteros
        item['day'] = item['day'].strftime('%Y-%m-%d')  # Convertir a string de fecha

    # Ingresos por tipo de servicio
    service_income = Product.objects.filter(
        category='service'
    ).annotate(
        total_revenue=Sum('bookings__total_price', default=0),
        total_orders=Count('bookings')
    ).order_by('-total_revenue')

    # Calcular ingresos totales para porcentajes
    total_revenue = service_income.aggregate(total=Sum('total_revenue'))['total'] or 0

    # Redondear el porcentaje para cada servicio
    for service in service_income:
        if total_revenue > 0:
            service_percentage = (service.total_revenue / total_revenue) * 100
            service.percentage = round(service_percentage)  # Redondear el porcentaje a un entero
        else:
            service.percentage = 0  # Si no hay ingresos totales, establecer el porcentaje en 0

    # Convertir daily_income a un formato JSON válido
    daily_income_json = json.dumps(list(daily_income), cls=DjangoJSONEncoder)

    context = {
        'daily_income': daily_income_json,
        'service_income': service_income,
        'total_revenue': total_revenue
    }

    return render(request, 'workshop/admin/reports/financial_report.html', context)





@login_required
@admin_required
def customer_report(request):
    """Informe de clientes y retención"""
    # Clientes más frecuentes
    top_clients = Client.objects.annotate(
        total_orders=Count('workorder'),
        total_spent=Sum('workorder__total_cost', default=0)
    ).order_by('-total_orders')[:10]

    # Tasa de retención (clientes que han vuelto al menos una vez)
    total_clients = Client.objects.count()
    returning_clients = Client.objects.annotate(
        visit_count=Count('workorder')
    ).filter(visit_count__gt=1).count()

    # Distribución de clientes por frecuencia
    vip_clients = Client.objects.annotate(
        visit_count=Count('workorder')
    ).filter(visit_count__gte=10).count()
    
    frequent_clients = Client.objects.annotate(
        visit_count=Count('workorder')
    ).filter(visit_count__range=(5, 9)).count()
    
    regular_clients = Client.objects.annotate(
        visit_count=Count('workorder')
    ).filter(visit_count__range=(1, 4)).count()

    retention_rate = (returning_clients / total_clients * 100) if total_clients > 0 else 0

    context = {
        'top_clients': top_clients,
        'retention_rate': round(retention_rate, 2),
        'vip_clients': vip_clients,
        'frequent_clients': frequent_clients,
        'regular_clients': regular_clients
    }

    return render(request, 'workshop/admin/reports/customer_report.html', context)

def report_view(request):
    # Supón que estás obteniendo los servicios de una base de datos o de alguna fuente
    services = Product.objects.all()  # Cambia esto según tu modelo de datos

    return render(request, 'your_template.html', {
        'services': services,
    })
