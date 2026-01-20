#!/usr/bin/env python3
"""
Script para reconvertir archivos CSV a Parquet CON los delimitadores correctos.
Versión corregida que usa el mapping de delimitadores por tipo de archivo.
"""

import pandas as pd
from pathlib import Path
import os

# Configuración de delimitadores por tipo
DELIMITERS = {
    "sms": ";",
    "whatsapp": ",",
    "interacciones": ";"
}

ENCODINGS = {
    "sms": "LATIN1",
    "whatsapp": "utf-8",
    "interacciones": "LATIN1"
}

def convert_csv_to_parquet_correct(csv_path: Path, parquet_path: Path = None, delimiter=None, encoding=None) -> dict:
    """Convierte un CSV a Parquet CON delimitador y encoding correctos."""
    if parquet_path is None:
        parquet_path = csv_path.with_suffix('.parquet')
    
    print(f"\n🔄 Convirtiendo: {csv_path.name}")
    print(f"   Delimitador: '{delimiter}'")
    print(f"   Encoding: {encoding}")
    
    # Leer CSV con delimitador y encoding correctos
    try:
        df = pd.read_csv(csv_path, encoding=encoding, delimiter=delimiter, on_bad_lines='skip', low_memory=False)
        print(f"  ✓ CSV leído: {len(df):,} filas, {len(df.columns)} columnas")
    except Exception as e:
        print(f"  ✗ Error leyendo CSV: {e}")
        return None
    
    # Convertir todas las columnas a string para evitar problemas de tipo
    df = df.astype(str)
    
    # Guardar como Parquet
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
    """Reconvierte todos los archivos con delimitadores correctos."""
    print("=" * 70)
    print("🔄 RECONVERSIÓN DE CSV A PARQUET (CON DELIMITADORES CORRECTOS)")
    print("=" * 70)
    
    base_dir = Path(__file__).parent
    
    # Archivos a reconvertir
    files_to_convert = [
        {
            'path': base_dir / "data" / "mensajes_texto" / "mensajes_texto.csv",
            'type': 'sms'
        },
        {
            'path': base_dir / "data" / "mensajes_texto" / "interacciones.csv",
            'type': 'interacciones'
        },
    ]
    
    all_stats = []
    
    for file_info in files_to_convert:
        csv_file = file_info['path']
        file_type = file_info['type']
        
        if not csv_file.exists():
            print(f"\n⚠️  Archivo no encontrado: {csv_file}")
            continue
        
        delimiter = DELIMITERS.get(file_type, ',')
        encoding = ENCODINGS.get(file_type, 'utf-8')
        
        stats = convert_csv_to_parquet_correct(
            csv_file, 
            delimiter=delimiter, 
            encoding=encoding
        )
        
        if stats:
            all_stats.append(stats)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE RECONVERSIÓN")
    print("=" * 70)
    
    if all_stats:
        total_csv_size = sum(s['csv_size_mb'] for s in all_stats)
        total_parquet_size = sum(s['parquet_size_mb'] for s in all_stats)
        total_reduction = ((total_csv_size - total_parquet_size) / total_csv_size) * 100
        
        print(f"\n✅ Archivos reconvertidos: {len(all_stats)}")
        print(f"📊 Tamaño total CSV: {total_csv_size:.2f} MB")
        print(f"📊 Tamaño total Parquet: {total_parquet_size:.2f} MB")
        print(f"💾 Espacio ahorrado: {total_csv_size - total_parquet_size:.2f} MB")
        print(f"✅ Reducción total: {total_reduction:.1f}%")
        
        print("\n📋 Detalle por archivo:")
        for stats in all_stats:
            print(f"  • {stats['parquet_path'].name}: {stats['rows']:,} filas, {stats['parquet_size_mb']:.2f} MB")
        
        print("\n" + "=" * 70)
        print("✅ RECONVERSIÓN COMPLETADA")
        print("=" * 70)
    else:
        print("\n⚠️  No se reconvirtieron archivos")

if __name__ == "__main__":
    main()
