# 💭 ANÁLISIS DE SENTIMIENTOS CON OPENAI - GUÍA COMPLETA

## 📋 Resumen Ejecutivo

Se ha completado la integración de análisis de sentimientos usando OpenAI API para analizar 315K+ mensajes de interacciones.

**Datos Disponibles:**
- Total de mensajes: 315,914
- Mensajes únicos: ~315,874  
- Operadores: 9 (Claro, Tigo, Movistar, etc.)
- Códigos cortos: 4 (890083, 897781, 87736, null)

## 🎯 Componentes Implementados

### 1. Módulo `sentiment_analyzer.py`
Ubicación: `scripts/sentiment_analyzer.py`

**Funciones principales:**
```python
analyze_sentiment(message, use_cache=True)      # Analiza un mensaje
analyze_multiple_messages(messages, batch_size) # Procesa lotes
get_sentiment_summary(sentiments)               # Genera resumen
```

**Características:**
- ✅ Sistema de caché persistente (evita reprocesar)
- ✅ API Key desde variables de entorno (seguro)
- ✅ Modelo: gpt-3.5-turbo
- ✅ Clasificación: Positivo, Negativo, Neutral

### 2. Funciones en `data_loader.py`
```python
get_interacciones_messages(limit)       # Carga mensajes
get_unique_messages(limit)              # Mensajes únicos
get_sentiment_stats_by_operator()       # Stats por operador
get_sentiment_stats_by_codigo()         # Stats por código
```

### 3. Nueva Tab en App: "💭 Sentimientos"
Ubicación: Sección de Interacciones → Tab 6

**Interfaz:**
1. Botón "🚀 Iniciar Análisis"
2. Barra de progreso interactiva
3. Métricas: Positivos, Negativos, Neutrales, Confianza
4. Gráficos: Pie chart + Bar chart
5. Tabla colorizada por sentimiento

## 📊 Estadísticas de Interacciones

```
Por Operador (Top 5):
  1. Claro:     173,759 (173,741 únicos)
  2. Tigo:       74,158 (74,148 únicos)
  3. Movistar:   47,479 (47,477 únicos)
  4. Avantel:    12,346 (12,346 únicos)
  5. Virgin:      3,611 (3,611 únicos)
  + 4 operadores más

Por Código Corto (Top 4):
  1. 890083:    234,505 mensajes (234,484 únicos)
  2. 897781:     76,458 mensajes (76,448 únicos)
  3. 87736:       3,611 mensajes (3,611 únicos)
  4. null:        1,335 mensajes (1,335 únicos)
```

## 🔐 Configuración de API

**API Key (variables de entorno):**
```bash
export OPENAI_API_KEY="sk-..."
```

**En Streamlit Cloud:**
1. Ir a Settings del proyecto
2. Agregar secreto: `OPENAI_API_KEY = "sk-..."`

**Modelo:**
- Nombre: gpt-3.5-turbo
- Temperatura: 0.3 (consistente)
- Max tokens: 100

## 💾 Sistema de Caché

**Ubicación:** `data/.sentiment_cache.json`

**Estructura:**
```json
{
  "md5_hash_del_mensaje": {
    "mensaje": "...",
    "sentimiento": "positivo|negativo|neutral",
    "confianza": 0.0-1.0,
    "razon": "..."
  }
}
```

**Beneficios:**
- No reprocesa mensajes
- Ahorra costos de API
- Rápido en reboots
- Persiste entre sesiones

## 🚀 Pasos para Usar

### 1. Configurar API Key
```bash
# Local
export OPENAI_API_KEY="sk-..."

# O en archivo .env
echo 'OPENAI_API_KEY="sk-..."' > .env
```

### 2. Reboot Streamlit Cloud
- Dashboard → "reportes" → ⋮ → "Reboot app"
- Esperar 1-2 minutos

### 3. Usar en Interfaz
- Ir a: 💌 ANÁLISIS DE INTERACCIONES
- Tab 6: 💭 Sentimientos
- Click en: 🚀 Iniciar Análisis
- Esperar procesamiento (2-5 min primera vez)
- Ver resultados

## 📈 Rendimiento Esperado

**Primera ejecución:** ~2-5 minutos (500 mensajes)
**Ejecuciones posteriores:** <1 segundo (caché)
**Costo API:** ~$0.50-1.00 por 500 mensajes

## ✅ Validación Local

```bash
cd /Users/mac/Documents/trabajo/cuantico/reportes
python3 test_datos_interacciones.py
```

Verifica:
- ✅ Carga de 315K+ mensajes
- ✅ Identifica mensajes únicos
- ✅ Estadísticas por operador (9)
- ✅ Estadísticas por código (4)

## 🔍 Solucionar Problemas

### "API Key no configurada"
```bash
# Verificar API key
echo $OPENAI_API_KEY

# Si está vacío, configurar
export OPENAI_API_KEY="sk-..."
```

### "Error: No hay mensajes disponibles"
- Verificar que parquet de interacciones existe
- Ejecutar: `python3 test_datos_interacciones.py`

### Mensaje: "Error durante análisis"
- Verificar API key es válida
- Verificar cuota de OpenAI
- Revisar logs de Streamlit Cloud

## 📝 Roadmap Futuro

- [ ] Exportar resultados a CSV/Excel
- [ ] Análisis de tendencias de sentimientos
- [ ] Comparación por operador/código
- [ ] Alertas de sentimientos negativos
- [ ] Dashboard de seguimiento

---

**Commits:**
- `37d87ce`: Feature módulo sentiment_analyzer
- `623eec0`: Feature tab de sentimientos en app

**Estado:** ✅ LISTO PARA REBOOT STREAMLIT CLOUD
