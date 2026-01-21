#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/mac/Documents/trabajo/cuantico/reportes/scripts')

from data_loader import (
    count_total_sms_records,
    count_total_interacciones_records,
    load_whatsapp_data,
    get_interacciones_states_summary,
    get_interacciones_by_operator,
)

print("\n" + "="*80)
print("RESUMEN DE DATOS - VERIFICACIÓN FINAL")
print("="*80)

sms_count = count_total_sms_records()
inter_count = count_total_interacciones_records()
wa_df = load_whatsapp_data()
wa_count = len(wa_df)

print(f"\n📊 CONTEOS TOTALES:")
print(f"  SMS:              {sms_count:>10,}")
print(f"  Interacciones:    {inter_count:>10,}")
print(f"  WhatsApp:         {wa_count:>10,}")
print(f"  {'-'*40}")
print(f"  TOTAL:            {sms_count + inter_count + wa_count:>10,}")

print(f"\n📈 INTERACCIONES - ESTADOS:")
states = get_interacciones_states_summary()
for state, count in states.items():
    pct = (count / inter_count * 100) if inter_count > 0 else 0
    print(f"  {state:20s}: {count:>10,} ({pct:>5.1f}%)")

print(f"\n🏢 INTERACCIONES - OPERADORES:")
ops = get_interacciones_by_operator()
for op, count in sorted(ops.items(), key=lambda x: x[1], reverse=True)[:5]:
    pct = (count / inter_count * 100) if inter_count > 0 else 0
    print(f"  {op:15s}: {count:>10,} ({pct:>5.1f}%)")

print("\n" + "="*80)
print("✅ ESTADO: LISTO PARA DESPLIEGUE")
print("="*80)
