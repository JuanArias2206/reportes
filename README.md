# 📊 Sistema de Análisis de Mensajería SMS/WhatsApp

Sistema completo de análisis y visualización de datos para campañas de mensajería SMS y WhatsApp, con validación de números telefónicos colombianos y análisis de calidad de datos.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Características Principales

### 📱 Análisis de SMS
- ✅ Procesamiento de 315K+ registros con rendimiento optimizado (2-3 segundos)
- 📊 Visualización de estados de envío (Delivered, Failed, Read, etc.)
- 🔄 Diagramas de flujo Sankey interactivos
- 📈 Análisis de engagement: clicks en URLs
- 🎨 Gráficos interactivos con Plotly
- ⚡ Muestreo inteligente y extrapolación estadística

### 💬 Análisis de WhatsApp
- 📊 Análisis de 1.9K+ mensajes WhatsApp
- 🔍 **Análisis de Calidad de Datos (DQ)** avanzado
- ✅ Validación de números telefónicos colombianos
- 📡 Identificación de operadores (Tigo, Movistar, Claro, Avantel, ETB, WOM, etc.)
- ⚠️ Detección de patrones sospechosos
- 🔴 Análisis de mensajes fallidos y en procesamiento
- 🏷️ Categorización de problemas de validación

### 💌 Análisis de Interacciones
- 📊 Análisis de 315K+ interacciones multicanal
- 📡 Distribución por operadores
- 🔢 Análisis por códigos cortos
- 🔄 Flujos de interacción
- 📈 Visualizaciones comparativas

### 🇨🇴 Validador de Números Telefónicos Colombia
- ✅ Validación completa según reglas colombianas
- 📱 Detección de operadores por prefijo
- 🔍 Identificación de patrones sospechosos
- 📊 Aplicación web interactiva con Streamlit
- 🧪 Suite completa de pruebas

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes Python)

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/reportes-mensajeria.git
cd reportes-mensajeria

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
reportes/
├── scripts/
│   ├── app.py                   # Aplicación principal de reportes
│   ├── config.py                # Configuración general
│   ├── data_loader.py           # Carga y procesamiento de datos
│   ├── visualizations.py        # Gráficos y visualizaciones
│   ├── utils.py                 # Utilidades generales
│   ├── phone_validator.py       # Módulo de validación de teléfonos
│   └── validador_app.py         # App web del validador
├── data/
│   ├── mensajes_texto/          # Datos SMS e Interacciones
│   └── mensajes_whatsapp/       # Datos WhatsApp
├── test_validator.py            # Suite de pruebas del validador
├── ejemplo_validador.py         # Ejemplos de uso del validador
├── requirements.txt             # Dependencias Python
├── .gitignore                   # Archivos ignorados por Git
├── README.md                    # Este archivo
└── docs/                        # Documentación adicional
    ├── VALIDADOR_NUMEROS.md     # Docs del validador
    ├── README_VALIDADOR.md      # Guía rápida
    ├── ARQUITECTURA.md          # Arquitectura
    └── GUIA_USO.md             # Guía de uso
```

## 💻 Uso

### 📦 Datos de Ejemplo

El repositorio incluye archivos CSV de muestra para probar la aplicación:
- `data/mensajes_texto/mensajes_texto_sample.csv` - 5 mensajes SMS de ejemplo
- `data/mensajes_texto/interacciones_sample.csv` - 5 interacciones de ejemplo  
- `data/mensajes_whatsapp/whatsapp_sample.csv` - 4 mensajes WhatsApp de ejemplo

**Para usar tus propios datos:**
1. Coloca tus archivos CSV en las carpetas correspondientes dentro de `data/`
2. Asegúrate de que tengan las mismas columnas que los archivos de ejemplo
3. La app detectará automáticamente los archivos disponibles

### Aplicación Principal de Reportes

```bash
streamlit run scripts/app.py
```

La aplicación se abrirá en `http://localhost:8505` con tres secciones:
1. **📱 SMS** - Análisis completo de mensajes SMS
2. **💬 WhatsApp** - Análisis de WhatsApp con validación colombiana
3. **💌 Interacciones** - Análisis de interacciones multicanal

### Validador de Números Telefónicos

```bash
# Aplicación web interactiva
streamlit run scripts/validador_app.py

# Ejecutar ejemplos
python ejemplo_validador.py

# Ejecutar pruebas
python test_validator.py
```

### Uso Programático

```python
from scripts.phone_validator import validar_numero_colombiano

# Validar un número
resultado = validar_numero_colombiano("+573001234567")
print(resultado['valido'])    # True
print(resultado['operador'])  # "Tigo"
```

## 📊 Características Técnicas

### Optimizaciones de Rendimiento
- ⚡ **Muestreo inteligente**: Procesa 10K registros de 315K con extrapolación estadística
- 🎯 **Caching**: Sistema de caché con `@st.cache_data` para evitar recálculos
- 📦 **Tipos optimizados**: Uso de `Int16` y `category` para reducir memoria
- 🔄 **Lectura por chunks**: Procesamiento eficiente de archivos grandes
- 📈 **Carga asíncrona**: Datos se cargan bajo demanda

### Validación de Números Colombianos
- ✅ **Formato**: Acepta +57, 57, o sin código de país
- 📏 **Longitud**: Valida 10 dígitos después de +57
- 3️⃣ **Celular**: Verifica que comience con 3
- 📡 **Operadores**: Identifica 9 operadores por prefijo
- 🔍 **Patrones sospechosos**: Detecta 5 tipos de patrones inusuales

#### Operadores Soportados
| Operador | Prefijos |
|----------|----------|
| Tigo | 300-306 |
| Movistar | 310-314, 316-319, 321-323 |
| Claro | 315, 320, 324-325 |
| Avantel | 350-352 |
| ETB | 353-355 |
| WOM | 356-357 |
| Virgin Mobile | 328-329 |
| Éxito Móvil | 358-359 |
| Flash Mobile | 334 |

#### Patrones Sospechosos Detectados
- 🔢 Todos dígitos iguales: `3111111111`
- 🔄 Secuencias numéricas: `3012345678`, `3098765432`
- ⚡ Patrones alternantes: `3012121212`
- 0️⃣ Termina en muchos ceros: `3001230000`
- 🔁 Dígitos consecutivos: `3001111123`

## 📖 Documentación

- **[VALIDADOR_NUMEROS.md](VALIDADOR_NUMEROS.md)** - Documentación completa del validador
- **[README_VALIDADOR.md](README_VALIDADOR.md)** - Guía rápida del validador
- **[ARQUITECTURA.md](ARQUITECTURA.md)** - Arquitectura del sistema
- **[GUIA_USO.md](GUIA_USO.md)** - Guía de uso detallada

## 🧪 Pruebas

```bash
# Validador de números
python test_validator.py

# Ejemplo completo
python ejemplo_validador.py

# Test de chunks
python test_chunks.py
```

## 🔧 Configuración

### Archivos de Datos

El sistema espera los siguientes archivos en `data/`:

```
data/
├── mensajes_texto/
│   ├── mensajes_texto.csv       # SMS (131.9MB, 315K registros)
│   └── interacciones.csv        # Interacciones (76MB, 315K registros)
└── mensajes_whatsapp/
    ├── archivo1.csv              # WhatsApp
    └── archivo2.csv              # WhatsApp
```

**Nota:** Los archivos CSV no se incluyen en el repositorio por su tamaño y privacidad. Asegúrate de tenerlos en la carpeta `data/` antes de ejecutar.

### Variables de Configuración

Edita `scripts/config.py` para ajustar:
- Rutas de archivos
- Encodings (LATIN1 para SMS, UTF-8 para WhatsApp)
- Delimitadores (`;` para SMS, `,` para WhatsApp)
- Tamaños de muestra

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

### v2.0.0 - 2026-01-20
- ✅ Integración completa del validador de números colombianos
- ✅ Detección de patrones sospechosos
- ✅ Análisis de calidad de datos mejorado
- ✅ Categorización de problemas de validación
- ✅ Nuevos gráficos y visualizaciones

### v1.5.0 - 2026-01-19
- ✅ Optimización de rendimiento (2-3s de carga)
- ✅ Diagramas Sankey mejorados
- ✅ Análisis de engagement con URLs
- ✅ UI mejorada con CSS personalizado

### v1.0.0 - 2026-01-15
- 🎉 Versión inicial
- 📊 Análisis básico de SMS y WhatsApp
- 🔄 Diagramas de flujo Sankey

## 🐛 Reporte de Errores

Si encuentras un bug, por favor abre un [issue](https://github.com/tu-usuario/reportes-mensajeria/issues) con:
- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado
- Screenshots (si aplica)
- Versión de Python y Streamlit

## 📊 Rendimiento

- **Carga inicial**: 2-3 segundos (315K registros)
- **Cambio de tabs**: <1 segundo (con cache)
- **Validación de números**: ~100 números/segundo
- **Memoria**: ~200MB en uso normal

## 🔒 Seguridad y Privacidad

- ⚠️ Los archivos CSV con datos personales NO están en el repositorio
- ⚠️ Asegúrate de agregar `data/*.csv` al `.gitignore` para producción
- ⚠️ Usa variables de entorno para credenciales si las necesitas
- ✅ El `.gitignore` ya está configurado para proteger datos sensibles

### 🚫 Error al subir archivos >100MB (GitHub)

Si ves el aviso de “Files Too Large” al intentar commitear `data/mensajes_texto/mensajes_texto.csv`, sigue estos pasos:

1) Agregar reglas de ignore (ya incluidas): `.gitignore` ignora todos los CSV reales y mantiene solo los `*_sample.csv`.
2) Retirar el archivo grande del índice de Git si ya está staged:

```bash
git rm --cached data/mensajes_texto/mensajes_texto.csv
git rm --cached data/mensajes_texto/interacciones.csv  # si aplica
git rm --cached data/mensajes_whatsapp/*.csv           # mantiene los sample
git add .
git commit -m "Ignorar datos grandes; usar muestras para cloud"
git push
```

Opcional: si necesitas versionar archivos grandes de forma controlada, usa Git LFS:

```bash
brew install git-lfs    # macOS
git lfs install
git lfs track "data/mensajes_texto/*.csv"
git add .gitattributes
git add data/mensajes_texto/*.csv
git commit -m "Track datos grandes con Git LFS"
git push
```

Nota: La app detecta automáticamente si existen archivos reales en `data/` y, si no están, usa los `*_sample.csv` para que la ejecución en la nube funcione sin problemas.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autor

- **Juan** - Desarrollo y arquitectura

## 🙏 Agradecimientos

- [Streamlit](https://streamlit.io/) por el framework de visualización
- [Plotly](https://plotly.com/) por los gráficos interactivos
- [Pandas](https://pandas.pydata.org/) por el procesamiento de datos
- Comunidad Python por las herramientas open source

## 📞 Contacto

Para preguntas o soporte, abre un [issue](https://github.com/tu-usuario/reportes-mensajeria/issues) en GitHub.

---

**Desarrollado con ❤️ para análisis de datos de telecomunicaciones en Colombia**

## ⭐ Si te gusta este proyecto, dale una estrella!

---

## 🚀 Inicio Rápido (TL;DR)

```bash
# Clonar, instalar y ejecutar
git clone https://github.com/tu-usuario/reportes-mensajeria.git
cd reportes-mensajeria
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
streamlit run scripts/app.py
```

Luego abre: http://localhost:8505 🎉
