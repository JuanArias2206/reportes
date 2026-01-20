"""Script para eliminar archivos sample que puedan existir en el servidor."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
WHATSAPP_DIR = DATA_DIR / "mensajes_whatsapp"

# Lista de archivos sample a eliminar
sample_files = [
    WHATSAPP_DIR / "whatsapp_sample.csv",
    DATA_DIR / "mensajes_texto" / "mensajes_texto_sample.csv",
    DATA_DIR / "mensajes_texto" / "interacciones_sample.csv",
]

print("🧹 Limpiando archivos sample...")
removed = 0
for sample_file in sample_files:
    if sample_file.exists():
        try:
            os.remove(sample_file)
            print(f"✅ Eliminado: {sample_file.name}")
            removed += 1
        except Exception as e:
            print(f"❌ Error eliminando {sample_file.name}: {e}")
    else:
        print(f"⏭️  No existe: {sample_file.name}")

print(f"\n{'='*60}")
if removed > 0:
    print(f"✅ Se eliminaron {removed} archivo(s) sample")
else:
    print("✅ No había archivos sample para eliminar")
print(f"{'='*60}")
