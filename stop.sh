#!/bin/bash
# Script para detener la app que está corriendo en el puerto 8050

PORT=8050

echo "🛑 Deteniendo la aplicación en el puerto $PORT..."

# Buscar y matar procesos en el puerto 8050
PIDS=$(lsof -ti:$PORT 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "✅ No hay procesos ejecutándose en el puerto $PORT"
else
    echo "🔍 Procesos encontrados: $PIDS"
    kill -9 $PIDS 2>/dev/null
    echo "✅ Procesos eliminados"
    sleep 1
    
    # Verificar que se cerró correctamente
    if lsof -ti:$PORT > /dev/null 2>&1; then
        echo "⚠️  Algunos procesos pueden aún estar activos"
    else
        echo "✅ Puerto $PORT liberado exitosamente"
    fi
fi

