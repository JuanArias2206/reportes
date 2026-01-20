# 🎉 ¡Bienvenido a Estados de Interacción!

## ✅ Aplicación Completamente Configurada

Tu aplicación Streamlit para visualizar estados de mensajes está **completamente lista** para usar.

## 🚀 Cómo Iniciar

### Opción 1: Script Automático (Recomendado)
```bash
cd /Users/mac/Documents/trabajo/cuantico/reportes
./run.sh
```

### Opción 2: Comando Directo
```bash
cd /Users/mac/Documents/trabajo/cuantico/reportes
source venv/bin/activate
streamlit run scripts/app.py
```

### Opción 3: Desde cualquier lugar
```bash
cd /Users/mac/Documents/trabajo/cuantico/reportes
./run.sh
```

La aplicación se abrirá en `http://localhost:8503`

## 📁 Estructura del Proyecto

```
reportes/
├── 📄 README.md                # Documentación completa
├── 📄 ARQUITECTURA.md          # Detalles técnicos
├── 📄 GUIA_USO.md              # Cómo usar la app
├── 📄 WELCOME.md               # Este archivo
├── 📄 requirements.txt         # Dependencias
├── 🐚 run.sh                   # Script de inicio
│
├── 📁 scripts/                 # Código fuente
│   ├── app.py                  # Aplicación Streamlit
│   ├── config.py               # Configuración centralizada
│   ├── data_loader.py          # Carga de datos
│   ├── visualizations.py       # Gráficos
│   ├── utils.py                # Utilidades
│   └── visor.py                # Módulo adicional
│
├── 📁 data/                    # Datos
│   ├── 📁 mensajes_texto/      # SMS (132 MB)
│   │   └── mensajes_texto.csv
│   └── 📁 mensajes_whatsapp/   # WhatsApp
│       ├── 2026-01-15...csv
│       └── 2026-01-16...csv
│
└── 📁 venv/                    # Entorno virtual
    └── (dependencias)
```

## 🎯 Lo que puede hacer la aplicación

### 📊 Visualizaciones
- ✅ Diagrama Sankey interactivo
- ✅ Gráficos de barras
- ✅ Gráficos de pastel
- ✅ Series temporales
- ✅ Comparativa SMS vs WhatsApp

### 📈 Análisis
- ✅ 315,520 registros SMS analizados
- ✅ 1,903 registros WhatsApp analizados
- ✅ Cálculo de estadísticas
- ✅ Distribución de estados
- ✅ Flujos de interacción

### ⚡ Rendimiento
- ✅ Carga eficiente de datos grandes (132 MB)
- ✅ Muestreo inteligente
- ✅ Caché automático
- ✅ UI rápida y responsiva

### 🎨 Diseño
- ✅ Interfaz limpia y moderna
- ✅ Colores intuitivos
- ✅ Paleta consistente
- ✅ Responsive design

## 📚 Documentación

1. **README.md** - Comienza aquí
   - Características
   - Instalación
   - Uso básico

2. **GUIA_USO.md** - Cómo usar la app
   - Inicio rápido
   - Explicación de cada sección
   - Ejemplos prácticos
   - Solución de problemas

3. **ARQUITECTURA.md** - Para desarrolladores
   - Estructura modular
   - Cómo funciona cada módulo
   - Extensibilidad
   - Mejoras futuras

## 🔑 Conceptos Clave

### Estados de SMS
- **Entregado al operador**: Envío exitoso (99.9%)
- **Fallido**: No se pudo enviar (0.08%)
- **Lista negra**: Usuario no quiere más mensajes (0.02%)

### Estados de WhatsApp
- **Delivered**: Llegó al teléfono
- **Read**: Usuario vio el mensaje
- **Failed**: No se pudo entregar
- **Processing**: Aún procesando

### Diagrama Sankey
Muestra cómo los mensajes fluyen de un estado a otro:
```
Inicio (100% mensajes)
├─ 60% → Entregado
├─ 30% → Fallido
└─ 10% → Rechazado
```

## 💡 Casos de Uso

### 1. Verificar Entrega de Campaña
```
Abrir app → SMS → Estadísticas
Ver: 99.9% entregado ✓
```

### 2. Comparar Canales
```
Abrir app → Comparativa
Ver: WhatsApp tiene mejor lectura
```

### 3. Analizar Fallos
```
Abrir app → SMS → Datos
Filtrar por "Fallido"
Investigar por qué falló
```

### 4. Entender Flujos
```
Abrir app → Sankey
Ver: Cómo se distribuyen los mensajes
```

## 🛠️ Requisitos del Sistema

- ✅ Python 3.8+ 
- ✅ pip
- ✅ macOS/Linux/Windows
- ✅ ~200 MB libre en disco
- ✅ Conexión a internet (primera instalación)

## 📊 Datos Analizados

### SMS
```
Archivo: mensajes_texto.csv
Tamaño: 132 MB
Registros: 315,520
Campos: 16+ columnas
Período: 2026-01-15 a 2026-01-17
```

### WhatsApp
```
Archivo 1: 2026-01-15... (1,001 registros)
Archivo 2: 2026-01-16... (902 registros)
Total: 1,903 registros
Campos: 11 columnas
Período: Enero 2026
```

## 🎓 Primeros Pasos

1. **Abre la app**
   ```bash
   ./run.sh
   ```

2. **Explora Visión General**
   - Mira los totales de cada canal

3. **Ve el Sankey**
   - Entiende el flujo de estados

4. **Analiza SMS**
   - Observa estadísticas detalladas

5. **Compara Canales**
   - Ve diferencias entre SMS y WhatsApp

6. **Lee la documentación**
   - Para entender qué significan los números

## 🤔 Preguntas Frecuentes

**P: ¿Es lenta la app?**
R: No, es muy rápida. La primera carga tarda 5-10s (caché), después es instantáneo.

**P: ¿Puedo cambiar el puerto?**
R: Sí: `streamlit run scripts/app.py --server.port=8504`

**P: ¿Se pierden los datos al cerrar?**
R: Sí, son en memoria. Solo se cargan mientras la app está abierta.

**P: ¿Puedo exportar gráficos?**
R: Sí, click en la cámara en la esquina superior derecha de cada gráfico.

**P: ¿Dónde están los logs?**
R: En la consola donde ejecutaste `./run.sh`

## 🚀 Mejoras Futuras

Planeadas para versiones posteriores:
- Filtros por fecha
- Búsqueda de teléfonos
- Exportar a PDF
- Dashboard compartible
- Base de datos
- API REST

## 📞 Contacto / Soporte

Equipo de Análisis de Datos
Cuántico Tecnología
Enero 2026

---

## ✨ Resumen

Tu aplicación tiene:

✅ **5 módulos** Python bien estructurados
✅ **3 documentos** de guía completa
✅ **8 secciones** de análisis
✅ **6 tipos** de visualizaciones
✅ **315k+** registros analizados
✅ **Código modular** y escalable
✅ **Rendimiento** optimizado
✅ **UI moderna** e intuitiva

### Ahora... ¡A explorar!

```bash
./run.sh
```

Abre tu navegador en http://localhost:8503 y comienza a analizar. 📊
