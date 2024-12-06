from django import forms
from ..models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del producto'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Precio'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Cantidad en stock'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = 'product'
        self.fields['category'].disabled = True