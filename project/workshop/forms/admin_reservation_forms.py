from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Product, Reservation, Client, BusinessHours

class AdminReservationForm(forms.ModelForm):
    """Formulario de reservas para administradores y recepcionistas"""
    class Meta:
        model = Reservation
        fields = ['client', 'services', 'service_date', 'description', 'status']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'services': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'required': 'required',
                'id': 'servicesInput'
            }),
            'service_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'required': 'required'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['services'].queryset = Product.objects.filter(category='service')
        
        # Si hay una instancia, convertir la fecha a formato datetime-local
        if self.instance.pk and self.instance.service_date:
            self.initial['service_date'] = self.instance.service_date.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        services = cleaned_data.get('services')
        service_date = cleaned_data.get('service_date')

        if services and service_date:
            # Calcular duración total y precio
            total_duration = sum(service.duration or 0 for service in services)
            total_price = sum(service.price for service in services)

            # Verificar que la reserva termine dentro del horario de atención
            end_time = service_date + timedelta(minutes=total_duration)
            business_hours = BusinessHours.objects.get(day=service_date.weekday())
            
            closing_datetime = datetime.combine(
                service_date.date(),
                business_hours.close_time,
                tzinfo=service_date.tzinfo
            )

            if end_time > closing_datetime:
                raise forms.ValidationError(
                    'La duración total de los servicios excede el horario de atención.'
                )

            cleaned_data['total_duration'] = total_duration
            cleaned_data['total_price'] = total_price

        return cleaned_data

    def save(self, commit=True):
        # Calculate total duration and price from services
        services = self.cleaned_data.get('services', [])
        total_duration = sum(service.duration or 0 for service in services)
        total_price = sum(service.price for service in services)

        # Create the instance
        instance = super().save(commit=False)
        
        # Set additional calculated fields
        instance.total_duration = total_duration
        instance.total_price = total_price

        if commit:
            instance.save()  # Save the instance first to get an ID
            
            # Use set() for many-to-many relationships after saving
            if services:
                instance.services.set(services)

        return instance