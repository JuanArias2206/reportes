"""
Módulo para análisis de sentimientos usando OpenAI API.
Clasifica mensajes como positivos, negativos o neutrales.
"""

import pandas as pd
from openai import OpenAI
import json
from pathlib import Path
import hashlib
import os

# API KEY desde variables de entorno (usa os.getenv para obtener)
# En producción: export OPENAI_API_KEY="sk-..."
# En Streamlit Cloud: Agregar en secretos del proyecto
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    import warnings
    warnings.warn("⚠️ OPENAI_API_KEY no configurada. Algunos análisis fallarán.")

CACHE_FILE = Path(__file__).parent.parent / "data" / ".sentiment_cache.json"

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def load_cache() -> dict:
    """Carga el cache de análisis de sentimientos."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_cache(cache: dict):
    """Guarda el cache de análisis de sentimientos."""
    try:
        os.makedirs(CACHE_FILE.parent, exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando cache: {e}")


def get_message_hash(message: str) -> str:
    """Genera un hash único para un mensaje."""
    return hashlib.md5(message.encode()).hexdigest()


def analyze_sentiment(message: str, use_cache=True) -> dict:
    """
    Analiza el sentimiento de un mensaje usando OpenAI.
    
    Args:
        message: Texto del mensaje a analizar
        use_cache: Usar cache si está disponible
    
    Returns:
        {
            'mensaje': str,
            'sentimiento': 'positivo' | 'negativo' | 'neutral',
            'confianza': float (0-1),
            'razon': str
        }
    """
    if not message or len(str(message).strip()) == 0:
        return {
            'mensaje': message,
            'sentimiento': 'neutral',
            'confianza': 0.0,
            'razon': 'Mensaje vacío'
        }
    
    msg_hash = get_message_hash(message)
    cache = load_cache()
    
    # Verificar si ya está en cache
    if use_cache and msg_hash in cache:
        return cache[msg_hash]
    
    # Si no hay cliente configurado
    if not client or not OPENAI_API_KEY:
        return {
            'mensaje': message[:100],
            'sentimiento': 'neutral',
            'confianza': 0.0,
            'razon': 'API Key no configurada'
        }
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un analizador de sentimientos en español.
                    Analiza cada mensaje y clasifícalo como:
                    - positivo: si expresa apoyo, satisfacción, acuerdo, entusiasmo
                    - negativo: si expresa rechazo, insatisfacción, crítica, desacuerdo
                    - neutral: si es informativo, sin carga emocional clara
                    
                    Responde SOLO en formato JSON:
                    {
                        "sentimiento": "positivo|negativo|neutral",
                        "confianza": 0.0-1.0,
                        "razon": "explicación breve"
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Analiza este mensaje: '{message}'"
                }
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        # Parsear respuesta
        response_text = response.choices[0].message.content.strip()
        data = json.loads(response_text)
        
        result = {
            'mensaje': message[:100],  # Truncar para almacenamiento
            'sentimiento': data['sentimiento'],
            'confianza': data['confianza'],
            'razon': data['razon']
        }
        
        # Guardar en cache
        cache[msg_hash] = result
        save_cache(cache)
        
        return result
        
    except Exception as e:
        return {
            'mensaje': message[:100],
            'sentimiento': 'neutral',
            'confianza': 0.0,
            'razon': f'Error: {str(e)[:50]}'
        }


def analyze_multiple_messages(messages: list, batch_size=10, use_cache=True) -> list:
    """
    Analiza múltiples mensajes en lotes.
    
    Args:
        messages: Lista de mensajes a analizar
        batch_size: Número de mensajes por lote
        use_cache: Usar cache
    
    Returns:
        Lista de análisis de sentimientos
    """
    results = []
    
    for i, message in enumerate(messages):
        result = analyze_sentiment(message, use_cache=use_cache)
        results.append(result)
        
        if (i + 1) % batch_size == 0:
            print(f"✅ Procesados {i + 1}/{len(messages)} mensajes")
    
    return results


def get_sentiment_summary(sentiments: list) -> dict:
    """Genera un resumen de sentimientos."""
    df = pd.DataFrame(sentiments)
    
    total = len(df)
    positivos = len(df[df['sentimiento'] == 'positivo'])
    negativos = len(df[df['sentimiento'] == 'negativo'])
    neutrales = len(df[df['sentimiento'] == 'neutral'])
    
    confianza_promedio = df['confianza'].mean()
    
    return {
        'total': total,
        'positivos': positivos,
        'negativos': negativos,
        'neutrales': neutrales,
        'porcentajes': {
            'positivos': (positivos / total * 100) if total > 0 else 0,
            'negativos': (negativos / total * 100) if total > 0 else 0,
            'neutrales': (neutrales / total * 100) if total > 0 else 0,
        },
        'confianza_promedio': confianza_promedio
    }
