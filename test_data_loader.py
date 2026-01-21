#!/usr/bin/env python
"""Test para verificar que data_loader funciona correctamente después de los arreglos."""

import sys
sys.path.insert(0, '/Users/mac/Documents/trabajo/cuantico/reportes/scripts')

import pandas as pd
from pathlib import Path

# Test 1: Verificar que los archivos Parquet existen y tienen estructura correcta
print("="*80)
print("TEST 1: Verificar archivos Parquet")
print("="*80)

sms_parquet = Path('data/mensajes_texto/mensajes_texto.parquet')
inter_parquet = Path('data/mensajes_texto/interacciones.parquet')

print(f"\n✓ SMS Parquet:")
df_sms = pd.read_parquet(sms_parquet)
print(f"  Registros: {len(df_sms):,}")
print(f"  Columnas: {len(df_sms.columns)}")
print(f"  'Id Envio' en columnas: {'Id Envio' in df_sms.columns}")

print(f"\n✓ Interacciones Parquet:")
df_inter = pd.read_parquet(inter_parquet)
print(f"  Registros: {len(df_inter):,}")
print(f"  Columnas: {len(df_inter.columns)}")
print(f"  'Estado del envio' en columnas: {'Estado del envio' in df_inter.columns}")

# Test 2: Verificar que data_loader puede leer los datos
print("\n" + "="*80)
print("TEST 2: Importar data_loader")
print("="*80)

try:
    from data_loader import (
        count_total_sms_records,
        count_total_interacciones_records,
        get_interacciones_states_summary,
        get_interacciones_by_operator,
        load_sms_data,
        load_whatsapp_data,
    )
    print("✅ Módulos importados correctamente")
except Exception as e:
    print(f"❌ Error importando: {e}")
    sys.exit(1)

# Test 3: Verificar funciones de conteo
print("\n" + "="*80)
print("TEST 3: Funciones de conteo")
print("="*80)

try:
    sms_count = count_total_sms_records()
    print(f"✅ SMS count: {sms_count:,}")
    if sms_count == 315520:
        print("   ✓ Cuenta correcta!")
    else:
        print(f"   ⚠️  Esperaba 315,520, obtuvo {sms_count:,}")
except Exception as e:
    print(f"❌ Error en count_total_sms_records: {e}")

try:
    inter_count = count_total_interacciones_records()
    print(f"✅ Interacciones count: {inter_count:,}")
    if inter_count == 315914:
        print("   ✓ Cuenta correcta!")
    else:
        print(f"   ⚠️  Esperaba 315,914, obtuvo {inter_count:,}")
except Exception as e:
    print(f"❌ Error en count_total_interacciones_records: {e}")

# Test 4: Verificar get_interacciones_states_summary
print("\n" + "="*80)
print("TEST 4: get_interacciones_states_summary()")
print("="*80)

try:
    states = get_interacciones_states_summary()
    print(f"✅ Estados obtenidos: {len(states)} tipo(s)")
    for state, count in list(states.items())[:5]:
        print(f"   {state}: {count:,}")
    if len(states) > 0:
        print("   ✓ Estados encontrados!")
    else:
        print("   ⚠️  No se encontraron estados")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Verificar get_interacciones_by_operator
print("\n" + "="*80)
print("TEST 5: get_interacciones_by_operator()")
print("="*80)

try:
    operators = get_interacciones_by_operator()
    print(f"✅ Operadores obtenidos: {len(operators)} operadores")
    for op, count in list(operators.items())[:5]:
        print(f"   {op}: {count:,}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Verificar load_sms_data
print("\n" + "="*80)
print("TEST 6: load_sms_data()")
print("="*80)

try:
    sms_df = load_sms_data(sample=True, sample_size=1000)
    print(f"✅ SMS data cargados: {len(sms_df):,} registros")
    print(f"   Columnas: {len(sms_df.columns)}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Verificar load_whatsapp_data
print("\n" + "="*80)
print("TEST 7: load_whatsapp_data()")
print("="*80)

try:
    wa_df = load_whatsapp_data()
    print(f"✅ WhatsApp data cargados: {len(wa_df):,} registros")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ TODOS LOS TESTS COMPLETADOS")
print("="*80)
