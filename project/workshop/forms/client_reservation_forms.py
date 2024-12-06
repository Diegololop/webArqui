from django import forms
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Product, Reservation, Client, BusinessHours


class ClientReservationForm(forms.Form):
    """Formulario de reservas para clientes"""
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre'
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su apellido'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com'
        })
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 XXXX XXXX'
        })
    )
    rut = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XX.XXX.XXX-X'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': 'required'
        })
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'required': 'required'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción opcional'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            # Combinar fecha y hora
            service_date = datetime.combine(date, time)
            service_date = timezone.make_aware(service_date)

            # Validar que no sea en el pasado
            if service_date < timezone.now():
                raise forms.ValidationError('La fecha y hora no pueden estar en el pasado.')

            # Validar horario de atención
            try:
                business_hours = BusinessHours.objects.get(day=date.weekday())
                if business_hours.is_closed:
                    raise forms.ValidationError(f'No hay atención los {business_hours.get_day_display()}.')
                
                if time < business_hours.open_time or time > business_hours.close_time:
                    raise forms.ValidationError(
                        f'El horario de atención es de {business_hours.open_time.strftime("%H:%M")} '
                        f'a {business_hours.close_time.strftime("%H:%M")}.'
                    )
            except BusinessHours.DoesNotExist:
                raise forms.ValidationError('No hay horarios definidos para este día.')

            cleaned_data['service_date'] = service_date

        return cleaned_data
    
