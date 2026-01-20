#!/usr/bin/env python3
"""Test para verificar que los archivos Parquet se leen correctamente."""

import sys
from pathlib import Path

scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from config import SMS_FILE, WHATSAPP_FILES, INTERACCIONES_FILE
from data_loader import _read_file

print("=" * 70)
print("🧪 TEST: Lectura de archivos Parquet")
print("=" * 70)

# Test SMS
print(f"\n📱 SMS_FILE: {SMS_FILE.name}")
print(f"   Tipo: {SMS_FILE.suffix}")
try:
    df = _read_file(SMS_FILE, nrows=10)
    print(f"   ✅ Lectura exitosa: {len(df)} filas (muestra)")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test WhatsApp
print(f"\n💬 WhatsApp Files: {len(WHATSAPP_FILES)} archivo(s)")
for wa_file in WHATSAPP_FILES:
    print(f"\n   📄 {wa_file.name}")
    print(f"      Tipo: {wa_file.suffix}")
    try:
        df = _read_file(wa_file)
        print(f"      ✅ Lectura exitosa: {len(df)} filas")
    except Exception as e:
        print(f"      ❌ Error: {e}")

# Test Interacciones
print(f"\n💌 INTERACCIONES_FILE: {INTERACCIONES_FILE.name}")
print(f"   Tipo: {INTERACCIONES_FILE.suffix}")
try:
    df = _read_file(INTERACCIONES_FILE, nrows=10)
    print(f"   ✅ Lectura exitosa: {len(df)} filas (muestra)")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ Test completado")
print("=" * 70)
