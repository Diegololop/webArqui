from django import template
from datetime import timedelta
from decimal import Decimal
import json

register = template.Library()

@register.filter
def duration(value):
    """Convert timedelta to human readable format"""
    if not isinstance(value, timedelta):
        return "N/A"
    
    days = value.days
    hours = value.seconds // 3600
    minutes = (value.seconds % 3600) // 60
    
    parts = []
    if days:
        parts.append(f"{days} día{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hora{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minuto{'s' if minutes != 1 else ''}")
    
    return ", ".join(parts) if parts else "0 minutos"

@register.filter(name='divide')
def divide(value, arg):
    """
    Divides the value by the argument.
    Handles cases where the argument might be zero.
    """
    try:
        return Decimal(value) / Decimal(arg) if arg else 0
    except (ValueError, TypeError):
        return 0

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    """
    try:
        return Decimal(value) * Decimal(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def map_attr(value, attr):
    """Map an iterable of objects to a list of attribute values"""
    try:
        return [getattr(item, attr) for item in value]
    except (AttributeError, TypeError):
        return []

@register.filter
def jsonify(obj):
    """Convert object to JSON string"""
    return json.dumps(obj)