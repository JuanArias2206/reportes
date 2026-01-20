# 🚨 INSTRUCCIONES PARA REBOOT EN STREAMLIT CLOUD

## Problema Actual
La app en Streamlit Cloud muestra errores porque:
1. Tiene archivos `sample` cacheados
2. No ha rebuildeado después de los últimos commits

## ✅ Solución: Forzar Reboot Manual

### Opción 1: Reboot desde el Dashboard (MÁS RÁPIDO)
1. Ve a https://share.streamlit.io/
2. Busca tu app "reportes"
3. Click en **"⋮" (menú de 3 puntos)** → **"Reboot app"**
4. Espera 1-2 minutos
5. ✅ La app se recargará con los archivos correctos

### Opción 2: Clear Cache desde la App
1. Abre tu app en Streamlit Cloud
2. Click en **"☰"** (hamburger menu arriba derecha)
3. Click en **"Clear cache"**
4. Recarga la página

### Opción 3: Delete y Redeploy (ÚLTIMA OPCIÓN)
1. En el dashboard, elimina la app
2. Crea nueva app apuntando al mismo repo
3. Branch: `main`
4. Main file: `scripts/app.py`

## 🎯 Resultado Esperado Después del Reboot

✅ **SMS:**
- Total: 315,520 registros
- Estados: 3 (Entregado al operador, Lista negra, Operador fallido)
- Gráficas: Todas visibles

✅ **Interacciones:**
- Total: 315,914 registros
- Operadores: 8 (Tigo, Avantel, Claro, Movistar, etc.)
- Códigos: 4 códigos cortos
- Gráficas: Todas visibles

✅ **WhatsApp:**
- Total: 1,903 registros (NO 1,907)
- Archivos: 2 Parquets (sin sample)
- Gráficas: Todas visibles

## 📝 Commits Aplicados
- `aecc896` - Cleanup automático de samples al iniciar
- `fb3ad85` - Force rebuild
- `e9defb2` - Exclusión reforzada de samples
- `49c857b` - Fix columns nativo de PyArrow
- `d3ec64a` - Optimización y reparación de datos

## ⏱️ Tiempo Estimado
- Reboot: 1-2 minutos
- Clear cache: 30 segundos
- Redeploy: 3-5 minutos

---
**Fecha:** 20 de enero de 2026  
**Status:** ✅ Código correcto en repo, esperando reboot en servidor
