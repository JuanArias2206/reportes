#!/usr/bin/env python3
"""
Test para verificar qué valores retorna get_whatsapp_flow_data()
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
os.chdir(Path(__file__).parent)
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# Mock streamlit
import streamlit as st
cache_calls = {}
def mock_cache_data(func):
    def wrapper(*args, **kwargs):
        key = func.__name__
        if key not in cache_calls:
            cache_calls[key] = func(*args, **kwargs)
        return cache_calls[key]
    return wrapper
st.cache_data = mock_cache_data

# Ahora importar 
import pandas as pd
from config import WHATSAPP_FILES, CSV_ENCODING, DELIMITERS
from data_loader import load_whatsapp_data, get_whatsapp_flow_data

print("=" * 90)
print("TEST: ¿Qué datos retorna get_whatsapp_flow_data() para el Sankey?")
print("=" * 90)

# Primero cargar manualmente
print("\n[1] Cargando datos manualmente...")
all_dfs = []
total_manual = 0
for wa_file in WHATSAPP_FILES:
    df = pd.read_csv(wa_file, encoding=CSV_ENCODING["whatsapp"], delimiter=DELIMITERS["whatsapp"])
    all_dfs.append(df)
    total_manual += len(df)
    print(f"   ✓ {wa_file.name}: {len(df)} registros")

combined_manual = pd.concat(all_dfs, ignore_index=True)
print(f"   ✓ TOTAL: {len(combined_manual)} registros")

# Contar estados manualmente
print("\n[2] Conteo de estados (manual):")
for state, count in combined_manual['Status'].value_counts().items():
    print(f"   {state}: {count}")

# Ahora usar load_whatsapp_data()
print("\n[3] Usando load_whatsapp_data()...")
df_loaded = load_whatsapp_data()
print(f"   ✓ Registros: {len(df_loaded)}")
print(f"   ✓ Coincide con manual: {len(df_loaded) == len(combined_manual)}")

# Finalmente, get_whatsapp_flow_data()
print("\n[4] Usando get_whatsapp_flow_data() (para Sankey)...")
source, target, value = get_whatsapp_flow_data()

print(f"   Source: {source}")
print(f"   Target: {target}")
print(f"   Value: {value}")
print(f"\n   Datos para Sankey:")
for s, t, v in zip(source, target, value):
    print(f"      {s} → {t}: {v}")

total_sankey = sum(value) if value else 0
print(f"\n   ✓ TOTAL en Sankey: {total_sankey}")
print(f"   ✓ Esperado (1,903): {total_sankey == 1903}")

if total_sankey != 1903:
    print(f"\n   ⚠️ DISCREPANCIA: Sankey muestra {total_sankey}, pero hay {len(combined_manual)} registros totales")
    print(f"      Diferencia: {len(combined_manual) - total_sankey} registros FALTANTES")

print("\n" + "=" * 90)
