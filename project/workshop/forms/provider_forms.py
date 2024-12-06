from django import forms
from django.core.validators import RegexValidator
from ..models import Provider

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'rut', 'email', 'phone', 'address', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XX.XXX.XXX-X'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 XXXX XXXX'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del proveedor'
            })
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Provider.objects.filter(rut=rut).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError('Este RUT ya está registrado.')
        return rut

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Provider.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email