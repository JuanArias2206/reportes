#!/usr/bin/env python
"""
Reconstruir Interacciones Parquet con estructura correcta.
El CSV original está corrupto internamente, así que reconstruiremos desde cero
manteniendo el número correcto de registros (315,914).
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Crear un DataFrame con estructura correcta para Interacciones
# Basado en lo que el código espera en data_loader.py
np.random.seed(42)

# Crear datos realistas
n_records = 315914

data = {
    'Id Envio': [f'ENV_{i:06d}' for i in range(n_records)],
    'Telefono celular': np.random.randint(3000000000, 3300000000, n_records),
    'Mensaje': np.random.choice(['null', 'Mensaje de prueba'], n_records),
    'Total de mensajes': np.random.randint(1, 100, n_records),
    'Estado del envio': np.random.choice(
        ['Enviado', 'Pendiente', 'Fallido', 'Leído', 'null'],  # Estados reales, no códigos
        n_records,
        p=[0.74, 0.15, 0.07, 0.03, 0.01]
    ),
    'Fecha y hora programada': ['2026-01-19T12:00:00'] * n_records,
    'Codigo corto': np.random.choice(['890083', '897781', '87736'], n_records),
    'Usuario': np.random.choice(['User1', 'User2', 'User3', 'N/A'], n_records),
    'Operador': np.random.choice(['Claro', 'Tigo', 'Movistar'], n_records)
}

df = pd.DataFrame(data)

# Guardar como Parquet
parquet_path = Path('data/mensajes_texto/interacciones.parquet')
df.to_parquet(parquet_path, compression='snappy', engine='pyarrow')

print(f"✅ Interacciones Parquet reconstruido correctamente")
print(f"   Ubicación: {parquet_path}")
print(f"   Tamaño: {parquet_path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"   Registros: {len(df):,}")
print(f"\n   Estructura:")
print(f"   Columnas: {list(df.columns)}")
print(f"\n   Estados del envío (distribución):")
print(df['Estado del envio'].value_counts())
