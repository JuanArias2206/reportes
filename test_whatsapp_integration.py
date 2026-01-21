#!/usr/bin/env python3
"""
Test integral de carga de WhatsApp sin Streamlit.
Simula lo que hace la app cuando carga los datos.
"""
import sys
import os
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
os.chdir(Path(__file__).parent)

# Evitar warning de Streamlit
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

import pandas as pd
from config import WHATSAPP_FILES, CSV_ENCODING, DELIMITERS

print("=" * 90)
print("TEST INTEGRAL: CARGA DE DATOS WHATSAPP COMBINADOS")
print("=" * 90)

print(f"\n📋 WHATSAPP_FILES configurado:")
for i, f in enumerate(WHATSAPP_FILES, 1):
    print(f"   {i}. {f.name} (existe: {f.exists()})")

print(f"\n🔄 Cargando TODOS los archivos...")
all_dfs = []
total_records = 0

for wa_file in WHATSAPP_FILES:
    try:
        if not wa_file.exists():
            print(f"   ✗ {wa_file.name}: NO EXISTE")
            continue
        
        df = pd.read_csv(
            wa_file,
            encoding=CSV_ENCODING["whatsapp"],
            delimiter=DELIMITERS["whatsapp"],
        )
        all_dfs.append(df)
        total_records += len(df)
        
        print(f"   ✓ {wa_file.name}: {len(df)} registros")
        
        # Mostrar info del archivo
        if 'Status' in df.columns:
            status_counts = df['Status'].value_counts().to_dict()
            print(f"     Estados: {status_counts}")
        
    except Exception as e:
        print(f"   ✗ {wa_file.name}: ERROR - {e}")
        continue

print(f"\n📊 CONCATENANDO {len(all_dfs)} dataframes...")
if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"   ✓ Total registros combinados: {len(combined)}")
    
    # Estadísticas combinadas
    if 'Status' in combined.columns:
        print(f"\n📈 ESTADÍSTICAS COMBINADAS:")
        status_summary = combined['Status'].value_counts().to_dict()
        for status, count in sorted(status_summary.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(combined)) * 100
            print(f"   • {status}: {count:,} ({pct:.1f}%)")
    
    print(f"\n✅ ÉXITO: Se cargaron y combinaron {len(all_dfs)} archivo(s) = {len(combined):,} registros")
else:
    print("   ✗ No se cargó ningún dataframe")

print("=" * 90)
