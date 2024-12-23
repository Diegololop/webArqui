# Generated by Django 5.0.1 on 2024-12-05 02:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('rut', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Formato de RUT inválido. Debe ser XX.XXX.XXX-X', regex='^\\d{1,2}\\.\\d{3}\\.\\d{3}[-][0-9kK]{1}$')], verbose_name='RUT')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('address', models.CharField(max_length=200, verbose_name='Dirección')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['name'],
            },
        ),
    ]
