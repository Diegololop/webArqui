from django.urls import path
from .views import (
    home_views, auth_views, employee_views,
    inventory_views, product_views, public_views,
    service_views, work_order_views,
    admin_reservation_views,
    client_reservation_views,
    client_views,
    report_views, 
    provider_views
)
from .views.admin_reservation_views import (
    admin_reservation_list,
    admin_reservation_form,
    admin_reservation_delete,
)

urlpatterns = [
    # Home
    path('', home_views.home, name='home'),
    path('dashboard/', home_views.dashboard, name='dashboard'),
    path('vehicle-tracking/', home_views.vehicle_tracking, name='vehicle_tracking'),

    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register, name='register'),
    path('activate-account/', auth_views.activate_account, name='activate_account'),

    # Client Management
    path('management/clients/', client_views.client_list, name='client_list'),
    path('management/clients/add/', client_views.client_add, name='client_add'),
    path('management/clients/<int:client_id>/edit/', client_views.client_edit, name='client_edit'),
    path('management/clients/<int:client_id>/delete/', client_views.client_delete, name='client_delete'),

    # Employee Management
    path('management/employees/', employee_views.employee_list, name='employee_list'),
    path('management/employees/add/', employee_views.employee_add, name='employee_add'),
    path('management/employees/<int:employee_id>/edit/', employee_views.employee_edit, name='employee_edit'),
    path('management/employees/<int:employee_id>/delete/', employee_views.employee_delete, name='employee_delete'),

    # Product Management
    path('management/products/', product_views.product_list, name='product_list'),
    path('management/products/add/', product_views.product_add, name='product_add'),
    path('management/products/<int:product_id>/edit/', product_views.product_edit, name='product_edit'),
    path('management/products/<int:product_id>/delete/', product_views.product_delete, name='product_delete'),

    # Service Management
    path('management/services/', service_views.service_list, name='service_list'),
    path('management/services/add/', service_views.service_add, name='service_add'),
    path('management/services/<int:service_id>/edit/', service_views.service_edit, name='service_edit'),
    path('management/services/<int:service_id>/delete/', service_views.service_delete, name='service_delete'),

    # Admin/Receptionist Reservation URLs
    path('management/reservations/', admin_reservation_views.admin_reservation_list, name='admin_reservation_list'),
    path('management/reservations/add/', admin_reservation_views.admin_reservation_form, name='admin_reservation_add'),
    path('management/reservations/<int:reservation_id>/edit/', admin_reservation_views.admin_reservation_form, name='admin_reservation_edit'),
    path('management/reservations/<int:reservation_id>/delete/', admin_reservation_views.admin_reservation_delete, name='admin_reservation_delete'),

    # Client Reservation URLs
    path('reservations/create/', client_reservation_views.client_reservation_form, name='create_reservation'),

    # Work Order Management
    path('management/work-orders/', work_order_views.work_order_list, name='work_order_list'),
    path('management/work-orders/add/', work_order_views.work_order_add, name='work_order_add'),
    path('management/work-orders/<int:order_id>/edit/', work_order_views.work_order_edit, name='work_order_edit'),
    path('management/work-orders/<int:order_id>/delete/', work_order_views.work_order_delete, name='work_order_delete'),
    path('management/work-orders/check-availability/', work_order_views.check_work_order_availability, name='check_work_order_availability'),

    # Public Views
    path('services/', public_views.service_list_public, name='service_list_public'),
    path('products/', public_views.product_list_public, name='product_list_public'),

    path('reservations/', admin_reservation_list, name='admin_reservation_list'),
    path('reservations/form/<int:reservation_id>/', admin_reservation_form, name='admin_reservation_form'),
    path('reservations/delete/<int:reservation_id>/', admin_reservation_delete, name='admin_reservation_delete'),

    # Reports
    path('management/reports/', report_views.dashboard_reports, name='dashboard_reports'),
    path('management/reports/services/', report_views.service_performance_report, name='service_performance_report'),
    path('management/reports/financial/', report_views.financial_report, name='financial_report'),
    path('management/reports/customers/', report_views.customer_report, name='customer_report'),

    # Provider Management
    path('providers/', provider_views.provider_list, name='provider_list'),
    path('providers/add/', provider_views.provider_add, name='provider_add'),
    path('providers/<int:provider_id>/edit/', provider_views.provider_edit, name='provider_edit'),
    path('providers/<int:provider_id>/delete/', provider_views.provider_delete, name='provider_delete'),
]