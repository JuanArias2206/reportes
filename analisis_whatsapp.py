import pandas as pd
import glob

files = sorted([f for f in glob.glob('data/mensajes_whatsapp/*.csv') if 'sample' not in f])

dfs = []
for f in files:
    df = pd.read_csv(f, encoding='utf-8')
    dfs.append(df)
    print(f'✅ {f.split("/")[-1]}: {len(df)} filas')

df_total = pd.concat(dfs, ignore_index=True)
print(f'\n📊 TOTAL: {len(df_total)} registros')
print(f'\n🔍 Status (Entregas):')
print(df_total['Status'].value_counts())
print(f'\n✉️ Reply Status (Respuestas):')
print(df_total['Reply Status'].value_counts())
print(f'\n📋 COMBINACIÓN Status + Reply:')
combo = pd.crosstab(df_total['Status'], df_total['Reply Status'], margins=True)
print(combo)
