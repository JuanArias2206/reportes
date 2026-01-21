#!/usr/bin/env python3
"""
Test final para verificar que el Sankey mostrará 1,903 registros.
Este test simula EXACTAMENTE lo que hace app.py
"""

import sys
from pathlib import Path

# Agregar scripts al path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from config import WHATSAPP_FILES
import pandas as pd

print("=" * 70)
print("🔍 TEST FINAL: Verificación del Sankey de WhatsApp")
print("=" * 70)

# 1. Verificar que WHATSAPP_FILES tiene 2 archivos
print(f"\n1️⃣ Archivos encontrados: {len(WHATSAPP_FILES)}")
for wa_file in WHATSAPP_FILES:
    print(f"   ✓ {wa_file.name}")

# 2. Cargar cada archivo y contar registros
print(f"\n2️⃣ Cargando archivos individually...")
total_records = 0
all_statuses = {}

for wa_file in WHATSAPP_FILES:
    try:
        df = pd.read_csv(wa_file, encoding="utf-8")
        num_records = len(df)
        total_records += num_records
        print(f"   ✓ {wa_file.name}: {num_records} registros")
        
        # Mostrar conteos por estado
        if 'Status' in df.columns:
            status_counts = df['Status'].value_counts().to_dict()
            print(f"     Estados: {status_counts}")
            for status, count in status_counts.items():
                all_statuses[status] = all_statuses.get(status, 0) + count
    except Exception as e:
        print(f"   ✗ Error cargando {wa_file.name}: {e}")

print(f"\n3️⃣ TOTAL combinado: {total_records} registros")
print(f"   Estados combinados: {all_statuses}")
print(f"   Suma de estados: {sum(all_statuses.values())}")

# 3. Simular lo que hace load_whatsapp_data()
print(f"\n4️⃣ Simulando load_whatsapp_data()...")
all_dfs = []
for wa_file in WHATSAPP_FILES:
    try:
        df = pd.read_csv(wa_file, encoding="utf-8")
        all_dfs.append(df)
    except:
        pass

if all_dfs:
    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"   ✓ DataFrame combinado: {len(combined_df)} filas")
    print(f"   ✓ Columnas: {combined_df.columns.tolist()}")
    
    # 4. Simular lo que hace get_whatsapp_flow_data()
    print(f"\n5️⃣ Simulando get_whatsapp_flow_data()...")
    if 'Status' in combined_df.columns:
        sankey_data = combined_df['Status'].value_counts()
        print(f"   ✓ Status value_counts:")
        for status, count in sankey_data.items():
            print(f"     - {status}: {count}")
        print(f"   ✓ TOTAL: {sankey_data.sum()}")
        
        # Simular creación de source/target/value para Sankey
        source = []
        target = []
        value = []
        for state, count in sankey_data.items():
            source.append("Enviados")
            target.append(str(state))
            value.append(count)
        
        print(f"\n6️⃣ Datos para Sankey:")
        print(f"   source: {source}")
        print(f"   target: {target}")
        print(f"   value: {value}")
        print(f"   SUMA value: {sum(value)}")
        
        if sum(value) == 1903:
            print("\n✅ ¡ÉXITO! El Sankey mostrará 1,903 registros como se espera.")
        else:
            print(f"\n❌ ERROR: El Sankey mostrará {sum(value)} registros, se esperaban 1,903")
    else:
        print("   ✗ Columna 'Status' no encontrada")
else:
    print("   ✗ No se pudieron cargar los archivos")

print("\n" + "=" * 70)
