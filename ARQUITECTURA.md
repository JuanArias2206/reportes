# 🏗️ Arquitectura de la Aplicación

## Visión General

La aplicación está diseñada con una arquitectura modular y escalable, separando responsabilidades en diferentes módulos:

```
┌─────────────────────────────────────┐
│      app.py (Streamlit UI)          │
└────────────────┬────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────────┐  ┌───────────┐
│ config │  │data_loader │  │   utils   │
└────────┘  └────────────┘  └───────────┘
    │            │                │
    └────────────┼────────────────┘
                 │
                 ▼
         ┌────────────────┐
         │visualizations  │
         └────────────────┘
                 │
                 ▼
         ┌────────────────┐
         │  Plotly Figs   │
         └────────────────┘
```

## Módulos

### 1. **config.py** - Configuración Centralizada
**Responsabilidad**: Almacenar todas las configuraciones y constantes

**Contenido**:
- Rutas de archivos
- Configuración de lectura CSV (encoding, delimitadores)
- Mapeos de estados
- Paleta de colores
- Mensajes y configuración de Streamlit

**Ventajas**:
- Cambios de configuración en un solo lugar
- Fácil mantenimiento
- Reutilizable en otros módulos

**Ejemplo**:
```python
from config import SMS_FILE, COLORS, PAGE_CONFIG

# Usar rutas
df = pd.read_csv(SMS_FILE)

# Usar colores
color = COLORS.get("Entregado", "#808080")
```

### 2. **data_loader.py** - Carga y Procesamiento de Datos
**Responsabilidad**: Manejar todas las operaciones de carga y procesamiento de datos

**Funciones principales**:

#### `load_sms_data(sample=True, sample_size=10000)`
- Carga datos SMS de manera eficiente
- Soporta muestreo para archivos grandes
- Convierte tipos de datos
- Cachea resultados automáticamente

```python
# Cargar muestra (rápido)
df_sample = load_sms_data(sample=True, sample_size=5000)

# Cargar todo (lento pero completo)
df_complete = load_sms_data(sample=False)
```

#### `load_whatsapp_data()`
- Carga y combina múltiples archivos WhatsApp
- Estandariza nombres de columnas
- Procesa fechas correctamente

#### `get_sms_statistics(sample=True)`
- Estadísticas rápidas sin cargar todo el dataset
- Cuenta por estado
- Información de operadores

#### `get_interaction_flow_data()`
- Prepara datos para el diagrama Sankey
- Retorna (source, target, value) tuplas
- Mapea estados según el esquema de flujo

**Caché de Streamlit**:
```python
@st.cache_data(show_spinner=True)
def load_sms_data(...):
    # Datos se cachean automáticamente
```

### 3. **visualizations.py** - Gráficos e Visualizaciones
**Responsabilidad**: Crear todas las visualizaciones con Plotly

**Funciones**:

#### `create_sankey_diagram(source, target, value, title)`
- Diagrama Sankey interactivo
- Colores automáticos según estados
- Tamaño de flujo proporcional a valores

#### `create_status_bar_chart(data, title)`
- Gráfico de barras con estados
- Colores consistentes
- Etiquetas claras

#### `create_pie_chart(data, title)`
- Distribución porcentual
- Interactivo con porcentajes
- Colores por estado

#### `create_comparison_chart(sms_stats, whatsapp_stats)`
- Comparativa lado a lado
- SMS vs WhatsApp
- Gráfico de barras agrupadas

### 4. **utils.py** - Utilidades Auxiliares
**Responsabilidad**: Funciones reutilizables

**Funciones**:
- `normalize_phone()`: Normalización de teléfonos
- `categorize_response_time()`: Categorización de tiempos
- `calculate_engagement_rate()`: Cálculo de engagement
- `get_busiest_hours()`: Horas más activas
- `format_large_number()`: Formato de números

### 5. **app.py** - Aplicación Principal
**Responsabilidad**: Orquestar la interfaz Streamlit

**Estructura**:
```python
def setup_page()
    ↓ Configurar CSS y layout
    
def render_header()
    ↓ Título y subtítulo
    
def render_overview_section()
    ↓ Resumen rápido
    
def render_sankey_section()
    ↓ Diagrama Sankey
    
def render_sms_section()
    ↓ Análisis SMS (3 tabs)
    
def render_whatsapp_section()
    ↓ Análisis WhatsApp (3 tabs)
    
def render_comparison_section()
    ↓ Comparativa SMS vs WhatsApp
    
def render_sidebar()
    ↓ Controles y info
    
def main()
    ↓ Ejecutar todo
```

## Flujo de Datos

### 1. Carga Inicial
```
Usuario abre app
    ↓
Streamlit ejecuta app.py
    ↓
Se cargan configuraciones (config.py)
    ↓
Se cargan datos (data_loader.py)
    ↓
Se cachean en memoria
```

### 2. Render
```
Se llama a cada función render_*()
    ↓
Se obtienen datos del caché (rápido)
    ↓
Se crean visualizaciones
    ↓
Se muestran en UI
```

### 3. Interacción
```
Usuario interactúa con gráfico Plotly
    ↓
Plotly actualiza vista (client-side)
    ↓
No se vuelven a cargar datos
```

## Manejo Eficiente de Datos Grandes

### SMS (132 MB)
```
Opción 1: Muestreo (recomendado)
├─ Cargar 10,000 registros
├─ Análisis rápido
└─ Suficiente para patrones

Opción 2: Estadísticas sin cargar
├─ Usar comandos del SO
├─ Contar líneas
└─ Muy rápido
```

### WhatsApp (~2 KB)
```
Cargar completamente
└─ Siempre cabe en memoria
```

## Caché y Rendimiento

### Estrategia de Caché
```python
@st.cache_data  # Cachea en primer render
def load_sms_data(...):
    # Estos datos se guardan en memoria
    # Solo se recalculan si cambian los parámetros
    pass
```

### Tiempos Típicos
- SMS (muestra 10k): 2-5 segundos (primera ejecución)
- SMS (caché): <100ms
- WhatsApp: <200ms (primera ejecución)
- WhatsApp (caché): <50ms
- Sankey: 1-2 segundos

## Extensibilidad

### Agregar Nuevo Gráfico
1. Crear función en `visualizations.py`
2. Importar en `app.py`
3. Usar en la sección correspondiente

### Agregar Nuevo Dataset
1. Definir configuración en `config.py`
2. Crear función carga en `data_loader.py`
3. Crear sección en `app.py`

### Agregar Nuevo Estado
1. Agregar color en `config.py`
2. Puede usarse automáticamente en gráficos

## Separación de Responsabilidades

```
config.py
├─ ¿Dónde están los datos?
├─ ¿Qué colores usar?
└─ ¿Cómo leer CSV?

data_loader.py
├─ Cargar datos
├─ Procesar datos
└─ Calcular estadísticas

visualizations.py
├─ Crear gráficos
└─ Formatear visualizaciones

utils.py
├─ Funciones reutilizables
└─ Helpers

app.py
├─ Llamar a todo lo anterior
├─ Renderizar UI
└─ Manejar interacciones
```

## Mejoras Futuras

### Corto Plazo
- [ ] Exportar datos a CSV
- [ ] Filtros por fecha
- [ ] Búsqueda de teléfonos

### Mediano Plazo
- [ ] Base de datos en lugar de CSV
- [ ] Autenticación de usuarios
- [ ] Reportes automáticos

### Largo Plazo
- [ ] API REST
- [ ] Dashboard en tiempo real
- [ ] Predicciones con ML
- [ ] Integración con CRM

## Testing

### Estructura de Tests (futuro)
```
tests/
├── test_config.py
├── test_data_loader.py
├── test_visualizations.py
├── test_utils.py
└── test_app.py
```

## Documentación del Código

Cada función sigue el estándar:
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Descripción breve.
    
    Args:
        param1: Descripción
        param2: Descripción
    
    Returns:
        Descripción del retorno
    """
    pass
```

## Dependencias

```
streamlit==1.28+
├─ pandas
│  └─ numpy
├─ plotly==5.13+
└─ (transientes)
```

Todas están en `requirements.txt` con versiones pinned para reproducibilidad.
