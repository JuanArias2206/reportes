#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "scripts")
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

import streamlit as st
cache_calls = {}
def mock_cache(func):
    def wrapper(*args, **kwargs):
        key = func.__name__
        if key not in cache_calls:
            cache_calls[key] = func(*args, **kwargs)
        return cache_calls[key]
    return wrapper
st.cache_data = mock_cache

from data_loader import load_whatsapp_data, get_whatsapp_flow_data
from config import WHATSAPP_FILES

print("\nDEBUG: Verificando qué ve get_whatsapp_flow_data()")
print("=" * 80)

print(f"\nWHATSAPP_FILES: {len(WHATSAPP_FILES)}")
for f in WHATSAPP_FILES:
    print(f"  {f.name}")

print(f"\nCargando...")
df = load_whatsapp_data()
print(f"Total: {len(df)}")

print(f"\nSankey:")
source, target, value = get_whatsapp_flow_data()
total = sum(value)
print(f"  Total: {total}")
for s,t,v in zip(source, target, value):
    print(f"  {t}: {v}")
