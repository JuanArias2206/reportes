#!/bin/bash

# Script para iniciar la aplicación Streamlit
# Uso: ./run.sh

set -e

cd "$(dirname "$0")"

echo "🚀 Iniciando Estados de Interacción Streamlit App..."
echo ""

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "✓ Activando entorno virtual..."
source venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -q -r requirements.txt
fi

echo "✓ Dependencias listas"
echo ""
echo "📊 Abriendo aplicación en: http://localhost:8503"
echo ""

# Iniciar Streamlit
streamlit run scripts/app.py
