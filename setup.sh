#!/bin/bash

# Script de inicialización del proyecto
# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   Sistema de Análisis de Mensajería${NC}"
echo -e "${BLUE}   SMS / WhatsApp / Interacciones${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Verificar Python
echo -e "${YELLOW}Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION encontrado${NC}"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
fi
echo ""

# Activar entorno virtual
echo -e "${YELLOW}Activando entorno virtual...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"
echo ""

# Instalar/Actualizar dependencias
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Verificar estructura de carpetas
echo -e "${YELLOW}Verificando estructura de datos...${NC}"
if [ ! -d "data" ]; then
    echo -e "${YELLOW}⚠️  Carpeta 'data/' no existe. Creándola...${NC}"
    mkdir -p data/mensajes_texto
    mkdir -p data/mensajes_whatsapp
    echo -e "${YELLOW}⚠️  Coloca tus archivos CSV en las carpetas correspondientes:${NC}"
    echo -e "   - data/mensajes_texto/mensajes_texto.csv"
    echo -e "   - data/mensajes_texto/interacciones.csv"
    echo -e "   - data/mensajes_whatsapp/*.csv"
else
    echo -e "${GREEN}✓ Estructura de carpetas OK${NC}"
fi
echo ""

# Verificar archivos de datos
echo -e "${YELLOW}Verificando archivos de datos...${NC}"
if [ -f "data/mensajes_texto/mensajes_texto.csv" ]; then
    SIZE=$(du -h "data/mensajes_texto/mensajes_texto.csv" | cut -f1)
    echo -e "${GREEN}✓ mensajes_texto.csv encontrado ($SIZE)${NC}"
else
    echo -e "${RED}❌ mensajes_texto.csv NO encontrado${NC}"
fi

if [ -f "data/mensajes_texto/interacciones.csv" ]; then
    SIZE=$(du -h "data/mensajes_texto/interacciones.csv" | cut -f1)
    echo -e "${GREEN}✓ interacciones.csv encontrado ($SIZE)${NC}"
else
    echo -e "${RED}❌ interacciones.csv NO encontrado${NC}"
fi

WA_FILES=$(ls data/mensajes_whatsapp/*.csv 2>/dev/null | wc -l)
if [ $WA_FILES -gt 0 ]; then
    echo -e "${GREEN}✓ $WA_FILES archivo(s) de WhatsApp encontrado(s)${NC}"
else
    echo -e "${RED}❌ No hay archivos de WhatsApp${NC}"
fi
echo ""

# Ejecutar pruebas rápidas
echo -e "${YELLOW}Ejecutando pruebas rápidas...${NC}"
if python3 -c "import streamlit; import pandas; import plotly; print('OK')" &> /dev/null; then
    echo -e "${GREEN}✓ Dependencias funcionando correctamente${NC}"
else
    echo -e "${RED}❌ Error en dependencias${NC}"
    exit 1
fi
echo ""

# Mostrar opciones
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✅ Inicialización completada${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${YELLOW}Comandos disponibles:${NC}"
echo ""
echo -e "  ${GREEN}1. Aplicación principal de reportes:${NC}"
echo -e "     streamlit run scripts/app.py"
echo ""
echo -e "  ${GREEN}2. Validador de números:${NC}"
echo -e "     streamlit run scripts/validador_app.py"
echo ""
echo -e "  ${GREEN}3. Ejecutar pruebas:${NC}"
echo -e "     python test_validator.py"
echo ""
echo -e "  ${GREEN}4. Ver ejemplos:${NC}"
echo -e "     python ejemplo_validador.py"
echo ""
echo -e "${YELLOW}Para ejecutar la aplicación ahora:${NC}"
echo -e "${GREEN}streamlit run scripts/app.py${NC}"
echo ""
