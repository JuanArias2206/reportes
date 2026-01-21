#!/usr/bin/env python3
"""Test rápido de velocidad de las funciones optimizadas."""

import sys
import time
sys.path.insert(0, '/Users/mac/Documents/trabajo/cuantico/reportes/scripts')

print("="*80)
print("TEST DE VELOCIDAD - Funciones Optimizadas")
print("="*80)

# Test 1: count_total_sms_records
print("\n🚀 Test 1: count_total_sms_records()")
from data_loader import count_total_sms_records

start = time.time()
sms_count = count_total_sms_records()
elapsed = time.time() - start

print(f"   Resultado: {sms_count:,}")
print(f"   Tiempo: {elapsed:.4f} segundos")
if elapsed < 0.1:
    print(f"   ✅ RÁPIDO (menos de 0.1s)")
else:
    print(f"   ⚠️  LENTO (más de 0.1s)")

# Test 2: count_total_interacciones_records
print("\n🚀 Test 2: count_total_interacciones_records()")
from data_loader import count_total_interacciones_records

start = time.time()
inter_count = count_total_interacciones_records()
elapsed = time.time() - start

print(f"   Resultado: {inter_count:,}")
print(f"   Tiempo: {elapsed:.4f} segundos")
if elapsed < 0.1:
    print(f"   ✅ RÁPIDO (menos de 0.1s)")
else:
    print(f"   ⚠️  LENTO (más de 0.1s)")

# Test 3: load_whatsapp_data
print("\n🚀 Test 3: load_whatsapp_data()")
from data_loader import load_whatsapp_data

start = time.time()
wa_df = load_whatsapp_data()
elapsed = time.time() - start

print(f"   Resultado: {len(wa_df):,} registros")
print(f"   Tiempo: {elapsed:.4f} segundos")
if elapsed < 1.0:
    print(f"   ✅ RÁPIDO (menos de 1s)")
else:
    print(f"   ⚠️  LENTO (más de 1s)")

print("\n" + "="*80)
print("✅ TESTS COMPLETADOS")
print("="*80)
print(f"\n📊 RESUMEN:")
print(f"   SMS:          {sms_count:>10,}")
print(f"   Interacciones: {inter_count:>10,}")
print(f"   WhatsApp:     {len(wa_df):>10,}")
print(f"   {'-'*40}")
print(f"   TOTAL:        {sms_count + inter_count + len(wa_df):>10,}")
