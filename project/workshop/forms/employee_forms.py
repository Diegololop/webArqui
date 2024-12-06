from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from ..models import UserProfile

class EmployeeCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el apellido'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        label='Teléfono',
        widget=forms.TextInput(attrs={'placeholder': '+56 9 XXXX XXXX'})
    )
    role = forms.ChoiceField(
        choices=[choice for choice in UserProfile.ROLE_CHOICES if choice[0] != 'client'],
        required=True,
        label='Cargo',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})
        self.fields['password1'].help_text = (
            'La contraseña debe contener al menos:\n'
            '- 8 caracteres\n'
            '- Una letra mayúscula\n'
            '- Una letra minúscula\n'
            '- Un número\n'
            '- Un carácter especial (@$!%*?&)'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data['phone']
            )
        return user

class EmployeeEditForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[choice for choice in UserProfile.ROLE_CHOICES if choice[0] != 'client'],
        required=True,
        label='Cargo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['role', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(id=self.instance.user.id).filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.user.id).filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        return profile