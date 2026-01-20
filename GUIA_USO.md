# 📖 Guía de Uso - Estados de Interacción

## 🎯 Inicio Rápido

### 1. Activar el Entorno
```bash
cd reportes
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate     # Windows
```

### 2. Ejecutar la App
```bash
# Opción 1: Usando el script
./run.sh

# Opción 2: Directo con streamlit
streamlit run scripts/app.py

# Opción 3: Especificar puerto
streamlit run scripts/app.py --server.port=8504
```

### 3. Abrir en Navegador
La aplicación se abrirá automáticamente en `http://localhost:8503`

## 🖥️ Interfaz de Usuario

### Navegación Principal

```
┌─────────────────────────────────────────────────────┐
│              ESTADOS DE INTERACCIÓN                 │
│   Análisis de flujos de comunicación SMS y WhatsApp │
└─────────────────────────────────────────────────────┘
├─ 📊 Visión General
├─ 🔀 Flujo de Estados (Sankey)
├─ 📱 SMS
│  ├─ Estadísticas
│  ├─ Gráficos
│  └─ Datos
├─ 💬 WhatsApp
│  ├─ Estadísticas
│  ├─ Gráficos
│  └─ Datos
└─ ⚖️ Comparativa
```

### Barra Lateral (⚙️)
- Información de la aplicación
- Estadísticas en caché
- Velocidad de carga

## 📊 Secciones Detalladas

### 1. Visión General
**Qué muestra**:
- Conteo total de SMS
- Conteo total de WhatsApp
- Top 3 estados de cada canal

**Cómo usarla**:
- Obtener vista rápida del volumen
- Ver distribución inicial de estados

### 2. Diagrama Sankey
**Qué es**: Un gráfico de flujo que muestra cómo los mensajes se distribuyen entre estados

**Cómo leerlo**:
```
Ancho del flujo ∝ Cantidad de mensajes

SMS - Inicio (100%)
├─ 60% ─→ SMS - Entregado al operador
├─ 30% ─→ SMS - Fallido
└─ 10% ─→ SMS - Lista negra

WhatsApp - Inicio (100%)
├─ 50% ─→ WhatsApp - Entregado
├─ 30% ─→ WhatsApp - Leído
└─ 20% ─→ WhatsApp - Fallido
```

**Interactividad**:
- **Hover**: Ver cantidad exacta
- **Click y arrastrar**: Reorganizar nodos
- **Zoom**: Usar scroll del ratón
- **Pan**: Click derecho y arrastrar

### 3. SMS - Estadísticas
**Tab 1: Estadísticas**

Muestra en tarjetas:
- Total de mensajes SMS
- Cantidad por estado
- Porcentaje de cada estado

**Información**:
```
Total Mensajes: 315,520

Entregado al operador: 315,200 (99.9%)
Fallido: 250 (0.08%)
Lista negra: 70 (0.02%)
```

### 4. SMS - Gráficos
**Tab 2: Gráficos**

**Gráfico de Barras**:
- Eje X: Estados
- Eje Y: Cantidad
- Útil para comparar magnitudes

**Gráfico de Pastel**:
- Muestra proporciones
- Cada slice = un estado
- Porcentajes incluidos

**Cómo interpretarlos**:
```
Si el 99.9% está en "Entregado":
→ Excelente tasa de entrega
→ Operador funcionando correctamente

Si hay muchos "Fallidos":
→ Revisar configuración
→ Verificar números de teléfono
```

### 5. SMS - Datos
**Tab 3: Datos**

Muestra tabla con:
- Primeras 100 filas
- Todas las columnas
- Scroll horizontal y vertical

**Columnas importantes**:
- `id`: Identificador único
- `phone`: Número de teléfono
- `status`: Estado del envío
- `send_date`: Cuándo se envió
- `process_date`: Cuándo se procesó
- `message`: Contenido del mensaje

**Cómo usar**:
- Verificar datos crudos
- Buscar inconsistencias
- Copiar datos si es necesario

### 6. WhatsApp - Estadísticas
Similar a SMS, pero:

**Información por Envío**:
```
📄 2026-01-15 Saludo y agradecimiento firmantes
  Total: 1,001
  • Delivered: 600
  • Read: 350

📄 2026-01-16 17_57_53
  Total: 902
  • Delivered: 550
  • Read: 280
```

Click en expander para más detalles

### 7. WhatsApp - Gráficos
Mismos tipos que SMS:
- Gráfico de barras
- Gráfico de pastel

**Estados WhatsApp**:
- **Delivered**: Mensaje entregado al teléfono
- **Read**: Mensaje leído por el usuario
- **Failed**: Falló el envío
- **Processing**: Aún procesando

### 8. WhatsApp - Datos
Tabla con:
- Todos los registros de WhatsApp
- Campos: nick, phone, status, dates, etc.

### 9. Comparativa
Gráfico de barras agrupadas:

```
SMS vs WhatsApp por estado:

Estado          SMS        WhatsApp
Delivered    315,200      1,150
Read            ---          630
Failed          250          100
```

**Insights**:
- WhatsApp tiene mejor tasa de lectura
- SMS más entrega, menos lectura
- SMS tiene más fallos

## 🔍 Cómo Analizar los Datos

### Escenario 1: "¿Cuántos mensajes se entregaron?"
1. Ir a **Visión General**
2. Ver "Total Mensajes" de cada canal
3. Ir a **Comparativa** para ver lado a lado

### Escenario 2: "¿Cuál es la distribución de estados?"
1. Ir a sección **SMS** o **WhatsApp**
2. Ver **Tab Gráficos**
3. Observar gráfico de pastel para proporciones

### Escenario 3: "¿Cómo fluyen los mensajes?"
1. Ir a **Flujo de Estados (Sankey)**
2. Observar ancho de cada flujo
3. Pasar mouse para ver números exactos

### Escenario 4: "¿Cuál canal es más efectivo?"
1. Ir a **Comparativa**
2. Comparar entrega vs lectura
3. WhatsApp: mejor lectura
4. SMS: mayor volumen

## 🎨 Guía de Colores

```
🟢 Verde (#28a745)    → Leído, estados positivos
🔵 Azul (#2196F3)     → Entregado
🟣 Violeta (#9C27B0)  → Interacción positiva
🟡 Amarillo (#FFC107) → Sin interacción, procesando
🔴 Rojo (#F44336)     → Fallido, error, negativo
🟠 Naranja (#FF9800)  → Rechazado
```

## ⚡ Consejos de Rendimiento

### Si la app es lenta:
1. **Primera carga**: Esperar 5-10 segundos (cargando datos)
2. **Cambiar de tab**: Muy rápido (datos en caché)
3. **Recargar página (F5)**: Vuelve a cargar todo

### Para mejorar velocidad:
```python
# data_loader.py cambiar línea:
sms_df = load_sms_data(sample=True, sample_size=5000)
                                     ↑
                        Aumentar este número si necesita más datos
```

## 🐛 Solución de Problemas

### "No carga ningún dato"
- ✓ Verificar que los archivos CSV existen en `data/`
- ✓ Revisar rutas en `config.py`
- ✓ Ver consola para mensajes de error

### "Caracteres extraños en mensajes"
- Ir a `config.py`
- Cambiar `CSV_ENCODING["sms"]` a "UTF-8" o "ISO-8859-1"

### "El Sankey está vacío"
- Los datos son muy pequeños o no hay flujo
- Verificar `get_interaction_flow_data()` en `data_loader.py`

### "La app se cierra al cambiar de tab"
- Error en los datos
- Revisar consola para stack trace
- Verificar tipos de datos en DataFrames

## 📤 Exportar/Compartir

### Descargar Gráfico
1. Hover sobre el gráfico Plotly
2. Click en el botón de cámara (📷)
3. Guarda como PNG

### Descargar Datos
1. Ir a **SMS** o **WhatsApp**
2. Tab **Datos**
3. Copiar tabla (Ctrl+A, Ctrl+C)
4. Pegar en Excel

### Compartir Análisis
1. Captura de pantalla
2. Compartir URL (localhost:8503)
3. O exportar gráfico como PNG

## 🔐 Seguridad

### Nota Importante
- Esta es una app local (localhost)
- No se transmiten datos a servidores externos
- Los datos se almacenan en memoria
- Se pierden al cerrar la app

### Proteger Datos
- No compartir URL en internet
- App solo accesible desde esta máquina
- Para compartir, usar VPN + contraseña (futuro)

## 📞 Soporte

### Documentación
- `README.md`: Visión general
- `ARQUITECTURA.md`: Detalles técnicos
- Code comments: Explicaciones en código

### Contacto
Equipo de Análisis de Datos - Cuántico Tecnología

## 🚀 Mejoras Planeadas

Próximamente:
- [ ] Filtros por fecha
- [ ] Búsqueda de teléfonos
- [ ] Exportar a PDF
- [ ] Dashboard compartible
- [ ] Notificaciones en tiempo real

## 📝 Atajos

```bash
# Abrir app en puerto diferente
streamlit run scripts/app.py --server.port=8504

# Limpiar caché
streamlit cache clear

# Ejecutar con reloader deshabilitado
streamlit run scripts/app.py --logger.level=debug
```

## 🎓 Ejemplos

### Ejemplo 1: Analizar SMS
```
1. Abrir app
2. Ir a "📱 SMS"
3. Click en "Gráficos"
4. Observar distribución en gráfico de pastel
5. Si hay muchos "Fallidos", investigar en Tab "Datos"
```

### Ejemplo 2: Comparar Canales
```
1. Abrir app
2. Ir a "⚖️ Comparativa"
3. Ver gráfico de barras agrupadas
4. Notar que WhatsApp tiene más "Read"
5. Ir a secciones individuales para detalles
```

### Ejemplo 3: Entender Flujo
```
1. Ir a "🔀 Flujo de Estados (Sankey)"
2. Ver que SMS va 99% a "Entregado"
3. WhatsApp tiene más dispersión
4. Analizar por qué algunos "Failed"
```

¡Listo! Ahora estás listo para analizar los datos.
