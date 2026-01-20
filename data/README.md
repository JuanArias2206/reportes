# 📁 Carpeta de Datos

Esta carpeta contiene los archivos CSV que la aplicación Streamlit utiliza para generar análisis y reportes.

## 📂 Estructura

```
data/
├── mensajes_texto/
│   ├── mensajes_texto_sample.csv       # ✅ Ejemplo incluido
│   ├── interacciones_sample.csv        # ✅ Ejemplo incluido
│   ├── mensajes_texto.csv              # ⚠️ Agrega tus datos aquí
│   └── interacciones.csv               # ⚠️ Agrega tus datos aquí
└── mensajes_whatsapp/
    ├── whatsapp_sample.csv             # ✅ Ejemplo incluido
    └── *.csv                           # ⚠️ Agrega tus archivos WhatsApp aquí
```

## 🚀 Cómo Usar Tus Propios Datos

### 1. Mensajes SMS

Crea el archivo `mensajes_texto/mensajes_texto.csv` con estas columnas:

```csv
estado,numero_telefono,mensaje,url_corta,operador,codigo_corto
Delivered,573001234567,Tu mensaje aquí,http://bit.ly/abc123,Tigo,12345
Read,573101234567,Otro mensaje,http://bit.ly/def456,Movistar,12346
```

**Columnas requeridas:**
- `estado`: Delivered, Read, Sent, Failed, etc.
- `numero_telefono`: Número completo con código de país
- `mensaje`: Texto del mensaje
- `url_corta`: URL incluida en el mensaje (opcional)
- `operador`: Nombre del operador (Tigo, Movistar, Claro, etc.)
- `codigo_corto`: Código corto utilizado para enviar

### 2. Interacciones

Crea el archivo `mensajes_texto/interacciones.csv` con estas columnas:

```csv
numero_telefono,operador,codigo_corto,tipo_interaccion
573001234567,Tigo,12345,Click
573101234567,Movistar,12346,Lectura
```

**Columnas requeridas:**
- `numero_telefono`: Número completo con código de país
- `operador`: Nombre del operador
- `codigo_corto`: Código corto
- `tipo_interaccion`: Click, Lectura, Entrega, etc.

### 3. WhatsApp

Coloca tus archivos CSV de WhatsApp en `mensajes_whatsapp/` con estas columnas:

```csv
numero_telefono,estado,mensaje,operador
573001234567,Entregado,Mensaje WhatsApp,Tigo
573101234567,Fallido,Otro mensaje,Movistar
```

**Columnas requeridas:**
- `numero_telefono`: Número completo con código de país
- `estado`: Entregado, Fallido, Procesando, etc.
- `mensaje`: Texto del mensaje
- `operador`: Nombre del operador (se detectará automáticamente si falta)

## ⚠️ Nota Importante

Los archivos de datos reales NO se suben a GitHub por razones de:
- **Tamaño**: GitHub tiene límite de 100MB por archivo
- **Privacidad**: Los datos pueden contener información sensible

Solo los archivos `*_sample.csv` están incluidos en el repositorio como ejemplos.

## 🔧 Formato de Números Telefónicos

Los números pueden estar en cualquiera de estos formatos:
- Con código internacional: `+573001234567`
- Sin símbolo +: `573001234567`
- Solo el número móvil: `3001234567`

La aplicación los procesará automáticamente y validará según reglas colombianas.

## 📊 Tamaño Recomendado

Para mejor rendimiento:
- **SMS**: Hasta 500K registros (procesamiento optimizado)
- **WhatsApp**: Hasta 10K registros
- **Interacciones**: Hasta 500K registros

La app utiliza muestreo inteligente para archivos grandes, manteniendo tiempos de respuesta de 2-3 segundos.
