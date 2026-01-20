#!/usr/bin/env python3
"""
Script para convertir archivos CSV grandes a formato Parquet.
Parquet es mucho más eficiente en espacio y velocidad de lectura.
"""

import pandas as pd
from pathlib import Path
import os

def convert_csv_to_parquet(csv_path: Path, parquet_path: Path = None) -> dict:
    """Convierte un CSV a Parquet y retorna estadísticas."""
    if parquet_path is None:
        parquet_path = csv_path.with_suffix('.parquet')
    
    print(f"\n🔄 Convirtiendo: {csv_path.name}")
    
    # Leer CSV
    try:
        # Intentar varios encodings
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
            try:
                df = pd.read_csv(csv_path, encoding=encoding, on_bad_lines='skip')
                print(f"  ✓ CSV leído: {len(df):,} filas, {len(df.columns)} columnas (encoding: {encoding})")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise Exception("No se pudo leer con ningún encoding")
    except Exception as e:
        print(f"  ✗ Error leyendo CSV: {e}")
        return None
    
    # Guardar como Parquet con compresión
    try:
        df.to_parquet(parquet_path, engine='pyarrow', compression='snappy', index=False)
        print(f"  ✓ Parquet guardado: {parquet_path.name}")
    except Exception as e:
        print(f"  ✗ Error guardando Parquet: {e}")
        return None
    
    # Comparar tamaños
    csv_size = os.path.getsize(csv_path)
    parquet_size = os.path.getsize(parquet_path)
    reduction = ((csv_size - parquet_size) / csv_size) * 100
    
    stats = {
        'csv_path': csv_path,
        'parquet_path': parquet_path,
        'csv_size_mb': csv_size / (1024 * 1024),
        'parquet_size_mb': parquet_size / (1024 * 1024),
        'reduction_pct': reduction,
        'rows': len(df),
        'columns': len(df.columns)
    }
    
    print(f"  📊 Tamaño CSV: {stats['csv_size_mb']:.2f} MB")
    print(f"  📊 Tamaño Parquet: {stats['parquet_size_mb']:.2f} MB")
    print(f"  ✅ Reducción: {reduction:.1f}%")
    
    return stats

def main():
    """Convierte todos los archivos CSV grandes a Parquet."""
    print("=" * 70)
    print("🔄 CONVERSIÓN DE CSV A PARQUET")
    print("=" * 70)
    
    base_dir = Path(__file__).parent
    
    # Directorios a procesar
    directories = [
        base_dir / "data" / "mensajes_texto",
        base_dir / "data" / "mensajes_whatsapp",
    ]
    
    all_stats = []
    
    for directory in directories:
        if not directory.exists():
            print(f"\n⚠️  Directorio no encontrado: {directory}")
            continue
        
        print(f"\n📂 Procesando: {directory.name}/")
        
        # Encontrar todos los CSV (excluyendo samples)
        csv_files = [f for f in directory.glob("*.csv") if not f.name.endswith("_sample.csv")]
        
        if not csv_files:
            print(f"  ℹ️  No se encontraron archivos CSV grandes")
            continue
        
        print(f"  📄 Archivos encontrados: {len(csv_files)}")
        
        for csv_file in csv_files:
            stats = convert_csv_to_parquet(csv_file)
            if stats:
                all_stats.append(stats)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE CONVERSIÓN")
    print("=" * 70)
    
    if all_stats:
        total_csv_size = sum(s['csv_size_mb'] for s in all_stats)
        total_parquet_size = sum(s['parquet_size_mb'] for s in all_stats)
        total_reduction = ((total_csv_size - total_parquet_size) / total_csv_size) * 100
        
        print(f"\n✅ Archivos convertidos: {len(all_stats)}")
        print(f"📊 Tamaño total CSV: {total_csv_size:.2f} MB")
        print(f"📊 Tamaño total Parquet: {total_parquet_size:.2f} MB")
        print(f"💾 Espacio ahorrado: {total_csv_size - total_parquet_size:.2f} MB")
        print(f"✅ Reducción total: {total_reduction:.1f}%")
        
        print("\n📋 Detalle por archivo:")
        for stats in all_stats:
            print(f"  • {stats['parquet_path'].name}: {stats['parquet_size_mb']:.2f} MB ({stats['rows']:,} filas)")
        
        print("\n" + "=" * 70)
        print("✅ CONVERSIÓN COMPLETADA")
        print("=" * 70)
        print("\nPróximos pasos:")
        print("1. Verificar que los archivos .parquet funcionan correctamente")
        print("2. Actualizar .gitignore para incluir .parquet")
        print("3. Commit y push de los archivos .parquet a Git")
    else:
        print("\n⚠️  No se convirtieron archivos")

if __name__ == "__main__":
    main()
