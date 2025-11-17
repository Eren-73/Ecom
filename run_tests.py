"""
Script pour exécuter tous les tests avec une verbosité complète
Affiche tous les tests exécutés avec leurs descriptions
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_platform.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Exécuter les tests avec verbosité 2 pour voir tous les détails
    execute_from_command_line(['manage.py', 'test', 'tests', '-v', '2'])

