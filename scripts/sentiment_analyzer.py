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

# API KEY desde variable de entorno o .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

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


def analyze_batch(messages: list, use_cache: bool = True, batch_size: int = 10) -> list:
    """
    Analiza un lote de mensajes en una sola llamada a OpenAI usando gpt-5-nano.
    
    Args:
        messages: Lista de mensajes a analizar
        use_cache: Si usar cache
        batch_size: Cantidad de mensajes por llamada (default 10)
    
    Returns:
        list: Lista de dicts con análisis de sentimiento
    """
    if not messages:
        return []
    
    if not client or not OPENAI_API_KEY:
        return [{
            'mensaje': msg[:100],
            'sentimiento': 'neutral',
            'confianza': 0.0,
            'razon': 'API Key no configurada'
        } for msg in messages]
    
    cache = load_cache()
    all_results = []
    
    # Procesar en lotes
    for batch_idx in range(0, len(messages), batch_size):
        batch = messages[batch_idx:batch_idx+batch_size]
        cached_results = {}
        to_analyze = []
        
        # Verificar qué mensajes están en cache
        for msg in batch:
            msg_hash = get_message_hash(msg)
            if use_cache and msg_hash in cache:
                cached_results[msg] = cache[msg_hash]
            else:
                to_analyze.append(msg)
        
        # Si hay mensajes para analizar
        if to_analyze:
            try:
                # Crear prompt para análisis en lote
                msgs_text = "\n".join([f"{i+1}. {msg[:200]}" for i, msg in enumerate(to_analyze)])
                
                response = client.chat.completions.create(
                    model="gpt-5-nano",
                    messages=[
                        {
                            "role": "system",
                            "content": """Eres un analizador de sentimientos en español.
                            Analiza cada mensaje y clasifícalo como positivo, negativo o neutral.
                            RESPONDE SOLO CON JSON VÁLIDO en este formato exacto:
                            {
                                "resultados": [
                                    {"indice": 0, "sentimiento": "positivo", "confianza": 0.95, "razon": "..."},
                                    {"indice": 1, "sentimiento": "neutral", "confianza": 0.8, "razon": "..."}
                                ]
                            }"""
                        },
                        {
                            "role": "user",
                            "content": f"Analiza estos mensajes:\n{msgs_text}"
                        }
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                result_text = response.choices[0].message.content.strip()
                print(f"📊 DEBUG Lote {batch_idx//batch_size + 1}: {len(to_analyze)} mensajes")
                print(f"📝 Respuesta OpenAI (primeros 300 chars): {result_text[:300]}...")
                
                batch_results = json.loads(result_text)
                
                # Procesar resultados del lote
                for item in batch_results.get('resultados', []):
                    idx = item.get('indice', 0)
                    if idx < len(to_analyze):
                        msg = to_analyze[idx]
                        output = {
                            'mensaje': msg[:100],
                            'sentimiento': item.get('sentimiento', 'neutral').lower(),
                            'confianza': float(item.get('confianza', 0.0)),
                            'razon': item.get('razon', '')
                        }
                        msg_hash = get_message_hash(msg)
                        cache[msg_hash] = output
                        all_results.append(output)
                        print(f"✅ {msg[:50]}... → {output['sentimiento']}")
            
            except json.JSONDecodeError as e:
                print(f"❌ JSON Error: {e}")
                print(f"📝 Texto recibido: {result_text[:500]}")
                for msg in to_analyze:
                    all_results.append({
                        'mensaje': msg[:100],
                        'sentimiento': 'neutral',
                        'confianza': 0.0,
                        'razon': 'Error parsing respuesta JSON'
                    })
            except Exception as e:
                print(f"❌ Error en lote: {e}")
                for msg in to_analyze:
                    all_results.append({
                        'mensaje': msg[:100],
                        'sentimiento': 'neutral',
                        'confianza': 0.0,
                        'razon': f'Error: {str(e)[:50]}'
                    })
        
        # Agregar resultados del cache
        all_results.extend([cached_results[msg] for msg in batch if msg in cached_results])
    
    # Guardar cache actualizado
    if all_results:
        save_cache(cache)
    
    return all_results


def analyze_sentiment(message: str, use_cache: bool = True) -> dict:
    """
    Analiza el sentimiento de un mensaje individual.
    
    Returns:
        dict: {'mensaje': str, 'sentimiento': str, 'confianza': float, 'razon': str}
    """
    if not message or len(str(message).strip()) == 0:
        return {
            'mensaje': message,
            'sentimiento': 'neutral',
            'confianza': 0.0,
            'razon': 'Mensaje vacío'
        }
    
    result = analyze_batch([message], use_cache=use_cache, batch_size=1)
    return result[0] if result else {
        'mensaje': message[:100],
        'sentimiento': 'neutral',
        'confianza': 0.0,
        'razon': 'Error desconocido'
    }


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
