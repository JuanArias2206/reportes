#!/usr/bin/env python3
"""
Test para verificar que create_sankey_diagram() no divide valores por 2
"""

import sys
from pathlib import Path

# Agregar scripts al path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

import plotly.graph_objects as go
from visualizations import create_sankey_diagram

# Simular los datos del Sankey de WhatsApp
source = ["Enviados", "Enviados", "Enviados", "Enviados"]
target = ["Delivered", "Failed", "Read", "Processing"]
value = [790, 595, 465, 53]

print("=" * 70)
print("Test: create_sankey_diagram() - Verificación de valores")
print("=" * 70)
print(f"\nDatos de entrada:")
print(f"  source: {source}")
print(f"  target: {target}")
print(f"  value: {value}")
print(f"  TOTAL: {sum(value)}")

# Crear el Sankey
fig = create_sankey_diagram(source, target, value, "Flujo WhatsApp (TOTAL)")

# Verificar los valores en los labels
print(f"\nLabels generados:")
sankey_data = fig.data[0]
for label in sankey_data.node.label:
    print(f"  {label}")

# Extraer números de los labels
import re
labels_with_values = {}
for label in sankey_data.node.label:
    match = re.search(r'\(([\d,]+)\)', label)
    if match:
        node_name = label.split('\n')[0]
        node_value = int(match.group(1).replace(',', ''))
        labels_with_values[node_name] = node_value
        print(f"\n  {node_name}: {node_value}")

# Verificación
print(f"\n" + "=" * 70)
if labels_with_values.get("Enviados") == 1903:
    print("✅ ¡ÉXITO! Enviados muestra 1903 (correcto)")
else:
    print(f"❌ ERROR: Enviados muestra {labels_with_values.get('Enviados')} (debería ser 1903)")

if (labels_with_values.get("Delivered") == 790 and 
    labels_with_values.get("Failed") == 595 and 
    labels_with_values.get("Read") == 465 and 
    labels_with_values.get("Processing") == 53):
    print("✅ ¡ÉXITO! Todos los destinos muestran valores correctos")
else:
    print("❌ ERROR: Los destinos tienen valores incorrectos")
    print(f"   Delivered: {labels_with_values.get('Delivered')} (esperado: 790)")
    print(f"   Failed: {labels_with_values.get('Failed')} (esperado: 595)")
    print(f"   Read: {labels_with_values.get('Read')} (esperado: 465)")
    print(f"   Processing: {labels_with_values.get('Processing')} (esperado: 53)")

print("=" * 70)
