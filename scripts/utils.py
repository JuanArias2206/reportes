"""
Utilidades y funciones auxiliares para la aplicación.
Incluye funciones de helper, conversiones y funciones de procesamiento.
"""

import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import re


def normalize_phone(phone: str) -> str:
    """Normaliza números telefónicos."""
    if isinstance(phone, str):
        phone = re.sub(r'\D', '', phone)
    return str(phone)


def categorize_response_time(sent_date: datetime, received_date: datetime) -> str:
    """Categoriza el tiempo de respuesta."""
    if pd.isna(sent_date) or pd.isna(received_date):
        return "Sin entrega"
    
    delta = received_date - sent_date
    minutes = delta.total_seconds() / 60
    
    if minutes < 1:
        return "Inmediato (< 1 min)"
    elif minutes < 5:
        return "Muy rápido (< 5 min)"
    elif minutes < 30:
        return "Rápido (< 30 min)"
    elif minutes < 60:
        return "Moderado (< 1 hora)"
    elif minutes < 1440:
        return "Lento (< 1 día)"
    else:
        return "Muy lento (> 1 día)"


def calculate_engagement_rate(df: pd.DataFrame, total_sent: int) -> float:
    """Calcula tasa de engagement (interacción)."""
    if total_sent == 0:
        return 0.0
    
    engaged = len(df[df.get("status") == "Leído"])
    return (engaged / total_sent) * 100


def get_date_range(df: pd.DataFrame, date_col: str) -> Tuple[datetime, datetime]:
    """Obtiene rango de fechas de un DataFrame."""
    if date_col not in df.columns:
        return None, None
    
    dates = pd.to_datetime(df[date_col], errors="coerce")
    return dates.min(), dates.max()


def get_busiest_hours(df: pd.DataFrame, date_col: str) -> Dict[int, int]:
    """Identifica las horas más activas."""
    if date_col not in df.columns:
        return {}
    
    dates = pd.to_datetime(df[date_col], errors="coerce")
    hours = dates.dt.hour.value_counts().sort_index()
    
    return hours.to_dict()


def get_busiest_days(df: pd.DataFrame, date_col: str) -> Dict[str, int]:
    """Identifica los días más activos."""
    if date_col not in df.columns:
        return {}
    
    dates = pd.to_datetime(df[date_col], errors="coerce")
    day_names = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
        4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    
    days = dates.dt.dayofweek.value_counts().sort_index()
    return {day_names[idx]: int(count) for idx, count in days.items()}


def format_large_number(num: int) -> str:
    """Formatea números grandes con separadores."""
    return f"{num:,}"


def generate_summary_text(sms_total: int, whatsapp_total: int, sms_states: Dict, whatsapp_states: Dict) -> str:
    """Genera un resumen textual de estadísticas."""
    total = sms_total + whatsapp_total
    
    sms_delivered = sms_states.get("Entregado al operador", 0)
    sms_failed = sms_states.get("Operador fallido", 0)
    sms_rejected = sms_states.get("Lista negra", 0)
    
    wpp_delivered = whatsapp_states.get("Delivered", 0)
    wpp_read = whatsapp_states.get("Read", 0)
    wpp_failed = whatsapp_states.get("Failed", 0)
    
    summary = f"""
    📊 RESUMEN EJECUTIVO
    
    Total de Mensajes Enviados: {total:,}
    
    📱 SMS ({sms_total:,} mensajes)
    - Entregados: {sms_delivered:,} ({sms_delivered/sms_total*100:.1f}% if sms_total > 0 else 0)
    - Fallidos: {sms_failed:,} ({sms_failed/sms_total*100:.1f}% if sms_total > 0 else 0)
    - Rechazados: {sms_rejected:,} ({sms_rejected/sms_total*100:.1f}% if sms_total > 0 else 0)
    
    💬 WhatsApp ({whatsapp_total:,} mensajes)
    - Entregados: {wpp_delivered:,} ({wpp_delivered/whatsapp_total*100:.1f}% if whatsapp_total > 0 else 0)
    - Leídos: {wpp_read:,} ({wpp_read/whatsapp_total*100:.1f}% if whatsapp_total > 0 else 0)
    - Fallidos: {wpp_failed:,} ({wpp_failed/whatsapp_total*100:.1f}% if whatsapp_total > 0 else 0)
    """
    
    return summary
