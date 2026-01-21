#!/usr/bin/env python3
"""
Script para verificar que TODOS los archivos WhatsApp se cargan correctamente.
"""
import sys
from pathlib import Path

# Add scripts to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from config import WHATSAPP_FILES, WHATSAPP_DIR
import pandas as pd

print("=" * 80)
print("VERIFICACIÓN DE CARGA DE ARCHIVOS WHATSAPP")
print("=" * 80)

print(f"\n📁 Directorio: {WHATSAPP_DIR}")
print(f"📋 Archivos configurados en WHATSAPP_FILES: {len(WHATSAPP_FILES)}")

if WHATSAPP_FILES:
    print("\n📄 Archivos detectados:")
    for i, f in enumerate(WHATSAPP_FILES, 1):
        print(f"   {i}. {f.name}")
else:
    print("\n⚠️ NO se detectaron archivos WhatsApp")

# Intentar cargar cada uno
print("\n🔄 Intentando cargar cada archivo:")
total_records = 0

for wa_file in WHATSAPP_FILES:
    try:
        df = pd.read_csv(wa_file, encoding='utf-8', delimiter=',')
        print(f"   ✓ {wa_file.name}: {len(df)} registros")
        print(f"     Columnas: {list(df.columns)[:5]}... (mostrando primeras 5)")
        if 'Status' in df.columns:
            status_counts = df['Status'].value_counts().to_dict()
            print(f"     Estados: {status_counts}")
        total_records += len(df)
    except Exception as e:
        print(f"   ✗ {wa_file.name}: ERROR - {e}")

print(f"\n📊 TOTAL de registros cargados: {total_records}")
print("=" * 80)
