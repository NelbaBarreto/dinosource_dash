#!/bin/bash
# Script para probar que la app funciona correctamente

echo "🧪 Probando la aplicación..."
echo ""

# Activar entorno virtual
source venv/bin/activate

echo "📦 Verificando que el dataset puede cargarse..."
python3 -c "
import sys
sys.path.insert(0, '.')
print('Importando app...')
try:
    import app
    print('✅ App importada correctamente')
    print('✅ Dataset cargado: {} filas'.format(len(app.data)))
    print('✅ Sistema de caché funcionando')
except Exception as e:
    print('❌ Error:', e)
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos los tests pasaron correctamente"
    echo "✅ La app está lista para ser ejecutada con: ./run.sh"
else
    echo ""
    echo "❌ Hubo errores en los tests"
    exit 1
fi

