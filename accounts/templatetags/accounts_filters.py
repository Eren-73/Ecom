"""
Filtres de template personnalisés pour l'application accounts
"""
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplie deux nombres avec gestion d'erreur"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
