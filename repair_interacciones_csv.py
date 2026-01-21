#!/usr/bin/env python
"""
Último intento: Leer el CSV manualmente y mapear las columnas correctamente.
Los datos están en posiciones equivocadas, así que necesitamos identificar
y remapear manualmente.

Estructura observada:
  0: "0" (índice o campo oculto)
  1: "3235805406" (Telefono celular) ✓
  2: "Kjvdol..." (Mensaje) ✓
  3: "1" (Total de mensajes - número de mensajes) ✓
  4: "null" (Estado del envio?) ✓
  5: "2026-01-19T15:50:20" (Fecha y hora programada) ✓
  6: "890083" (Codigo corto - número)  ✓
  7: "N/A" (Usuario) ✓
  8: "Claro" (Operador) ✓
"""

import pandas as pd
from pathlib import Path
import csv

csv_path = Path('data/mensajes_texto/interacciones.csv')

# Lee el CSV de forma manual para entender la estructura
print("🔍 Leyendo CSV manualmente...")
rows_data = []
with open(csv_path, 'r', encoding='LATIN1') as f:
    reader = csv.reader(f, delimiter=';')
    for i, row in enumerate(reader):
        if i == 0:  # Header
            print(f"Encabezado ({len(row)} campos):")
            for j, field in enumerate(row):
                print(f"  {j}: {repr(field)}")
        elif i < 5:  # First 5 data rows
            print(f"\nFila {i} ({len(row)} campos):")
            for j, field in enumerate(row):
                val = field.strip('"') if field.startswith('"') else field
                print(f"  {j}: {repr(val[:50])}")
        else:
            break

print("\n" + "="*80)
print("El CSV tiene columnas en orden diferente al encabezado.")
print("Los datos están ligeramente desfasados.")
print("="*80)

# Ahora lee TODO el CSV y remapea
print("\n📖 Leyendo todo el CSV...")
all_rows = []
with open(csv_path, 'r', encoding='LATIN1') as f:
    reader = csv.reader(f, delimiter=';')
    header = next(reader)  # Salta encabezado
    for row_idx, row in enumerate(reader):
        if len(row) >= 9:  # Solo si tiene suficientes campos
            # Mapeo basado en lo observado
            all_rows.append({
                'Id Envio': row[0].strip('"') if len(row) > 0 else '',
                'Telefono celular': row[1].strip('"') if len(row) > 1 else '',
                'Mensaje': row[2].strip('"') if len(row) > 2 else '',
                'Total de mensajes': row[3].strip('"') if len(row) > 3 else '',
                'Estado del envio': row[4].strip('"') if len(row) > 4 else '',
                'Fecha y hora programada': row[5].strip('"') if len(row) > 5 else '',
                'Codigo corto': row[6].strip('"') if len(row) > 6 else '',
                'Usuario': row[7].strip('"') if len(row) > 7 else '',
                'Operador': row[8].strip('"') if len(row) > 8 else '',
            })

print(f"✅ Leídos {len(all_rows):,} registros")

# Crea DataFrame
df = pd.DataFrame(all_rows)

print(f"\n📊 Estructura del DataFrame:")
print(f"   Forma: {df.shape}")
print(f"   Columnas: {list(df.columns)}")

print(f"\n📋 Primeras 5 filas:")
print(df.head())

print(f"\n🔍 Estados del envío (primeros 10):")
print(df['Estado del envio'].value_counts().head(10))

# Guarda como CSV limpio
print(f"\n💾 Guardando CSV limpio...")
df.to_csv(csv_path, index=False, encoding='LATIN1', sep=';')
print(f"✅ CSV guardado")

# Guarda como Parquet
parquet_path = Path('data/mensajes_texto/interacciones.parquet')
df.to_parquet(parquet_path, compression='snappy', engine='pyarrow')
print(f"✅ Parquet creado: {parquet_path.stat().st_size / 1024 / 1024:.2f} MB")

print(f"\n✔️ COMPLETADO")
