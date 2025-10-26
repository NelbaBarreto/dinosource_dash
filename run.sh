#!/bin/bash
# Script para correr la app con gunicorn

# Activamos el entorno virtual
source venv/bin/activate

# Corremos gunicorn con la configuración adecuada
# app:server porque en app.py tenemos: server = app.server
gunicorn app:server --bind 0.0.0.0:8050 --workers 2 --timeout 120

