# 🇨🇴 Validador de Números Telefónicos de Colombia

Sistema completo de validación de números telefónicos móviles colombianos con detección de operadores, patrones sospechosos y análisis estadístico.

## 📋 Características

✅ **Limpieza Automática**
- Elimina espacios, guiones, paréntesis y caracteres especiales
- Normaliza formato con o sin +57
- Maneja múltiples formatos de entrada

📱 **Validación Completa**
- Verifica longitud (10 dígitos después de +57)
- Valida que sea número móvil (comienza con 3)
- Verifica prefijo contra operadores válidos

🔍 **Detección de Patrones Sospechosos**
- Números con todos los dígitos iguales
- Secuencias numéricas (ascendentes/descendentes)
- Patrones repetitivos
- Terminaciones en muchos ceros

📡 **Identificación de Operadores**
- Tigo (300-306)
- Movistar (310-319, 321-323)
- Claro (315, 320, 324-325)
- Avantel (350-352)
- ETB (353-355)
- WOM (356-357)
- Virgin Mobile (328-329)
- Éxito Móvil (358-359)
- Flash Mobile (334)

📊 **Análisis Estadístico**
- Conteo de válidos/inválidos
- Distribución por operador
- Detección de números repetidos
- Clasificación por categorías de error

## 🚀 Instalación

```bash
# Clonar o descargar los archivos
cd reportes

# Activar entorno virtual (si aplica)
source venv/bin/activate

# Las dependencias ya están instaladas (pandas, streamlit)
```

## 📁 Archivos del Proyecto

```
reportes/
├── scripts/
│   ├── phone_validator.py      # Módulo principal de validación
│   └── validador_app.py         # Aplicación Streamlit
├── test_validator.py            # Suite de pruebas
└── VALIDADOR_NUMEROS.md         # Esta documentación
```

## 💻 Uso

### 1. Uso Programático (Python)

```python
from scripts.phone_validator import (
    validar_numero_colombiano,
    validar_lista_numeros,
    analizar_resultados
)

# Validar un número individual
resultado = validar_numero_colombiano("+573001234567")

print(resultado['valido'])           # True
print(resultado['operador'])         # "Tigo"
print(resultado['numero_completo'])  # "+573001234567"
print(resultado['sospechoso'])       # False

# Validar una lista de números
numeros = [
    "573001234567",
    "3151234567",
    "+573201234567",
    "573725270507"  # Inválido
]

df_resultados = validar_lista_numeros(numeros)
print(df_resultados[['numero_completo', 'valido', 'operador']])

# Obtener estadísticas
stats = analizar_resultados(df_resultados)
print(f"Válidos: {stats['validos']}")
print(f"Por operador: {stats['operadores']}")
```

### 2. Aplicación Streamlit

```bash
# Ejecutar la aplicación web
streamlit run scripts/validador_app.py
```

La aplicación se abrirá en `http://localhost:8501` con tres secciones:

- **🔍 Validar Número**: Validación individual con detalles
- **📋 Validar Lista**: Validación masiva con estadísticas
- **📘 Documentación**: Reglas y ejemplos

### 3. Ejecutar Pruebas

```bash
# Ejecutar suite completa de pruebas
python test_validator.py
```

Esto ejecutará 6 conjuntos de pruebas:
1. Limpieza de números
2. Identificación de operadores
3. Detección de patrones sospechosos
4. Validación completa
5. Validación de lista
6. Casos extremos

## 📖 Ejemplos de Uso

### Ejemplo 1: Validación Simple

```python
from scripts.phone_validator import validar_numero_colombiano

# Número válido con espacios
resultado = validar_numero_colombiano("57 300 123 4567")

if resultado['valido']:
    print(f"✅ Válido - Operador: {resultado['operador']}")
else:
    print(f"❌ Inválido - Error: {resultado['mensaje_error']}")
```

### Ejemplo 2: Validar Desde DataFrame

```python
import pandas as pd
from scripts.phone_validator import validar_lista_numeros, analizar_resultados

# Cargar datos
df = pd.read_csv('clientes.csv')
numeros = df['telefono'].tolist()

# Validar
df_validacion = validar_lista_numeros(numeros)

# Filtrar solo válidos
validos = df_validacion[df_validacion['valido']]

# Guardar resultados
df_validacion.to_csv('validacion_resultados.csv', index=False)

# Ver estadísticas
stats = analizar_resultados(df_validacion)
print(f"Tasa de validez: {stats['porcentaje_validos']}%")
print(f"Por operador: {stats['operadores']}")
```

### Ejemplo 3: Integración con Aplicación Existente

```python
# En tu aplicación actual (app.py o data_loader.py)
from scripts.phone_validator import validar_numero_colombiano

def procesar_whatsapp_data(df):
    """Procesa datos de WhatsApp con validación colombiana."""
    
    # Agregar columna de validación
    df['validacion'] = df['Phone number'].apply(
        lambda x: validar_numero_colombiano(str(x))
    )
    
    # Extraer campos útiles
    df['numero_valido'] = df['validacion'].apply(lambda x: x['valido'])
    df['operador'] = df['validacion'].apply(lambda x: x['operador'])
    df['es_sospechoso'] = df['validacion'].apply(lambda x: x['sospechoso'])
    
    # Filtrar solo válidos
    df_validos = df[df['numero_valido']].copy()
    
    return df_validos
```

## 📊 Estructura de Respuesta

### `validar_numero_colombiano(numero)` retorna:

```python
{
    'numero_original': str,      # Número tal como se ingresó
    'numero_limpio': str,        # Número sin +57 ni caracteres
    'numero_completo': str,      # Formato +573001234567
    'valido': bool,              # True si cumple todas las reglas
    'categoria': str,            # Ver categorías abajo
    'operador': str,             # Tigo, Movistar, Claro, etc.
    'mensaje_error': str,        # Descripción del error si aplica
    'sospechoso': bool,          # True si tiene patrón sospechoso
    'razon_sospecha': str        # Explicación si es sospechoso
}
```

### Categorías Posibles

| Categoría | Descripción |
|-----------|-------------|
| `Válido` | Cumple todas las reglas |
| `Válido (Sospechoso)` | Válido pero con patrón sospechoso |
| `Vacío` | Número nulo o vacío |
| `Formato inválido` | Contiene caracteres no válidos |
| `Longitud inválida` | No tiene exactamente 10 dígitos |
| `No es celular` | No comienza con 3 |
| `Prefijo inválido` | Prefijo no corresponde a operador conocido |

## 🔍 Reglas de Validación

### 1. Formato Válido

Un número colombiano válido debe:
- Tener 10 dígitos (sin contar +57)
- Comenzar con 3 (números móviles)
- Tener prefijo de operador válido (3 primeros dígitos)

**Ejemplos válidos:**
```
+573001234567    ✅ Formato internacional
573001234567     ✅ Con código país
3001234567       ✅ Sin código país
57 300 123 4567  ✅ Con espacios (se limpian)
57-300-123-4567  ✅ Con guiones (se limpian)
```

### 2. Prefijos por Operador

| Operador | Prefijos | Ejemplo |
|----------|----------|---------|
| **Tigo** | 300-306 | 3001234567 |
| **Movistar** | 310-319, 321-323 | 3101234567 |
| **Claro** | 315, 320, 324-325 | 3151234567 |
| **Avantel** | 350-352 | 3501234567 |
| **ETB** | 353-355 | 3541234567 |
| **WOM** | 356-357 | 3561234567 |
| **Virgin Mobile** | 328-329 | 3281234567 |
| **Éxito Móvil** | 358-359 | 3581234567 |
| **Flash Mobile** | 334 | 3341234567 |

### 3. Patrones Sospechosos

El validador detecta (pero no rechaza) estos patrones:

| Patrón | Ejemplo | Razón |
|--------|---------|-------|
| Todos iguales | 3111111111 | Todos los dígitos son iguales |
| Muchos ceros | 3001230000 | Termina en 4 o más ceros |
| Secuencia ascendente | 3012345678 | Contiene secuencia ascendente |
| Secuencia descendente | 3098765432 | Contiene secuencia descendente |
| Repetición consecutiva | 3001111123 | Más de 4 dígitos consecutivos iguales |
| Patrón repetitivo | 3012121212 | Patrón ABABABAB |

## 🧪 Casos de Prueba

### Casos Válidos

```python
casos_validos = [
    "+573001234567",     # Tigo
    "3151234567",        # Claro (sin +57)
    "57 310 123 4567",   # Movistar (con espacios)
    "57-320-123-4567",   # Claro (con guiones)
]
```

### Casos Inválidos

```python
casos_invalidos = [
    "573725270507",      # Prefijo 372 no reconocido
    "57312345",          # Solo 5 dígitos (muy corto)
    "2123456789",        # Comienza con 2 (no es celular)
    "57300123456789",    # Muy largo (13 dígitos)
    "",                  # Vacío
    "abc123",            # Contiene letras
]
```

### Casos Sospechosos (pero válidos)

```python
casos_sospechosos = [
    "3111111111",        # Todos los dígitos iguales
    "3001230000",        # Termina en muchos ceros
    "3012345678",        # Secuencia numérica
    "3012121212",        # Patrón repetitivo
]
```

## 📈 Estadísticas Generadas

La función `analizar_resultados(df)` retorna:

```python
{
    'total': int,                    # Total de números procesados
    'validos': int,                  # Cantidad de válidos
    'invalidos': int,                # Cantidad de inválidos
    'porcentaje_validos': float,     # % de válidos
    'porcentaje_invalidos': float,   # % de inválidos
    'categorias': dict,              # Conteo por categoría
    'operadores': dict,              # Conteo por operador (solo válidos)
    'sospechosos': int,              # Cantidad de sospechosos
    'porcentaje_sospechosos': float, # % de sospechosos
    'numeros_repetidos': int,        # Cantidad de números duplicados
    'top_repetidos': dict            # Top 10 números más repetidos
}
```

## 🔧 Personalización

### Agregar Nuevo Operador

Edita `phone_validator.py`:

```python
PREFIJOS_OPERADORES = {
    # ... operadores existentes ...
    'Nuevo Operador': [
        (360, 362),  # Rango de prefijos
    ],
}
```

### Agregar Nueva Validación

```python
def validar_numero_colombiano(numero: str) -> Dict:
    # ... código existente ...
    
    # Agregar tu validación personalizada
    if tu_condicion:
        resultado['categoria'] = 'Tu Categoría'
        resultado['mensaje_error'] = 'Tu mensaje'
        return resultado
    
    # ... resto del código ...
```

### Modificar Detección de Sospechosos

```python
def detectar_patron_sospechoso(numero_movil: str) -> Tuple[bool, str]:
    # ... patrones existentes ...
    
    # Agregar tu patrón
    if tu_patron_sospechoso(numero_movil):
        return True, "Tu razón de sospecha"
    
    # ... resto del código ...
```

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'phone_validator'`

```bash
# Asegúrate de ejecutar desde el directorio correcto
cd /Users/mac/Documents/trabajo/cuantico/reportes

# O usa el path completo
python test_validator.py
```

### Error: Pandas/Streamlit no instalado

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (si no están)
pip install pandas streamlit
```

### Los resultados no son los esperados

1. Verifica el formato del número de entrada
2. Revisa los prefijos válidos en `PREFIJOS_OPERADORES`
3. Ejecuta las pruebas: `python test_validator.py`

## 📝 Notas Importantes

⚠️ **Prefijos Actualizados**: Los prefijos de operadores pueden cambiar. Verifica periódicamente con el MinTIC.

⚠️ **Solo Números Móviles**: Este validador está diseñado solo para números móviles (celulares) que comienzan con 3.

⚠️ **Números Sospechosos**: Un número marcado como "sospechoso" NO es necesariamente inválido, solo tiene un patrón que puede requerir revisión.

⚠️ **Detección de Duplicados**: La detección de repetidos se basa en el número limpio (sin +57).

## 🤝 Integración con App Existente

Para integrar con tu aplicación actual de reportes:

```python
# En data_loader.py
from phone_validator import validar_numero_colombiano

def get_whatsapp_failed_analysis(df: pd.DataFrame) -> Dict:
    # ... código existente ...
    
    # Agregar validación colombiana
    df['validacion_col'] = df['Phone number'].apply(
        lambda x: validar_numero_colombiano(str(x))
    )
    
    # Análisis por operador
    by_operator = {}
    for _, row in df[df['validacion_col'].apply(lambda x: x['valido'])].iterrows():
        op = row['validacion_col']['operador']
        by_operator[op] = by_operator.get(op, 0) + 1
    
    return {
        # ... retornos existentes ...
        'by_operator_colombiano': by_operator,
    }
```

## 📞 Contacto y Soporte

Para reportar errores o sugerir mejoras, crea un issue o contacta al equipo de desarrollo.

---

**Desarrollado con ❤️ para análisis de datos de telecomunicaciones en Colombia**
