# 📊 Estados de Interacción - Visor Streamlit

Aplicación web interactiva para visualizar y analizar los estados de los mensajes SMS y WhatsApp enviados en la campaña de comunicación.

## 🎯 Características

- **Diagrama Sankey Interactivo**: Visualiza el flujo de estados de los mensajes
- **Análisis SMS**: 315k+ registros de mensajes SMS (SMS outbound)
- **Análisis WhatsApp**: ~2k registros de WhatsApp (WhatsApp outbound)
- **Comparativa**: Gráficos comparativos entre SMS y WhatsApp
- **Estadísticas Detalladas**: Distribuciones, proporciones y tendencias
- **Procesamiento Eficiente**: Manejo óptimo de datasets grandes (132MB+)

## 📋 Estados de Interacción

### Flujo 1: WhatsApp (Outbound)
```
Leído ─┬─→ Se unió a la comunidad → Mensaje de bienvenida
       ├─→ Interacción positiva → Mensaje de invitación a interactuar
       ├─→ Sin interacción → Mensaje de invitación a interactuar
       ├─→ Interacción negativa → Lista negra
No leído → Mensaje de recordatorio
```

### Flujo 2: SMS (Outbound)
```
Leído ─┬─→ Se unió a la comunidad → Mensaje de bienvenida
       ├─→ Interacción positiva → Flujo 1: WhatsApp
       ├─→ Sin interacción → Flujo 1: WhatsApp
       ├─→ Interacción negativa → Lista negra
No leído → Flujo 1: WhatsApp
```

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- Virtualenv
- Dependencias: pandas, plotly, streamlit, numpy

### Instalación

1. Crear y activar el entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
streamlit run scripts/app.py
```

La aplicación se abrirá en `http://localhost:8503`

## 📁 Estructura del Proyecto

```
reportes/
├── scripts/
│   ├── app.py                 # Aplicación principal Streamlit
│   ├── config.py              # Configuración centralizada
│   ├── data_loader.py         # Carga eficiente de datos
│   ├── visualizations.py      # Gráficos y visualizaciones
│   ├── utils.py               # Funciones auxiliares
│   └── visor.py               # Módulo adicional
├── data/
│   ├── mensajes_texto/        # Archivo SMS (132MB+)
│   └── mensajes_whatsapp/     # Archivos WhatsApp (CSV)
├── requirements.txt           # Dependencias Python
├── run.sh                      # Script de inicio
└── README.md                  # Este archivo
```

## 🔧 Configuración

### config.py
Contiene toda la configuración centralizada:
- Rutas de archivos de datos
- Configuración CSV (encoding, delimitadores)
- Mapeos de estados
- Colores para visualizaciones
- Configuración de Streamlit

### data_loader.py
Funciones para cargar datos de manera eficiente:
- `load_sms_data()`: Carga SMS con soporte a muestreo
- `load_whatsapp_data()`: Carga y combina archivos WhatsApp
- `get_sms_statistics()`: Estadísticas rápidas sin cargar todo
- `get_whatsapp_statistics()`: Estadísticas de WhatsApp
- `get_interaction_flow_data()`: Prepara datos para Sankey

### visualizations.py
Funciones para crear gráficos:
- `create_sankey_diagram()`: Diagrama de Sankey
- `create_status_bar_chart()`: Gráfico de barras
- `create_pie_chart()`: Gráfico de pastel
- `create_time_series_chart()`: Series temporales
- `create_comparison_chart()`: Comparativa SMS vs WhatsApp

## 📊 Datasets

### SMS (mensajes_texto.csv)
- **Tamaño**: ~132 MB
- **Registros**: ~315,520
- **Campos**: Id, Teléfono, Mensaje, Fechas, Estado, Operador, etc.
- **Estados**: Entregado al operador, Fallido, Lista negra

### WhatsApp
**Archivo 1**: 2026-01-15 Saludo y agradecimiento firmantes
- Registros: 1,001
- Estados: Delivered, Failed, Read, Processing

**Archivo 2**: 2026-01-16 17_57_53
- Registros: 902
- Estados: Delivered, Failed, Read, Processing

## 📈 Visualizaciones

1. **Diagrama Sankey**: Flujo completo de estados
2. **Gráficos de Barras**: Distribución por estado
3. **Gráficos de Pastel**: Proporción de estados
4. **Series Temporales**: Actividad por fecha
5. **Comparativa**: SMS vs WhatsApp lado a lado

## 🎨 Colores de Estados

- 🟢 **Leído/Entregado**: Verde (#28a745, #2196F3)
- 🟣 **Interacción Positiva**: Violeta (#9C27B0)
- 🟡 **Sin Interacción**: Amarillo (#FFC107)
- 🔴 **Fallido/Negativo**: Rojo (#F44336)
- 🟠 **Rechazado**: Naranja (#FF9800)

## 💡 Uso

### Secciones de la Aplicación

1. **Visión General**: Resumen de totales por canal
2. **Diagrama Sankey**: Visualización interactiva del flujo
3. **SMS**: Análisis detallado de mensajes SMS
   - Estadísticas
   - Gráficos
   - Muestra de datos
4. **WhatsApp**: Análisis detallado de WhatsApp
   - Estadísticas
   - Gráficos
   - Detalles por envío
5. **Comparativa**: Gráficos comparativos

### Interactividad
- Hover sobre elementos para ver detalles
- Zoom en gráficos Plotly
- Expanders para ver información adicional
- Tabs para cambiar entre vistas

## ⚙️ Configuración Avanzada

### Muestreo de Datos SMS
Por defecto, la aplicación carga una muestra de 10,000 registros del archivo SMS para mejor rendimiento. Para cargar el dataset completo:

```python
# En data_loader.py
sms_df = load_sms_data(sample=False)  # Cargar todo
```

### Caché de Streamlit
Todos los datos se cachean automáticamente. Para limpiar el caché:
```bash
streamlit cache clear
```

## 🐛 Troubleshooting

### Error de Encoding SMS
Si hay problemas con caracteres especiales:
```python
# En config.py
CSV_ENCODING["sms"] = "UTF-8"  # o "ISO-8859-1"
```

### Advertencias de Formato de Fecha
Las advertencias de formato de fecha son normales. Especificar formato:
```python
pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S", errors="coerce")
```

### Aplicación Lenta
- Aumentar tamaño de muestra gradualmente
- Verificar disponibilidad de RAM
- Usar `sample=True` para diagnóstico rápido

## 📝 Desarrollo

### Agregar Nueva Visualización

1. Crear función en `visualizations.py`:
```python
def create_new_chart(data, title=""):
    fig = go.Figure(...)
    return fig
```

2. Usar en `app.py`:
```python
st.plotly_chart(create_new_chart(data), use_container_width=True)
```

### Agregar Nuevo Dataset
1. Actualizar `config.py` con rutas
2. Crear función carga en `data_loader.py`
3. Crear sección en `app.py`

## 📄 Licencia

Proyecto interno de Cuántico Tecnología - 2026

## 👥 Contacto

Equipo de Análisis de Datos
Cuántico Tecnología
No leído → Flujo 1: WhatsApp
```

## 🗂️ Estructura de Directorios

```
reportes/
├── data/
│   ├── mensajes_texto/
│   │   └── mensajes_texto.csv (132MB, 315k registros)
│   └── mensajes_whatsapp/
│       ├── 2026-01-15 Saludo y agradecimiento firmantes_20260119_GMT-05.csv
│       └── 2026-01-16 17_57_53_20260119_GMT-05 (1).csv
├── scripts/
│   ├── config.py (Configuración centralizada)
│   ├── data_loader.py (Carga y procesamiento de datos)
│   ├── visualizations.py (Gráficos y visualizaciones)
│   └── app.py (Aplicación principal Streamlit)
├── requirements.txt (Dependencias de Python)
├── run.sh (Script de inicio)
└── README.md (Este archivo)
```

## 🚀 Inicio Rápido

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación
```bash
# Opción 1: Usar script bash
chmod +x run.sh
./run.sh

# Opción 2: Ejecutar directamente
streamlit run scripts/app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📊 Módulos

### `config.py`
Configuración centralizada:
- Rutas de archivos
- Codificación de caracteres
- Mapeos de estados
- Colores para visualizaciones
- Configuración de Streamlit

### `data_loader.py`
Carga y procesamiento de datos:
- `load_sms_data()`: Carga datos de SMS con soporte para muestreo
- `load_whatsapp_data()`: Carga y combina archivos WhatsApp
- `get_sms_stats()`: Estadísticas eficientes sin cargar todo
- `get_whatsapp_stats()`: Estadísticas de WhatsApp
- `get_interaction_flow_data()`: Datos para Sankey

### `visualizations.py`
Funciones de visualización:
- `create_sankey_diagram()`: Diagrama Sankey interactivo
- `create_status_bar_chart()`: Gráfico de barras de estados
- `create_pie_chart()`: Gráfico de pastel
- `create_time_series_chart()`: Serie temporal
- `create_comparison_chart()`: Comparativa SMS vs WhatsApp

### `app.py`
Aplicación principal con:
- Secciones temáticas
- Pestañas de estadísticas, gráficos y datos
- Barra lateral de configuración
- Caché de Streamlit para optimización

## 📈 Datos

### SMS (mensajes_texto.csv)
- **Registros**: 315,520
- **Tamaño**: 132 MB
- **Codificación**: LATIN1
- **Delimitador**: `;`

**Columnas principales:**
- Id Envio, Telefono celular, Mensaje
- Fecha de Carga, Fecha y hora procesado
- Estado del envio (Entregado al operador, Lista negra, Operador fallido)
- Referencia, Usuario, Operador
- Tipo Mensaje, URLs y clicks

### WhatsApp
**Archivo 1**: 1,001 registros (2026-01-15)
**Archivo 2**: 902 registros (2026-01-16)

**Columnas principales:**
- Nick name, Phone number, Status
- Date Sent, Date Delivered, Date Read
- Reply Status, Error Code

**Estados**: Delivered, Failed, Read, Processing

## ⚙️ Configuración Avanzada

### Muestreo de Datos SMS
Para trabajar con muestras del archivo SMS (más rápido):
```python
from data_loader import load_sms_data
df = load_sms_data(sample=True, sample_size=10000)
```

### Personalizar Colores
En `config.py`, modificar el diccionario `COLORS`:
```python
COLORS = {
    "Enviado": "#4CAF50",
    "Entregado": "#2196F3",
    ...
}
```

## 🔍 Análisis Eficiente de Datos Grandes

La aplicación utiliza varias técnicas para trabajar con archivos grandes sin cargarlos completamente:

1. **Caché de Streamlit**: `@st.cache_data` para datos frecuentemente accedidos
2. **Estadísticas Shell**: Comandos de sistema para conteos rápidos
3. **Muestreo**: Opción de cargar solo muestras de datos grandes
4. **Lectura Selectiva**: Solo cargar columnas necesarias

## 📝 Notas Técnicas

- **Encoding**: SMS en LATIN1, WhatsApp en UTF-8
- **Fechas**: Convertidas automáticamente a datetime
- **Estados**: Mapeados a nombres más legibles
- **Colores**: Consistentes en toda la aplicación
- **Performance**: Optimizado para carga rápida con datos grandes

## 🛠️ Troubleshooting

### Error de codificación al cargar SMS
Asegurar que el archivo SMS tenga encoding LATIN1. El código lo maneja automáticamente.

### Lentitud en cargas iniciales
- Usar muestreo: `load_sms_data(sample=True)`
- La caché de Streamlit acelera las cargas posteriores

### Puerto 8501 en uso
```bash
streamlit run scripts/app.py --server.port 8502
```

## 👨‍💼 Autor
Cuántico Tecnología - Análisis de Campañas de Comunicación

## 📄 Licencia
Desarrollado para Mauricio Lizcano - Campaña Presidencial 2026
