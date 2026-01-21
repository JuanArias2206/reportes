#!/usr/bin/env python
"""Fix Interacciones CSV column corruption and convert to Parquet."""

import pandas as pd
from pathlib import Path

inter_csv = Path('data/mensajes_texto/interacciones.csv')

print("🔍 Leyendo CSV original...")
df = pd.read_csv(inter_csv, encoding='LATIN1', delimiter=';', low_memory=False)

print(f"Columnas crudas: {df.columns.tolist()}")

# Limpia los nombres de columnas (elimina saltos de línea)
df.columns = df.columns.str.replace('\n', ' ').str.strip()

print(f"✅ Columnas limpiadas: {df.columns.tolist()}")
print(f"\nForma del DataFrame: {df.shape}")
print(f"\nEstados del envío únicos:")
print(df['Estado del envio'].value_counts())

# Guarda el CSV limpio
print("\n💾 Guardando CSV limpio...")
df.to_csv(inter_csv, index=False, encoding='LATIN1', delimiter=';')
print(f"✅ CSV limpiado y guardado: {inter_csv}")

# Convierte a Parquet
print("\n📦 Convirtiendo a Parquet...")
parquet_path = Path('data/mensajes_texto/interacciones.parquet')
df.to_parquet(parquet_path, compression='snappy', engine='pyarrow')
file_size_mb = parquet_path.stat().st_size / 1024 / 1024
print(f"✅ Parquet creado: {parquet_path}")
print(f"   Tamaño: {file_size_mb:.2f} MB")

# Verifica el Parquet
print("\n✔️ Verificando Parquet...")
df_check = pd.read_parquet(parquet_path)
print(f"✅ Filas en Parquet: {df_check.shape[0]:,}")
print(f"✅ Columnas en Parquet: {df_check.shape[1]}")
print(f"\nEstados del envío en Parquet:")
print(df_check['Estado del envio'].value_counts())
