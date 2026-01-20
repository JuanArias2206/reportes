#!/usr/bin/env python3
"""
Script de análisis exploratorio de datos (EDA).
Permite inspeccionar rápidamente la estructura y características de los datasets.
Uso: python3 eda.py
"""

import pandas as pd
import sys
from pathlib import Path

# Agregar scripts al path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from config import SMS_FILE, WHATSAPP_FILES, CSV_ENCODING, DELIMITERS
from data_loader import get_sms_stats, get_whatsapp_stats


def print_header(title):
    """Imprime un encabezado formateado."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def analyze_sms():
    """Analiza el archivo SMS."""
    print_header("ANÁLISIS SMS")
    
    try:
        # Obtener estadísticas
        stats = get_sms_stats()
        
        print(f"\n📊 Estadísticas Generales:")
        print(f"  Total de registros: {stats['total']:,}")
        print(f"\n📈 Distribución de Estados:")
        
        for state, count in sorted(stats['states'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            bar = "█" * int(percentage / 2)
            print(f"  {state:20} {count:>8,} ({percentage:>6.2f}%) {bar}")
        
        # Obtener información del archivo
        print(f"\n📄 Información del Archivo:")
        file_size_mb = SMS_FILE.stat().st_size / (1024 * 1024)
        print(f"  Ruta: {SMS_FILE}")
        print(f"  Tamaño: {file_size_mb:.2f} MB")
        print(f"  Encoding: {CSV_ENCODING['sms']}")
        print(f"  Delimitador: '{DELIMITERS['sms']}'")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def analyze_whatsapp():
    """Analiza los archivos WhatsApp."""
    print_header("ANÁLISIS WHATSAPP")
    
    try:
        stats = get_whatsapp_stats()
        
        print(f"\n📊 Estadísticas Generales:")
        print(f"  Total de registros: {stats['total']:,}")
        print(f"\n📈 Distribución de Estados (Agregado):")
        
        for state, count in sorted(stats['states'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            bar = "█" * int(percentage / 2)
            print(f"  {state:20} {count:>8,} ({percentage:>6.2f}%) {bar}")
        
        # Por archivo
        print(f"\n📂 Detalles por Archivo:")
        for file_name, file_data in stats['by_file'].items():
            print(f"\n  Archivo: {file_name}")
            print(f"    Registros: {file_data['count']:,}")
            print(f"    Estados:")
            for state, count in sorted(file_data['states'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / file_data['count'] * 100)
                print(f"      {state:20} {count:>8,} ({percentage:>6.2f}%)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def analyze_files_info():
    """Muestra información sobre los archivos."""
    print_header("INFORMACIÓN DE ARCHIVOS")
    
    # SMS
    if SMS_FILE.exists():
        size_mb = SMS_FILE.stat().st_size / (1024 * 1024)
        print(f"\n📱 SMS (Mensajes de Texto)")
        print(f"  Archivo: {SMS_FILE.name}")
        print(f"  Tamaño: {size_mb:.2f} MB")
        print(f"  Existe: ✓")
    else:
        print(f"\n📱 SMS - Archivo no encontrado")
    
    # WhatsApp
    print(f"\n💬 WhatsApp")
    for file in WHATSAPP_FILES:
        if file.exists():
            size_kb = file.stat().st_size / 1024
            print(f"  ✓ {file.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ✗ {file.name} (no encontrado)")


def compare_datasets():
    """Compara los datasets."""
    print_header("COMPARATIVA SMS vs WHATSAPP")
    
    try:
        sms_stats = get_sms_stats()
        whatsapp_stats = get_whatsapp_stats()
        
        total = sms_stats['total'] + whatsapp_stats['total']
        
        sms_pct = (sms_stats['total'] / total * 100) if total > 0 else 0
        wpp_pct = (whatsapp_stats['total'] / total * 100) if total > 0 else 0
        
        print(f"\n📊 Distribución General:")
        print(f"  SMS:      {sms_stats['total']:>10,} ({sms_pct:>6.2f}%)")
        print(f"  WhatsApp: {whatsapp_stats['total']:>10,} ({wpp_pct:>6.2f}%)")
        print(f"  Total:    {total:>10,} (100.00%)")
        
        print(f"\n📈 Promedio de Estados por Plataforma:")
        print(f"  SMS estados: {len(sms_stats['states'])}")
        print(f"  WhatsApp estados: {len(whatsapp_stats['states'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Ejecuta el análisis exploratorio."""
    print("\n" + "="*60)
    print("  ANÁLISIS EXPLORATORIO DE DATOS (EDA)")
    print("  Estados de Interacción - Reportes")
    print("="*60)
    
    analyze_files_info()
    analyze_sms()
    analyze_whatsapp()
    compare_datasets()
    
    print("\n" + "="*60)
    print("  ✅ Análisis completado")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
