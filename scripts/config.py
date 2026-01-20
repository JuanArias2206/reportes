"""
Configuración centralizada para la aplicación de visualización de estados de mensajes.
"""

from pathlib import Path
from typing import Dict, List

# Directorios
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SMS_DIR = DATA_DIR / "mensajes_texto"
WHATSAPP_DIR = DATA_DIR / "mensajes_whatsapp"

# Archivos de datos con fallback automático a muestras pequeñas
def _resolve_sms_file() -> Path:
    principal = SMS_DIR / "mensajes_texto.csv"
    muestra = SMS_DIR / "mensajes_texto_sample.csv"
    return principal if principal.exists() else muestra


def _resolve_interacciones_file() -> Path:
    principal = SMS_DIR / "interacciones.csv"
    muestra = SMS_DIR / "interacciones_sample.csv"
    return principal if principal.exists() else muestra


def _resolve_whatsapp_files() -> List[Path]:
    """Resuelve TODOS los archivos WhatsApp, priorizando los reales sobre samples."""
    files = sorted(WHATSAPP_DIR.glob("*.csv"))
    if not files:
        return []
    # Separar en reales y samples
    reales = [f for f in files if "_sample" not in f.name.lower()]
    samples = [f for f in files if "_sample" in f.name.lower()]
    # Retornar TODOS: primero reales, luego samples como fallback
    return (reales if reales else []) + samples


SMS_FILE = _resolve_sms_file()
INTERACCIONES_FILE = _resolve_interacciones_file()
WHATSAPP_FILES = _resolve_whatsapp_files()

# Configuración de lectura de CSV
CSV_ENCODING = {
    "sms": "LATIN1",
    "whatsapp": "utf-8",
}

# Delimitadores
DELIMITERS = {
    "sms": ";",
    "whatsapp": ",",
}

# Columnas relevantes para SMS
SMS_COLUMNS = [
    "Id Envio",
    "Telefono celular",
    "Mensaje",
    "Fecha de Carga",
    "Fecha y hora procesado",
    "Estado del envio",
    "Referencia",
    "Usuario",
    "Operador",
    "Tipo Mensaje",
    "Total Clicks URL 1",
    "Total Clicks URL 2",
    "Total Clicks URL 3",
]

# Columnas relevantes para WhatsApp
WHATSAPP_COLUMNS = [
    "Nick name",
    "Phone number",
    "Status",
    "Date Sent",
    "Date Delivered",
    "Date Read",
    "Reply Status",
    "Date First replied",
    "First reply message",
]

# Estados posibles según el esquema de flujo
FLOW_STATES = {
    "initial_state": "Leído",
    "joined_community": "Se unió a la comunidad",
    "positive_interaction": "Interacción positiva",
    "no_interaction": "Sin interacción",
    "negative_interaction": "Interacción negativa",
    "not_read": "No leído",
    "reminder": "Mensaje de recordatorio",
}

# Mapeos de estados para SMS
SMS_STATE_MAPPING = {
    "Entregado al operador": "Enviado",
    "Lista negra": "Rechazado",
    "Operador fallido": "Fallido",
    "Entregado": "Entregado",
}

# Mapeos de estados para WhatsApp
WHATSAPP_STATE_MAPPING = {
    "Delivered": "Entregado",
    "Read": "Leído",
    "Failed": "Fallido",
    "Processing": "Procesando",
}

# Colores para visualizaciones
COLORS = {
    # Estados iniciales
    "Leído": "#28a745",
    "No leído": "#ff9800",
    
    # Estados de entrega
    "Se unió a la comunidad": "#2196F3",
    "Entregado": "#2196F3",
    
    # Interacciones
    "Interacción positiva": "#9C27B0",
    "Sin interacción": "#FFC107",
    "Interacción negativa": "#F44336",
    
    # Estados genéricos
    "Enviado": "#4CAF50",
    "Fallido": "#F44336",
    "Procesando": "#FFC107",
    "Read": "#9C27B0",
    "Failed": "#F44336",
    "Processing": "#FFC107",
    "Rechazado": "#FF9800",
    "Mensaje de recordatorio": "#17A2B8",
}

# Configuración de Streamlit
PAGE_CONFIG = {
    "page_title": "Estados de Interacción",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Mensajes
MESSAGES = {
    "title": "Estados de Interacción de Mensajes",
    "subtitle": "Análisis de flujos de comunicación SMS y WhatsApp",
    "sms_section": "📱 SMS (Mensajes de Texto)",
    "whatsapp_section": "💬 WhatsApp",
    "sankey_section": "🔀 Diagrama de Flujos",
}
