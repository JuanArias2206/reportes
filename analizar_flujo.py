import pandas as pd
import glob

# Cargar archivos
files = sorted([f for f in glob.glob('data/mensajes_whatsapp/*.csv') if 'sample' not in f])
dfs = [pd.read_csv(f, encoding='utf-8') for f in files]
df = pd.concat(dfs, ignore_index=True)

print("📊 ANÁLISIS DETALLADO DEL ESTADO")
print("="*70)

# Verificar la lógica
delivered = df[df['Status'] == 'Delivered']
read = df[df['Status'] == 'Read']
failed = df[df['Status'] == 'Failed']
processing = df[df['Status'] == 'Processing']

print(f"\n✅ DELIVERED (No Leído): {len(delivered)}")
print(f"   Respondido (yes): {len(delivered[delivered['Reply Status']=='yes'])}")
print(f"   No respondido (no): {len(delivered[delivered['Reply Status']=='no'])}")

print(f"\n📖 READ (Leído): {len(read)}")
print(f"   Respondido (yes): {len(read[read['Reply Status']=='yes'])}")
print(f"   No respondido (no): {len(read[read['Reply Status']=='no'])}")

print(f"\n❌ FAILED (Fallido): {len(failed)}")
print(f"   Respondido: {len(failed[failed['Reply Status']=='yes'])}")
print(f"   No respondido: {len(failed[failed['Reply Status']=='no'])}")

print(f"\n⏳ PROCESSING (Procesando): {len(processing)}")
print(f"   Respondido: {len(processing[processing['Reply Status']=='yes'])}")
print(f"   No respondido: {len(processing[processing['Reply Status']=='no'])}")

print("\n" + "="*70)
print("🔄 FLUJO CORRECTO PARA SANKEY (3 NIVELES):")
print(f"Total Enviados: {len(df)}")
print(f"  ├─ Entregados: {len(delivered) + len(read)} (subdividido en)")
print(f"  │  ├─ No Leído: {len(delivered)}")
print(f"  │  │  ├─ Respondido: {len(delivered[delivered['Reply Status']=='yes'])}")
print(f"  │  │  └─ No Respondido: {len(delivered[delivered['Reply Status']=='no'])}")
print(f"  │  └─ Leído: {len(read)}")
print(f"  │     ├─ Respondido: {len(read[read['Reply Status']=='yes'])}")
print(f"  │     └─ No Respondido: {len(read[read['Reply Status']=='no'])}")
print(f"  ├─ Fallidos: {len(failed)}")
print(f"  │  └─ No Respondido: {len(failed[failed['Reply Status']=='no'])}")
print(f"  └─ Procesando: {len(processing)}")
print(f"     └─ No Respondido: {len(processing[processing['Reply Status']=='no'])}")
