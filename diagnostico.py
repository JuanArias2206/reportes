"""Script de diagnóstico para verificar estado de archivos en el servidor."""
import streamlit as st
from pathlib import Path
import pandas as pd

st.title("🔍 Diagnóstico de Archivos")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

st.header("📁 Archivos en data/mensajes_texto/")
sms_dir = DATA_DIR / "mensajes_texto"
if sms_dir.exists():
    files = list(sms_dir.glob("*"))
    for f in sorted(files):
        if f.is_file():
            size_mb = f.stat().st_size / 1024 / 1024
            st.write(f"- `{f.name}` ({size_mb:.2f} MB)")
else:
    st.error("Directory no existe")

st.header("📁 Archivos en data/mensajes_whatsapp/")
wa_dir = DATA_DIR / "mensajes_whatsapp"
if wa_dir.exists():
    files = list(wa_dir.glob("*"))
    for f in sorted(files):
        if f.is_file():
            size_mb = f.stat().st_size / 1024 / 1024
            st.write(f"- `{f.name}` ({size_mb:.2f} MB)")
else:
    st.error("Directory no existe")

st.header("🔬 Test de Lectura de Parquet")
try:
    sms_parquet = sms_dir / "mensajes_texto.parquet"
    if sms_parquet.exists():
        st.success(f"✅ SMS Parquet existe: {sms_parquet}")
        df = pd.read_parquet(sms_parquet, engine='pyarrow', columns=['Estado del envio'])
        st.write(f"Registros: {len(df):,}")
        st.write("Estados únicos:")
        st.write(df['Estado del envio'].value_counts())
    else:
        st.error("❌ SMS Parquet NO existe")
except Exception as e:
    st.error(f"Error leyendo SMS Parquet: {e}")

try:
    inter_parquet = sms_dir / "interacciones.parquet"
    if inter_parquet.exists():
        st.success(f"✅ Interacciones Parquet existe: {inter_parquet}")
        df = pd.read_parquet(inter_parquet, engine='pyarrow', columns=['Operador'])
        st.write(f"Registros: {len(df):,}")
        st.write("Operadores (top 5):")
        st.write(df['Operador'].value_counts().head())
    else:
        st.error("❌ Interacciones Parquet NO existe")
except Exception as e:
    st.error(f"Error leyendo Interacciones Parquet: {e}")
