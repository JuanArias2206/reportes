#!/usr/bin/env python3
"""
VERIFICACIÓN FINAL: El Sankey DEBE mostrar 1,903 registros, no 951
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
os.chdir(Path(__file__).parent)
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

import streamlit as st
cache_calls = {}
def mock_cache(func):
    def wrapper(*args, **kwargs):
        key = func.__name__
        if key not in cache_calls:
            cache_calls[key] = func(*args, **kwargs)
        return cache_calls[key]
    return wrapper
st.cache_data = mock_cache

from data_loader import get_whatsapp_statistics, get_whatsapp_flow_data

print("\n" + "=" * 90)
print("VERIFICACIÓN: Sankey vs Métricas")
print("=" * 90)

# Obtener estadísticas (lo que muestra las métricas)
stats = get_whatsapp_statistics()
total_wa = stats['total']

print(f"\n📊 MÉTRICAS (Tab 'Estados'):")
print(f"   💬 Total Mensajes: {total_wa:,}")

# Obtener flujo (lo que muestra el Sankey)
source, target, value = get_whatsapp_flow_data()
total_sankey = sum(value)

print(f"\n🔄 SANKEY (Tab 'Flujo'):")
print(f"   Datos:")
for s, t, v in zip(source, target, value):
    print(f"     {s} → {t}: {v:,}")
print(f"   TOTAL en Sankey: {total_sankey:,}")

# Comparación
print(f"\n{'=' * 90}")
print(f"VALIDACIÓN:")
print(f"{'=' * 90}")

if total_wa == total_sankey == 1903:
    print(f"✅ CORRECTO: Métricas y Sankey muestran {total_wa:,} (coinciden)")
else:
    print(f"❌ ERROR: Discrepancia detectada")
    print(f"   Métricas: {total_wa:,}")
    print(f"   Sankey:   {total_sankey:,}")
    print(f"   Diferencia: {abs(total_wa - total_sankey):,}")

print(f"\n{'=' * 90}\n")
