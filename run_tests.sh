#!/bin/bash
# Script shell pour exécuter les tests avec verbosité complète sur Linux/Mac
source venv/bin/activate
python manage.py test tests -v 2

