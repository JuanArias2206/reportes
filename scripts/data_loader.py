"""
Módulo para cargar y procesar datos de manera eficiente.
Especializado en trabajar con archivos grandes sin cargarlos completamente en memoria.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import streamlit as st
from config import (
    SMS_FILE,
    WHATSAPP_FILES,
    INTERACCIONES_FILE,
    SMS_COLUMNS,
    WHATSAPP_COLUMNS,
    CSV_ENCODING,
    DELIMITERS,
)


@st.cache_data
def load_sms_data(sample: bool = True, sample_size: int = 10000) -> pd.DataFrame:
    """Carga datos SMS optimizados."""
    try:
        if not SMS_FILE.exists():
            st.warning("No se encontró el archivo SMS. Asegúrate de colocar tus datos en data/mensajes_texto/.")
            return pd.DataFrame()

        dtypes = {
            "Id": "int32",
            "Celular": "category",
            "Mensaje": "string",
            "Fecha Envio": "string",
            "Fecha Proceso": "string",
            "Estado del envio": "category",
            "Referencia": "string",
            "Usuario": "category",
            "Operador": "category",
            "Tipo de Mensaje": "category",
            "Total Clicks URL 1": "Int16",
            "Total Clicks URL 2": "Int16",
            "Total Clicks URL 3": "Int16",
        }
        
        nrows = sample_size if sample else None
        
        df = pd.read_csv(
            SMS_FILE,
            encoding=CSV_ENCODING["sms"],
            delimiter=DELIMITERS["sms"],
            usecols=SMS_COLUMNS,
            nrows=nrows,
            dtype=dtypes,
            low_memory=False,
        )
        
        return df
    except Exception as e:
        st.warning(f"Error cargando SMS: {e}")
        return pd.DataFrame()


@st.cache_data
def load_whatsapp_data() -> pd.DataFrame:
    """Carga todos los datos de WhatsApp."""
    try:
        if not WHATSAPP_FILES:
            st.warning("No se encontraron archivos de WhatsApp. Coloca tus CSV en data/mensajes_whatsapp/.")
            return pd.DataFrame()

        all_dfs = []
        for wa_file in WHATSAPP_FILES:
            if not wa_file.exists():
                continue
            df = pd.read_csv(
                wa_file,
                encoding=CSV_ENCODING["whatsapp"],
                delimiter=DELIMITERS["whatsapp"],
            )
            all_dfs.append(df)

        if not all_dfs:
            st.warning("No se pudieron cargar archivos de WhatsApp.")
            return pd.DataFrame()

        return pd.concat(all_dfs, ignore_index=True)
    except Exception as e:
        st.warning(f"Error cargando WhatsApp: {e}")
        return pd.DataFrame()


@st.cache_data
def get_sms_statistics() -> Dict:
    """Obtiene estadísticas de SMS."""
    try:
        sms_stats = get_sms_states_summary()
        return {
            "total": count_total_sms_records(),
            "states": sms_stats,
        }
    except Exception as e:
        st.warning(f"Error en estadísticas SMS: {e}")
        return {"total": 0, "states": {}}


@st.cache_data
def get_whatsapp_statistics() -> Dict:
    """Obtiene estadísticas de WhatsApp."""
    try:
        whatsapp_df = load_whatsapp_data()
        
        if whatsapp_df.empty:
            return {"total": 0, "states": {}, "by_file": {}}
        
        total = len(whatsapp_df)
        status_col = 'Status' if 'Status' in whatsapp_df.columns else None
        states = {}
        
        if status_col:
            states = dict(whatsapp_df[status_col].value_counts())
        
        by_file = {}
        for wa_file in WHATSAPP_FILES:
            try:
                df = pd.read_csv(
                    wa_file,
                    encoding=CSV_ENCODING["whatsapp"],
                    delimiter=DELIMITERS["whatsapp"],
                )
                file_name = wa_file.name
                file_states = dict(df[status_col].value_counts()) if status_col else {}
                
                by_file[file_name] = {
                    "count": len(df),
                    "states": file_states,
                }
            except:
                pass
        
        return {
            "total": total,
            "states": states,
            "by_file": by_file,
        }
    except Exception as e:
        st.warning(f"Error en estadísticas WhatsApp: {e}")
        return {"total": 0, "states": {}, "by_file": {}}


@st.cache_data
def get_sms_flow_data() -> Tuple[List, List, List]:
    """Obtiene datos de flujo para SMS."""
    try:
        total_sms = count_total_sms_records()
        
        df = pd.read_csv(
            SMS_FILE,
            encoding=CSV_ENCODING["sms"],
            delimiter=DELIMITERS["sms"],
            usecols=["Estado del envio"],
            nrows=10000,
            dtype={"Estado del envio": "category"},
            low_memory=False
        )
        
        sample_size = len(df)
        source, target, value = [], [], []
        
        for state, count in df["Estado del envio"].value_counts().items():
            proportion = count / sample_size
            estimated = int(proportion * total_sms)
            if estimated > 0:
                source.append("Enviados")
                target.append(str(state))
                value.append(estimated)
        
        return source, target, value
    except Exception as e:
        st.warning(f"Error en flujo SMS: {e}")
        return [], [], []


@st.cache_data
def get_whatsapp_flow_data() -> Tuple[List, List, List]:
    """Obtiene datos de flujo para WhatsApp."""
    try:
        whatsapp_df = load_whatsapp_data()
        
        if whatsapp_df.empty or 'Status' not in whatsapp_df.columns:
            return [], [], []
        
        source, target, value = [], [], []
        
        for state, count in whatsapp_df['Status'].value_counts().items():
            if count > 0:
                source.append("Enviados")
                target.append(str(state))
                value.append(count)
        
        return source, target, value
    except Exception as e:
        st.warning(f"Error en flujo WhatsApp: {e}")
        return [], [], []


@st.cache_data
def count_total_sms_records() -> int:
    """Cuenta total de registros SMS."""
    try:
        if not SMS_FILE.exists():
            return 0
        import subprocess
        result = subprocess.run(['wc', '-l', str(SMS_FILE)], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return int(result.stdout.split()[0]) - 1
    except:
        pass
    
    count = 0
    chunk_size = 100000
    for chunk in pd.read_csv(
        SMS_FILE,
        encoding=CSV_ENCODING["sms"],
        delimiter=DELIMITERS["sms"],
        chunksize=chunk_size,
        usecols=["Id"]
    ):
        count += len(chunk)
    return count


@st.cache_data
def get_sms_states_summary() -> Dict:
    """Obtiene resumen de estados SMS."""
    try:
        if not SMS_FILE.exists():
            return {}
        df = pd.read_csv(
            SMS_FILE,
            encoding=CSV_ENCODING["sms"],
            delimiter=DELIMITERS["sms"],
            usecols=["Estado del envio"],
            nrows=10000,
            dtype={"Estado del envio": "category"},
            low_memory=False
        )
        
        total_sms = count_total_sms_records()
        sample_size = len(df)
        sample_counts = df["Estado del envio"].value_counts()
        
        state_counts = {}
        for state, sample_count in sample_counts.items():
            proportion = sample_count / sample_size
            estimated_count = int(proportion * total_sms)
            state_counts[state] = estimated_count
        
        return state_counts
    except Exception as e:
        st.warning(f"Aviso al procesar estados: {e}")
        return {}


@st.cache_data
def get_sms_clicks_stats() -> Dict:
    """Calcula estadísticas de clicks SMS."""
    try:
        if not SMS_FILE.exists():
            return {}
        total_sms = count_total_sms_records()
        
        df = pd.read_csv(
            SMS_FILE,
            encoding=CSV_ENCODING["sms"],
            delimiter=DELIMITERS["sms"],
            usecols=["Total Clicks URL 1", "Total Clicks URL 2", "Total Clicks URL 3"],
            nrows=10000,
            dtype={
                "Total Clicks URL 1": "Int16",
                "Total Clicks URL 2": "Int16",
                "Total Clicks URL 3": "Int16",
            },
            low_memory=False
        )
        
        df["Total Clicks URL 1"] = df["Total Clicks URL 1"].fillna(0).astype(int)
        df["Total Clicks URL 2"] = df["Total Clicks URL 2"].fillna(0).astype(int)
        df["Total Clicks URL 3"] = df["Total Clicks URL 3"].fillna(0).astype(int)
        
        sample_size = len(df)
        
        with_clicks_url1_sample = (df["Total Clicks URL 1"] > 0).sum()
        with_clicks_url2_sample = (df["Total Clicks URL 2"] > 0).sum()
        with_clicks_url3_sample = (df["Total Clicks URL 3"] > 0).sum()
        
        total_clicks_url1_sample = df["Total Clicks URL 1"].sum()
        total_clicks_url2_sample = df["Total Clicks URL 2"].sum()
        total_clicks_url3_sample = df["Total Clicks URL 3"].sum()
        
        with_clicks_url1 = int((with_clicks_url1_sample / sample_size) * total_sms)
        with_clicks_url2 = int((with_clicks_url2_sample / sample_size) * total_sms)
        with_clicks_url3 = int((with_clicks_url3_sample / sample_size) * total_sms)
        
        total_clicks_url1 = int((total_clicks_url1_sample / sample_size) * total_sms)
        total_clicks_url2 = int((total_clicks_url2_sample / sample_size) * total_sms)
        total_clicks_url3 = int((total_clicks_url3_sample / sample_size) * total_sms)
        
        with_any_click = max(with_clicks_url1, with_clicks_url2, with_clicks_url3)
        percentage = (with_any_click / total_sms * 100) if total_sms > 0 else 0
        
        return {
            "total_with_clicks": int(with_any_click),
            "total_sms": int(total_sms),
            "percentage": round(percentage, 2),
            "clicks_url1": int(with_clicks_url1),
            "clicks_url2": int(with_clicks_url2),
            "clicks_url3": int(with_clicks_url3),
            "total_clicks_url1": int(total_clicks_url1),
            "total_clicks_url2": int(total_clicks_url2),
            "total_clicks_url3": int(total_clicks_url3),
        }
    except Exception as e:
        st.warning(f"Error en clicks: {e}")
        return {}


def get_sms_file_size() -> str:
    """Obtiene el tamaño del archivo SMS."""
    try:
        size_bytes = SMS_FILE.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f}MB"
    except:
        return "Desconocido"


# ============= FUNCIONES PARA ANÁLISIS DE INTERACCIONES =============

@st.cache_data
def count_total_interacciones_records() -> int:
    """Cuenta total de registros en interacciones.csv."""
    try:
        if not INTERACCIONES_FILE.exists():
            return 0
        import subprocess
        result = subprocess.run(['wc', '-l', str(INTERACCIONES_FILE)], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return int(result.stdout.split()[0]) - 1
    except:
        pass
    
    count = sum(1 for _ in open(INTERACCIONES_FILE, encoding='LATIN1')) - 1
    return count


@st.cache_data
def get_interacciones_data(sample: bool = True, sample_size: int = 10000) -> pd.DataFrame:
    """Carga datos de interacciones."""
    try:
        if not INTERACCIONES_FILE.exists():
            st.warning("No se encontró interacciones.csv. Agrega tus datos en data/mensajes_texto/.")
            return pd.DataFrame()
        nrows = sample_size if sample else None
        
        df = pd.read_csv(
            INTERACCIONES_FILE,
            encoding='LATIN1',
            delimiter=';',
            usecols=['Id Envio', 'Telefono celular', 'Total de mensajes', 'Estado del envio', 'Operador', 'Codigo corto'],
            nrows=nrows,
            dtype={
                'Id Envio': 'string',
                'Telefono celular': 'int64',
                'Total de mensajes': 'Int16',
                'Estado del envio': 'category',
                'Operador': 'category',
                'Codigo corto': 'string',
            },
            low_memory=False
        )
        
        return df
    except Exception as e:
        st.warning(f"Error cargando interacciones: {e}")
        return pd.DataFrame()


@st.cache_data
def get_interacciones_states_summary() -> Dict:
    """Obtiene resumen de estados de interacciones."""
    try:
        if not INTERACCIONES_FILE.exists():
            return {}
        total = count_total_interacciones_records()
        
        df = pd.read_csv(
            INTERACCIONES_FILE,
            encoding='LATIN1',
            delimiter=';',
            usecols=['Estado del envio'],
            nrows=10000,
            dtype={'Estado del envio': 'category'},
            low_memory=False
        )
        
        sample_size = len(df)
        sample_counts = df['Estado del envio'].value_counts()
        
        state_counts = {}
        for state, sample_count in sample_counts.items():
            proportion = sample_count / sample_size
            estimated_count = int(proportion * total)
            state_counts[state] = estimated_count
        
        return state_counts
    except Exception as e:
        st.warning(f"Error en resumen de interacciones: {e}")
        return {}


@st.cache_data
def get_interacciones_by_operator() -> Dict:
    """Obtiene estadísticas por operador."""
    try:
        total = count_total_interacciones_records()
        
        df = pd.read_csv(
            INTERACCIONES_FILE,
            encoding='LATIN1',
            delimiter=';',
            usecols=['Operador'],
            nrows=10000,
            dtype={'Operador': 'category'},
            low_memory=False
        )
        
        sample_size = len(df)
        sample_counts = df['Operador'].value_counts()
        
        operator_counts = {}
        for operator, sample_count in sample_counts.items():
            if pd.notna(operator):
                proportion = sample_count / sample_size
                estimated_count = int(proportion * total)
                operator_counts[operator] = estimated_count
        
        return operator_counts
    except Exception as e:
        st.warning(f"Error en análisis por operador: {e}")
        return {}


@st.cache_data
def get_interacciones_by_codigo_corto() -> Dict:
    """Obtiene estadísticas por código corto."""
    try:
        total = count_total_interacciones_records()
        
        df = pd.read_csv(
            INTERACCIONES_FILE,
            encoding='LATIN1',
            delimiter=';',
            usecols=['Codigo corto'],
            nrows=10000,
            dtype={'Codigo corto': 'string'},
            low_memory=False
        )
        
        sample_size = len(df)
        sample_counts = df['Codigo corto'].value_counts()
        
        codigo_counts = {}
        for codigo, sample_count in sample_counts.items():
            if pd.notna(codigo) and codigo != '':
                proportion = sample_count / sample_size
                estimated_count = int(proportion * total)
                codigo_counts[codigo] = estimated_count
        
        return codigo_counts
    except Exception as e:
        st.warning(f"Error en análisis por código corto: {e}")
        return {}


@st.cache_data
def get_interacciones_interaction_flow() -> Tuple[List, List, List]:
    """Obtiene datos para diagrama de flujo de interacciones."""
    try:
        total = count_total_interacciones_records()
        
        df = pd.read_csv(
            INTERACCIONES_FILE,
            encoding='LATIN1',
            delimiter=';',
            usecols=['Total de mensajes', 'Estado del envio'],
            nrows=10000,
            dtype={
                'Total de mensajes': 'Int16',
                'Estado del envio': 'category'
            },
            low_memory=False
        )
        
        sample_size = len(df)
        source, target, value = [], [], []
        
        for num_messages in df['Total de mensajes'].dropna().unique()[:5]:
            for state in df['Estado del envio'].unique():
                count = len(df[(df['Total de mensajes'] == num_messages) & (df['Estado del envio'] == state)])
                if count > 0:
                    proportion = count / sample_size
                    estimated = int(proportion * total)
                    if estimated > 0:
                        source.append(f"{int(num_messages)} msgs")
                        target.append(str(state))
                        value.append(estimated)
        
        return source, target, value
    except Exception as e:
        st.warning(f"Error en flujo de interacciones: {e}")
        return [], [], []


# ============= FUNCIONES PARA ANÁLISIS DE WHATSAPP FALLIDOS =============

# Importar validador completo
from phone_validator import validar_numero_colombiano, detectar_patron_sospechoso

def validate_colombian_phone(phone_str: str) -> Dict:
    """
    Valida número celular colombiano usando el validador completo.
    Wrapper para mantener compatibilidad con código existente.
    """
    resultado = validar_numero_colombiano(phone_str)
    
    # Convertir formato del validador al formato esperado por el código existente
    validation = {
        'valid': resultado['valido'],
        'issues': [resultado['mensaje_error']] if resultado['mensaje_error'] else [],
        'operator': resultado['operador'],
        'type': 'Celular Colombia' if resultado['valido'] else 'Inválido',
        'categoria': resultado['categoria'],
        'sospechoso': resultado['sospechoso'],
        'razon_sospecha': resultado['razon_sospecha'],
    }
    
    return validation


@st.cache_data
def get_whatsapp_failed_analysis() -> Dict:
    """Analiza números fallidos y en procesamiento en WhatsApp para data quality enriquecido."""
    try:
        all_failed = []
        all_processing = []
        
        for wa_file in WHATSAPP_FILES:
            try:
                df = pd.read_csv(wa_file, encoding='utf-8', delimiter=',')
                
                # Mensajes fallidos
                failed_df = df[df['Status'] == 'Failed'].copy() if 'Status' in df.columns else pd.DataFrame()
                if not failed_df.empty:
                    all_failed.append(failed_df)
                
                # Mensajes en procesamiento
                processing_df = df[df['Status'] == 'Processing'].copy() if 'Status' in df.columns else pd.DataFrame()
                if not processing_df.empty:
                    all_processing.append(processing_df)
            except:
                pass
        
        if not all_failed and not all_processing:
            return {
                'total_failed': 0,
                'total_processing': 0,
                'unique_phones': 0,
                'repeated_phones': {},
                'top_prefixes': {},
                'error_codes': {},
                'invalid_format': {},
                'by_operator': {},
                'validation_summary': {},
                'processing_phones': {},
            }
        
        # Combinar todos los datos problemáticos
        problematic_dfs = []
        if all_failed:
            problematic_dfs.extend(all_failed)
        if all_processing:
            problematic_dfs.extend(all_processing)
        
        problematic_combined = pd.concat(problematic_dfs, ignore_index=True) if problematic_dfs else pd.DataFrame()
        
        phone_col = 'Phone number' if 'Phone number' in problematic_combined.columns else None
        error_col = 'Error Code' if 'Error Code' in problematic_combined.columns else None
        status_col = 'Status' if 'Status' in problematic_combined.columns else None
        
        if not phone_col:
            return {'total_failed': len(all_failed) if all_failed else 0}
        
        total_failed = len(pd.concat(all_failed, ignore_index=True)) if all_failed else 0
        total_processing = len(pd.concat(all_processing, ignore_index=True)) if all_processing else 0
        
        phones = problematic_combined[phone_col].dropna().astype(str)
        unique_phones = phones.nunique()
        
        # Números repetidos
        repeated = phones.value_counts()
        repeated_phones = dict(repeated[repeated > 1].head(20))
        
        # Teléfonos en processing
        processing_phones = {}
        if all_processing:
            processing_combined = pd.concat(all_processing, ignore_index=True)
            processing_phone_list = processing_combined[phone_col].dropna().astype(str)
            processing_phones = dict(processing_phone_list.value_counts().head(10))
        
        # Análisis de prefijos (después del 57)
        prefixes = {}
        for phone in phones.unique():
            # Limpiar y remover código de país
            clean = phone.replace('+', '').replace(' ', '')
            if clean.startswith('57'):
                clean = clean[2:]  # Remover el 57
            
            if len(clean) >= 3:
                prefix = clean[:3]  # Primeros 3 dígitos después del 57
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
        
        top_prefixes = dict(sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Códigos de error (solo para Failed)
        error_codes = {}
        if error_col and all_failed:
            failed_combined = pd.concat(all_failed, ignore_index=True)
            errors = failed_combined[error_col].dropna()
            error_codes = dict(errors.value_counts().head(10))
        
        # Validación colombiana mejorada con detección de patrones sospechosos
        invalid_format = {}
        by_operator = {}
        validation_issues = {}
        suspicious_phones = {}
        by_category = {}
        
        for phone in phones.unique():
            validation = validate_colombian_phone(phone)
            
            # Contar por categoría
            categoria = validation.get('categoria', 'Desconocido')
            by_category[categoria] = by_category.get(categoria, 0) + 1
            
            # Números inválidos
            if not validation['valid']:
                issue_summary = '; '.join(validation['issues']) if validation['issues'] else 'Inválido'
                invalid_format[phone] = issue_summary
                validation_issues[issue_summary] = validation_issues.get(issue_summary, 0) + 1
            
            # Números sospechosos (válidos pero con patrones raros)
            if validation.get('sospechoso', False):
                suspicious_phones[phone] = validation.get('razon_sospecha', 'Patrón sospechoso')
            
            # Contar por operador
            operator = validation['operator']
            if operator not in by_operator:
                by_operator[operator] = 0
            by_operator[operator] += 1
        
        validation_summary = {
            'números_inválidos': len(invalid_format),
            'números_válidos': unique_phones - len(invalid_format),
            'números_sospechosos': len(suspicious_phones),
            'issues_principales': dict(sorted(validation_issues.items(), key=lambda x: x[1], reverse=True)[:5]),
            'por_categoria': dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True))
        }
        
        return {
            'total_failed': total_failed,
            'total_processing': total_processing,
            'unique_phones': unique_phones,
            'repeated_phones': repeated_phones,
            'processing_phones': processing_phones,
            'top_prefixes': top_prefixes,
            'error_codes': error_codes,
            'invalid_format': invalid_format,
            'suspicious_phones': suspicious_phones,
            'by_operator': dict(sorted(by_operator.items(), key=lambda x: x[1], reverse=True)),
            'validation_summary': validation_summary,
        }
    
    except Exception as e:
        return {}


@st.cache_data
def get_whatsapp_failed_details() -> pd.DataFrame:
    """Retorna detalles de mensajes fallidos."""
    try:
        all_failed = []
        
        for wa_file in WHATSAPP_FILES:
            try:
                df = pd.read_csv(wa_file, encoding='utf-8', delimiter=',')
                failed_df = df[df['Status'] == 'Failed'].copy() if 'Status' in df.columns else pd.DataFrame()
                
                if not failed_df.empty:
                    cols_to_keep = ['Phone number', 'Status', 'Date Sent', 'Error Code'] 
                    cols_available = [c for c in cols_to_keep if c in failed_df.columns]
                    all_failed.append(failed_df[cols_available])
            except:
                pass
        
        if not all_failed:
            return pd.DataFrame()
        
        result = pd.concat(all_failed, ignore_index=True)
        return result.head(100)
    
    except Exception as e:
        return pd.DataFrame()
