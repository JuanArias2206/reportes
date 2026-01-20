import pandas as pd
from scripts.config import SMS_FILE, CSV_ENCODING, DELIMITERS
import time

print("⏱️ Testing procesamiento por chunks...")
print()

start = time.time()
state_counts = {}

for i, chunk in enumerate(pd.read_csv(
    SMS_FILE,
    encoding=CSV_ENCODING["sms"],
    delimiter=DELIMITERS["sms"],
    usecols=["Estado del envio"],
    chunksize=50000,
    dtype={"Estado del envio": "category"},
    low_memory=False
), 1):
    for state, count in chunk["Estado del envio"].value_counts().items():
        state_counts[state] = state_counts.get(state, 0) + count
    print(f"  ✓ Chunk {i}: {i*50000:,} registros procesados")

elapsed = time.time() - start

print()
print(f"✓ Tiempo total: {elapsed:.2f} segundos")
print(f"✓ Estados encontrados:")
total = sum(state_counts.values())
for state, count in sorted(state_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / total * 100)
    print(f"   {state:15s}: {count:8,d} ({pct:5.1f}%)")

print()
print(f"Total registros: {total:,}")
