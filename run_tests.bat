@echo off
REM Script batch pour exécuter les tests avec verbosité complète sur Windows
call venv\Scripts\activate.bat
python manage.py test tests -v 2
pause

