# 🦕 Dinosource Dashboard

Dashboard interactivo de datos sobre dinosaurios construido con Dash y Tailwind CSS.

## 🚀 Instalación y Uso

### 1. Preparar el entorno

```bash
# Crear entorno virtual (si no existe)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Probar que todo funciona (opcional)
./test.sh
```

### 2. Correr la aplicación

#### Opción 1: Modo Desarrollo
```bash
python app.py
```

#### Opción 2: Con Gunicorn (Producción)
```bash
gunicorn app:server --bind 0.0.0.0:8050 --workers 2 --timeout 120
```

#### Opción 3: Usando el script
```bash
./run.sh
```

### 3. Detener la aplicación

Si la aplicación está bloqueando el puerto, usa uno de estos métodos:

#### Método 1: Script de detención
```bash
./stop.sh
```

#### Método 2: Comando directo
```bash
# Buscar y eliminar procesos en el puerto 8050
lsof -ti:8050 | xargs kill -9
```

#### Método 3: Si ejecutaste desde terminal
Presiona `Ctrl + C` en la terminal donde corre la app

### 4. Verificar que el puerto está libre

```bash
# Ver qué procesos están usando el puerto 8050
lsof -ti:8050

# Ver información detallada
lsof -i:8050
```

## 🔧 Solución de Problemas

### Error: "Puerto 8050 ya en uso"
Ejecuta el script de detención:
```bash
./stop.sh
```

### Error: "HTTP 429: Too Many Requests"
La aplicación ahora usa un sistema de caché automático. Si ves este error:
1. La primera vez se descargará el dataset y se guardará en `dinosaurs_dataset_cache.csv`
2. Las siguientes veces usará el archivo de caché local
3. El sistema tiene reintentos automáticos con esperas exponenciales
4. Si persiste, espera unos minutos antes de reintentar

Para forzar la descarga nuevamente:
```bash
rm dinosaurs_dataset_cache.csv
./run.sh
```

### Error: "Command 'gunicorn' not found"
Asegúrate de tener el entorno virtual activado:
```bash
source venv/bin/activate
pip install gunicorn
```

### Error: "Permission denied" en los scripts
Dale permisos de ejecución:
```bash
chmod +x run.sh stop.sh
```

## 📋 Comandos Útiles

```bash
# Ver procesos en ejecución
ps aux | grep gunicorn

# Probar la aplicación (carga el dataset y lo guarda en caché)
./test.sh

# Ver logs en tiempo real
tail -f logs/access.log

# Reiniciar la aplicación
./stop.sh && ./run.sh

# Limpiar caché del dataset
rm dinosaurs_dataset_cache.csv

# Ver información del archivo de caché
ls -lh dinosaurs_dataset_cache.csv
```

## 🎨 Características

- **Fuente moderna**: Inter de Google Fonts
- **Diseño responsive**: Funciona en móvil, tablet y desktop
- **Gráficos interactivos**: Plotly charts
- **Estilo moderno**: Tailwind CSS con gradientes y animaciones
- **Sistema de caché inteligente**: Evita errores de rate limiting descargando el dataset una sola vez
- **Manejo robusto de errores**: Reintentos automáticos con esperas exponenciales

## 📝 Notas

- El comando correcto para gunicorn es `app:server` (no `app:app`)
- La aplicación usa el puerto 8050 por defecto
- Todos los datos se cargan desde una fuente externa de Kaggle

## 🛠️ Tecnologías

- Dash (Framework web)
- Plotly (Gráficos interactivos)
- Pandas (Manejo de datos)
- Tailwind CSS (Estilos)
- Gunicorn (Servidor WSGI)

