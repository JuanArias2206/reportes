#!/usr/bin/env python3
"""Rebuild interacciones.parquet from git history."""

import pandas as pd
import subprocess
from pathlib import Path

# Recuperar el archivo desde git (commit d3ec64a tiene la columna Usuario correcta)
result = subprocess.run(
    ['git', 'show', 'd3ec64a:data/mensajes_texto/interacciones.parquet'],
    capture_output=True,
    check=False
)

if result.returncode == 0:
    # Escribir a archivo temporal
    temp_file = Path('temp_interacciones.parquet')
    temp_file.write_bytes(result.stdout)
    
    try:
        # Leer con pandas
        df = pd.read_parquet(temp_file)
        print(f"✅ Leído desde git: {len(df):,} registros")
        print(f"📊 Columnas: {list(df.columns)}")
        
        # Guardar con PyArrow nuevo
        output_file = Path('data/mensajes_texto/interacciones.parquet')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_file, engine='pyarrow', index=False, compression='snappy')
        
        # Verificar
        df_test = pd.read_parquet(output_file)
        print(f"✅ Archivo recreado: {len(df_test):,} registros")
        
        # Verificar filtro
        filtered = df_test[df_test['Usuario'] != 'Cuantico_tecnologia']
        print(f"🔢 Registros después de filtro Usuario: {len(filtered):,}")
        
        # Cleanup
        temp_file.unlink()
        print("✅ Proceso completado")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if temp_file.exists():
            temp_file.unlink()
else:
    print(f"❌ No se pudo recuperar desde git: {result.stderr.decode()}")
