"""
Aplicación principal de Streamlit para visualizar estados de interacción.
Análisis separados de SMS, WhatsApp e Interacciones con visualizaciones mejoradas.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Agregar el directorio de scripts al path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# CLEANUP: Eliminar archivos sample Y CSVs grandes si existen (para limpiar cache en servidor)
BASE_DIR = scripts_dir.parent
DATA_DIR = BASE_DIR / "data"
files_to_remove = [
    # Samples
    DATA_DIR / "mensajes_whatsapp" / "whatsapp_sample.csv",
    DATA_DIR / "mensajes_texto" / "mensajes_texto_sample.csv",
    DATA_DIR / "mensajes_texto" / "interacciones_sample.csv",
    # CSVs grandes (deben usar Parquet)
    DATA_DIR / "mensajes_texto" / "mensajes_texto.csv",
    DATA_DIR / "mensajes_texto" / "interacciones.csv",
]
removed_files = []
for file_to_remove in files_to_remove:
    if file_to_remove.exists():
        try:
            os.remove(file_to_remove)
            removed_files.append(file_to_remove.name)
        except:
            pass

# Si se eliminaron archivos, mostrar advertencia
if removed_files:
    import streamlit as st
    st.warning(f"⚠️ **REBOOT REQUERIDO**: Se eliminaron {len(removed_files)} archivo(s) obsoleto(s). "
               f"Por favor REBOOT la app manualmente desde el dashboard de Streamlit Cloud para aplicar cambios. "
               f"Archivos eliminados: {', '.join(removed_files[:3])}")
    st.info("📍 **Cómo hacer reboot:** Dashboard → Encuentra 'reportes' → Click '⋮' → 'Reboot app'")
    st.stop()

from config import PAGE_CONFIG, MESSAGES, WHATSAPP_FILES
from data_loader import (
    load_sms_data,
    load_whatsapp_data,
    get_sms_statistics,
    get_whatsapp_statistics,
    get_sms_flow_data,
    get_whatsapp_flow_data,
    get_sms_clicks_stats,
    count_total_sms_records,
    get_sms_file_size,
    count_total_interacciones_records,
    get_interacciones_data,
    get_interacciones_states_summary,
    get_interacciones_by_operator,
    get_interacciones_by_codigo_corto,
    get_interacciones_interaction_flow,
    get_whatsapp_failed_analysis,
    get_whatsapp_failed_details,
    get_interacciones_messages,
    get_unique_messages,
    get_sentiment_stats_by_operator,
    get_sentiment_stats_by_codigo,
)
from visualizations import (
    create_sankey_diagram,
    create_status_bar_chart,
    create_pie_chart,
    create_horizontal_bar_chart,
    create_donut_chart,
    create_stacked_bar_chart,
    create_metric_cards,
)


def setup_page():
    """Configura la página de Streamlit con estilos mejorados."""
    st.set_page_config(**PAGE_CONFIG)
    st.markdown("""
    <style>
        /* Headers y títulos */
        .main-header {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: #555;
            font-weight: 500;
            margin-bottom: 2.5rem;
            font-style: italic;
        }
        
        .section-title {
            font-size: 2rem;
            font-weight: 800;
            color: #0d47a1;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            border-left: 5px solid #1f77b4;
            padding-left: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .section-divider {
            margin-top: 3rem;
            margin-bottom: 2rem;
            border-top: 3px solid #1f77b4;
            padding-top: 1.5rem;
        }
        
        .metrics-container {
            background: linear-gradient(135deg, rgba(31, 119, 180, 0.05) 0%, rgba(44, 160, 44, 0.05) 100%);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #1f77b4;
            margin-bottom: 1.5rem;
        }
        
        .tab-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0d47a1;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #1f77b4;
        }
        
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .success-box {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .data-source {
            font-size: 0.85rem;
            color: #999;
            font-style: italic;
            margin-top: 1rem;
            padding-top: 0.5rem;
            border-top: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Renderiza el encabezado de la aplicación."""
    st.markdown(f'<div class="main-header">{MESSAGES["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{MESSAGES["subtitle"]}</div>', unsafe_allow_html=True)


def render_sms_section():
    """Renderiza la sección completa de SMS con análisis detallado."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📱 ANÁLISIS DE CAMPAÑAS SMS</div>', unsafe_allow_html=True)
    st.markdown("*Visualización de 315K+ mensajes SMS procesados*")
    
    total_sms = count_total_sms_records()
    sms_stats = get_sms_statistics()
    file_size = get_sms_file_size()
    
    # Métricas resumen
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total SMS", f"{total_sms:,}")
    with col2:
        st.metric("💾 Tamaño Archivo", file_size)
    with col3:
        st.metric("🏷️ Estados Únicos", len(sms_stats["states"]))
    with col4:
        if sms_stats["states"]:
            top_state_count = max(sms_stats["states"].values())
            top_state = [k for k, v in sms_stats["states"].items() if v == top_state_count][0]
            st.metric("🔝 Estado Principal", top_state)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs para diferentes análisis
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Estados", "🔄 Flujo", "👆 Engagement", "📈 Gráficos", "📄 Datos"])
    
    with tab1:
        st.markdown("### Distribución de Estados")
        st.markdown("*Clasificación de mensajes SMS por su estado de entrega*")
        if sms_stats["states"]:
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = create_status_bar_chart(sms_stats["states"], "SMS por Estado")
                st.plotly_chart(fig_bar, use_container_width=True, key="sms_states_bar")
            with col2:
                fig_donut = create_donut_chart(sms_stats["states"], "Proporción de Estados")
                st.plotly_chart(fig_donut, use_container_width=True, key="sms_states_donut")
            
            # Tabla detallada
            st.markdown("#### Detalles de Estados")
            states_df = pd.DataFrame(
                [(state, count, f"{count/total_sms*100:.1f}%") 
                 for state, count in sorted(sms_stats["states"].items(), key=lambda x: x[1], reverse=True)],
                columns=["Estado", "Cantidad", "Porcentaje"]
            )
            st.dataframe(states_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### Flujo de Estados (Diagrama Sankey)")
        st.markdown("*Visualiza cómo transicionan los mensajes entre diferentes estados*")
        try:
            source, target, value = get_sms_flow_data()
            if source and target and value:
                fig = create_sankey_diagram(source, target, value, "Flujo SMS")
                st.plotly_chart(fig, use_container_width=True, key="sms_sankey")
            else:
                st.info("No hay suficientes datos para el Sankey")
        except Exception as e:
            st.error(f"Error en Sankey: {e}")
    
    with tab3:
        st.markdown("### 📊 Métricas de Engagement por URL")
        st.markdown("*Análisis de personas que dieron click en las URLs incluidas en los SMS*")
        try:
            clicks_stats = get_sms_clicks_stats()
            if clicks_stats:
                # Métricas principales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "👥 Personas con Clicks",
                        f"{clicks_stats['total_with_clicks']:,}",
                        f"{clicks_stats['percentage']:.1f}%"
                    )
                with col2:
                    total_clicks = (clicks_stats['total_clicks_url1'] + 
                                   clicks_stats['total_clicks_url2'] + 
                                   clicks_stats['total_clicks_url3'])
                    st.metric("🔗 Total de Clicks", f"{total_clicks:,}")
                with col3:
                    avg_clicks = total_clicks / total_sms if total_sms > 0 else 0
                    st.metric("📈 Clicks/SMS", f"{avg_clicks:.2f}")
                
                # Detalle por URL
                st.markdown("#### Clicks por URL")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("URL 1 - Personas", f"{clicks_stats['clicks_url1']:,}",
                             f"Σ {clicks_stats['total_clicks_url1']:,}")
                with col2:
                    st.metric("URL 2 - Personas", f"{clicks_stats['clicks_url2']:,}",
                             f"Σ {clicks_stats['total_clicks_url2']:,}")
                with col3:
                    st.metric("URL 3 - Personas", f"{clicks_stats['clicks_url3']:,}",
                             f"Σ {clicks_stats['total_clicks_url3']:,}")
                
                # Gráfico de engagement
                engagement_data = {
                    "URL 1": clicks_stats['total_clicks_url1'],
                    "URL 2": clicks_stats['total_clicks_url2'],
                    "URL 3": clicks_stats['total_clicks_url3'],
                }
                fig_engagement = create_horizontal_bar_chart(engagement_data, "Total Clicks por URL")
                st.plotly_chart(fig_engagement, use_container_width=True, key="sms_engagement")
        except Exception as e:
            st.error(f"Error en engagement: {e}")
    
    with tab4:
        st.markdown("### Visualizaciones Adicionales")
        col1, col2 = st.columns(2)
        
        if sms_stats["states"]:
            with col1:
                fig_pie = create_pie_chart(sms_stats["states"], "Distribución Porcentual")
                st.plotly_chart(fig_pie, use_container_width=True, key="sms_pie")
    
    with tab5:
        st.markdown("### Muestra de Datos SMS")
        sms_df = load_sms_data(sample=True, sample_size=100)
        if not sms_df.empty:
            st.write(f"**Mostrando 100 primeros registros de {total_sms:,} totales**")
            st.dataframe(sms_df, use_container_width=True)


def render_whatsapp_section():
    """Renderiza la sección completa de WhatsApp."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 ANÁLISIS DE WHATSAPP</div>', unsafe_allow_html=True)
    
    whatsapp_stats = get_whatsapp_statistics()
    total_wa = whatsapp_stats['total']
    num_files = len(whatsapp_stats.get('by_file', {}))
    
    # Encabezado con info de fuentes
    file_names = ", ".join([f.name for f in WHATSAPP_FILES]) if hasattr(WHATSAPP_FILES, '__iter__') else "múltiples archivos"
    st.markdown(f"*Análisis combinado de **{num_files} archivo(s)** con **{total_wa:,}+ mensajes** WhatsApp con validaciones de calidad*")
    st.markdown(f"<small>📂 Fuentes: {file_names}</small>", unsafe_allow_html=True)
    
    # Métricas resumen
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    st.markdown(f"**🔀 Datos Combinados de {num_files} archivo(s) WhatsApp:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💬 Total Mensajes", f"{total_wa:,}")
    with col2:
        st.metric("📂 Archivos Fuente", len(whatsapp_stats.get('by_file', {})))
    with col3:
        st.metric("🏷️ Estados Únicos", len(whatsapp_stats["states"]))
    with col4:
        if whatsapp_stats["states"]:
            top_state_count = max(whatsapp_stats["states"].values())
            top_state = [k for k, v in whatsapp_stats["states"].items() if v == top_state_count][0]
            st.metric("🔝 Estado Principal", top_state)
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Estados", "🔄 Flujo", "📈 Gráficos", "🔍 DQ Fallidos", "📄 Datos"])
    
    with tab1:
        st.markdown("### Distribución de Estados")
        st.markdown("*Clasificación de mensajes WhatsApp por su estado de entrega*")
        if whatsapp_stats["states"]:
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = create_status_bar_chart(whatsapp_stats["states"], "WhatsApp por Estado")
                st.plotly_chart(fig_bar, use_container_width=True, key="wa_states_bar")
            with col2:
                fig_donut = create_donut_chart(whatsapp_stats["states"], "Proporción de Estados")
                st.plotly_chart(fig_donut, use_container_width=True, key="wa_states_donut")
            
            # Tabla detallada
            st.markdown("#### Detalles de Estados")
            states_df = pd.DataFrame(
                [(state, count, f"{count/total_wa*100:.1f}%") 
                 for state, count in sorted(whatsapp_stats["states"].items(), key=lambda x: x[1], reverse=True)],
                columns=["Estado", "Cantidad", "Porcentaje"]
            )
            st.dataframe(states_df, use_container_width=True, hide_index=True)
            
            # Por archivo
            st.markdown("#### 📂 Desglose por Archivo Fuente (TOTAL COMBINADO)")
            st.markdown(f"*Estos datos provienen de {len(whatsapp_stats.get('by_file', {}))} archivo(s) en `data/mensajes_whatsapp/`*")
            
            # Tabla resumen de archivos
            if whatsapp_stats.get("by_file"):
                file_summary = []
                for file_name, file_data in whatsapp_stats.get("by_file", {}).items():
                    file_summary.append({
                        "📄 Archivo": file_name,
                        "Mensajes": file_data['count'],
                        "% del Total": f"{file_data['count']/total_wa*100:.1f}%"
                    })
                summary_df = pd.DataFrame(file_summary)
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            # Detalles expandibles por archivo
            for file_name, file_data in whatsapp_stats.get("by_file", {}).items():
                with st.expander(f"📄 {file_name} — {file_data['count']:,} mensajes"):
                    file_states_df = pd.DataFrame(
                        [(s, c, f"{c/file_data['count']*100:.1f}%")
                         for s, c in sorted(file_data["states"].items(), key=lambda x: x[1], reverse=True)],
                        columns=["Estado", "Cantidad", "Porcentaje"]
                    )
                    st.dataframe(file_states_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### 🔀 Flujo de Estados (Diagrama Sankey)")
        st.markdown("*Visualización en tiempo real del flujo de mensajes desde su envío hasta respuesta*")
        st.markdown("**Mostrado:** Total Enviados → Status (Delivered/Read/Failed/Processing) → Respuesta (Sí/No)")
        st.markdown(f"<small>📊 Datos agregados: {total_wa:,} mensajes de {len(whatsapp_stats.get('by_file', {}))} archivo(s)</small>", unsafe_allow_html=True)
        try:
            source, target, value = get_whatsapp_flow_data()
            if source and target and value and len(source) > 0:
                fig = create_sankey_diagram(source, target, value, "Flujo WhatsApp Completo")
                st.plotly_chart(fig, use_container_width=True, key="wa_sankey", height=700)
                
                # Tabla de flujos
                st.markdown("#### 📋 Detalle de Flujos")
                flow_df = pd.DataFrame({
                    'Desde': source,
                    'Hacia': target,
                    'Cantidad': value
                })
                flow_summary = flow_df.groupby(['Desde', 'Hacia'])['Cantidad'].sum().reset_index()
                st.dataframe(flow_summary, use_container_width=True, hide_index=True)
            else:
                st.info("No hay suficientes datos para el Sankey")
        except Exception as e:
            st.error(f"Error en Sankey: {str(e)}")
    
    with tab3:
        st.markdown("### Visualizaciones Adicionales")
        col1, col2 = st.columns(2)
        
        if whatsapp_stats["states"]:
            with col1:
                fig_pie = create_pie_chart(whatsapp_stats["states"], "Distribución Porcentual")
                st.plotly_chart(fig_pie, use_container_width=True, key="wa_pie")
    
    with tab4:
        st.markdown("### 🔍 Análisis de Calidad de Datos: Mensajes Problemáticos")
        st.markdown("*Análisis enriquecido con validaciones de números celulares colombianos (después del +57)*")
        
        failed_analysis = get_whatsapp_failed_analysis()
        
        if failed_analysis and (failed_analysis.get('total_failed', 0) > 0 or failed_analysis.get('total_processing', 0) > 0):
            # ===== MÉTRICAS RESUMEN =====
            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            st.markdown("#### 📊 Métricas Principales")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "🔴 Mensajes Fallidos",
                    f"{failed_analysis['total_failed']:,}",
                )
            
            with col2:
                st.metric(
                    "🟡 En Procesamiento",
                    f"{failed_analysis.get('total_processing', 0):,}",
                )
            
            with col3:
                pct_failed = (failed_analysis['total_failed'] / total_wa * 100) if total_wa > 0 else 0
                st.metric(
                    "⚠️ % Fallidos",
                    f"{pct_failed:.1f}%"
                )
            
            with col4:
                st.metric(
                    "📱 Teléfonos Únicos",
                    f"{failed_analysis['unique_phones']:,}"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ===== VALIDACIÓN COLOMBIANA =====
            if failed_analysis.get('validation_summary'):
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("#### ✅ Validación de Números Celulares Colombia (sin +57)")
                st.markdown("*Se validan los 10 dígitos después del código de país (+57)*")
                
                val_summary = failed_analysis['validation_summary']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    valid_count = val_summary.get('números_válidos', 0)
                    valid_pct = (valid_count / failed_analysis['unique_phones'] * 100) if failed_analysis['unique_phones'] > 0 else 0
                    st.metric(
                        "✓ Números Válidos",
                        f"{valid_count:,}",
                        f"{valid_pct:.1f}%"
                    )
                
                with col2:
                    invalid_count = val_summary.get('números_inválidos', 0)
                    invalid_pct = (invalid_count / failed_analysis['unique_phones'] * 100) if failed_analysis['unique_phones'] > 0 else 0
                    st.metric(
                        "✗ Números Inválidos",
                        f"{invalid_count:,}",
                        f"{invalid_pct:.1f}%"
                    )
                
                with col3:
                    suspicious_count = val_summary.get('números_sospechosos', 0)
                    suspicious_pct = (suspicious_count / failed_analysis['unique_phones'] * 100) if failed_analysis['unique_phones'] > 0 else 0
                    st.metric(
                        "⚠️ Sospechosos",
                        f"{suspicious_count:,}",
                        f"{suspicious_pct:.1f}%"
                    )
                
                with col4:
                    st.markdown("**Reglas Aplicadas:**")
                    st.write("• 10 dígitos después del 57")
                    st.write("• Comienza con 3 (celular)")
                    st.write("• Prefijo de operador válido")
                
                if val_summary.get('issues_principales'):
                    st.markdown("**Problemas Más Comunes:**")
                    for issue, count in val_summary.get('issues_principales', {}).items():
                        st.write(f"• **{issue}**: {count} números")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ===== NÚMEROS EN PROCESAMIENTO =====
            if failed_analysis.get('processing_phones'):
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.markdown("#### 🟡 Números en Estado 'Processing'")
                st.markdown(f"**{failed_analysis.get('total_processing', 0)}** mensajes aún en procesamiento - estos podrían pasar a Delivered o Failed")
                
                proc_df = pd.DataFrame([
                    (phone, count)
                    for phone, count in sorted(failed_analysis['processing_phones'].items(), key=lambda x: x[1], reverse=True)
                ], columns=["Número Teléfono", "Veces en Processing"])
                
                st.dataframe(proc_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ===== ANÁLISIS POR OPERADOR =====
            if failed_analysis.get('by_operator'):
                st.markdown("#### 📡 Distribución de Problemas por Operador")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    operator_data = failed_analysis['by_operator']
                    fig_operator = create_horizontal_bar_chart(
                        operator_data,
                        "Números con Problemas por Operador"
                    )
                    st.plotly_chart(fig_operator, use_container_width=True, key="wa_dq_operator")
                
                with col2:
                    st.markdown("**Detalle por Operador:**")
                    for op, count in sorted(failed_analysis['by_operator'].items(), key=lambda x: x[1], reverse=True):
                        pct = (count / failed_analysis['unique_phones'] * 100) if failed_analysis['unique_phones'] > 0 else 0
                        st.write(f"**{op}**: {count:,} números ({pct:.1f}%)")
                    
                    st.markdown('<div class="data-source">📌 Operadores identificados según prefijos después del +57</div>', unsafe_allow_html=True)
            
            # ===== ANÁLISIS DE PREFIJOS =====
            st.markdown("#### 📱 Análisis por Prefijo de Número (3 primeros dígitos después del +57)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if failed_analysis.get('top_prefixes'):
                    fig_prefix = create_horizontal_bar_chart(
                        failed_analysis['top_prefixes'],
                        "Top 10 Prefijos en Mensajes Problemáticos"
                    )
                    st.plotly_chart(fig_prefix, use_container_width=True, key="wa_dq_prefix")
            
            with col2:
                if failed_analysis.get('top_prefixes'):
                    st.markdown("**Prefijos Identificados:**")
                    for prefix, count in failed_analysis['top_prefixes'].items():
                        total_problematic = failed_analysis['total_failed'] + failed_analysis.get('total_processing', 0)
                        pct = (count / total_problematic * 100) if total_problematic > 0 else 0
                        st.write(f"**+57{prefix}**: {count:,} ({pct:.1f}%)")
                    
                    st.markdown('<div class="data-source">📌 Nota: Prefijo = primeros 3 dígitos después del código de país</div>', unsafe_allow_html=True)
            
            # ===== CÓDIGOS DE ERROR =====
            st.markdown("#### ⚠️ Análisis de Códigos de Error (Solo Failed)")
            
            if failed_analysis.get('error_codes'):
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_errors = create_horizontal_bar_chart(
                        failed_analysis['error_codes'],
                        "Códigos de Error Más Frecuentes"
                    )
                    st.plotly_chart(fig_errors, use_container_width=True, key="wa_dq_errors")
                
                with col2:
                    st.markdown("**Interpretación de Errores:**")
                    error_meanings = {
                        '31000': '🔴 Error de servidor',
                        '31001': '⚠️ Parámetro no válido',
                        '31005': '❌ Número de teléfono no válido',
                        '31008': '🚫 Usuario no tiene permisos',
                        '31100': '📵 Número no disponible',
                        '31301': '🚷 Mensaje rechazado por operador',
                    }
                    
                    for code, count in sorted(failed_analysis['error_codes'].items(), key=lambda x: x[1], reverse=True):
                        meaning = error_meanings.get(str(code), '❓ Error desconocido')
                        st.write(f"**{code}**: {meaning} ({count})")
            else:
                st.info("No hay códigos de error disponibles")
            
            # ===== NÚMEROS PROBLEMÁTICOS =====
            st.markdown("#### 🔴 Números Problemáticos (Múltiples Intentos Fallidos)")
            
            if failed_analysis.get('repeated_phones'):
                repeated_df = pd.DataFrame([
                    (phone, count)
                    for phone, count in sorted(failed_analysis['repeated_phones'].items(), 
                                              key=lambda x: x[1], reverse=True)
                ], columns=["Número Teléfono", "Intentos Fallidos"])
                
                st.dataframe(repeated_df, use_container_width=True, hide_index=True)
                
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.markdown(f"""
                **⚠️ Alerta**: Hay **{len(failed_analysis['repeated_phones'])}** números celulares que fallaron en múltiples intentos.
                
                **Posibles causas:**
                • 📵 Números bloqueados o cancelados
                • ❌ Números inválidos o inexistentes
                • 📡 Problemas de cobertura permanentes
                • 🚫 Restricciones del operador
                • 🔴 Teléfonos en lista negra
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ===== NÚMEROS SOSPECHOSOS =====
            if failed_analysis.get('suspicious_phones'):
                st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                st.markdown("#### ⚠️ Números con Patrones Sospechosos (Válidos pero Requieren Revisión)")
                st.markdown(f"**{len(failed_analysis['suspicious_phones'])}** números válidos pero con patrones inusuales detectados")
                
                suspicious_df = pd.DataFrame([
                    (phone, reason)
                    for phone, reason in list(failed_analysis['suspicious_phones'].items())[:20]
                ], columns=["Número Teléfono", "Patrón Detectado"])
                
                st.dataframe(suspicious_df, use_container_width=True, hide_index=True)
                
                if len(failed_analysis['suspicious_phones']) > 20:
                    st.write(f"*Mostrando 20 de {len(failed_analysis['suspicious_phones'])} números sospechosos*")
                
                st.markdown("""
                **Patrones Detectados:**
                • 🔢 Todos los dígitos iguales (ej: 3111111111)
                • 🔄 Secuencias numéricas (ej: 3012345678)
                • ⚡ Patrones alternantes (ej: 3012121212)
                • 0️⃣ Termina en muchos ceros (ej: 3001230000)
                • 🔁 Dígitos consecutivos repetidos (ej: 3001111123)
                
                **Nota:** Estos números pasan la validación técnica pero pueden requerir verificación manual.
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ===== RESUMEN POR CATEGORÍA =====
            if failed_analysis.get('validation_summary', {}).get('por_categoria'):
                st.markdown("#### 🏷️ Resumen por Categoría de Validación")
                
                categoria_data = failed_analysis['validation_summary']['por_categoria']
                fig_categoria = create_horizontal_bar_chart(
                    categoria_data,
                    "Distribución por Categoría"
                )
                st.plotly_chart(fig_categoria, use_container_width=True, key="wa_dq_categoria")
            
            # ===== NÚMEROS INVÁLIDOS =====
            if failed_analysis.get('invalid_format'):
                st.markdown("#### ❌ Números con Formato Inválido (No cumplen reglas colombianas)")
                
                invalid_df = pd.DataFrame([
                    (phone, issues)
                    for phone, issues in list(failed_analysis['invalid_format'].items())[:20]
                ], columns=["Número Teléfono", "Problemas Detectados"])
                
                st.dataframe(invalid_df, use_container_width=True, hide_index=True)
                
                if len(failed_analysis['invalid_format']) > 20:
                    st.write(f"*Mostrando 20 de {len(failed_analysis['invalid_format'])} números inválidos*")
        else:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("✅ **No hay mensajes con estado 'Failed' o 'Processing'** - La calidad de datos es excelente!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.subheader("Muestra de Datos WhatsApp")
        whatsapp_df = load_whatsapp_data()
        if not whatsapp_df.empty:
            st.write(f"Mostrando {len(whatsapp_df)} de {total_wa:,} registros")
            st.dataframe(whatsapp_df, use_container_width=True)


def render_interacciones_section():
    """Renderiza la sección de análisis de Interacciones."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💌 ANÁLISIS DE INTERACCIONES</div>', unsafe_allow_html=True)
    st.markdown("*Análisis de 315K+ interacciones de mensajes con múltiples canales*")
    
    total_inter = count_total_interacciones_records()
    inter_states = get_interacciones_states_summary()
    inter_operators = get_interacciones_by_operator()
    inter_codigos = get_interacciones_by_codigo_corto()
    
    # Métricas resumen
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💌 Total Interacciones", f"{total_inter:,}")
    with col2:
        st.metric("🏷️ Estados Únicos", len(inter_states))
    with col3:
        st.metric("📡 Operadores", len(inter_operators))
    with col4:
        st.metric("🔢 Códigos Cortos", len(inter_codigos))
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Estados", "📡 Operadores", "🔢 Códigos", "🔄 Flujo", "📄 Datos", "💭 Sentimientos"])
    
    with tab1:
        st.markdown("### Distribución de Estados")
        st.markdown("*Clasificación de interacciones por su estado de entrega*")
        if inter_states:
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = create_status_bar_chart(inter_states, "Interacciones por Estado")
                st.plotly_chart(fig_bar, use_container_width=True, key="inter_states_bar")
            with col2:
                fig_donut = create_donut_chart(inter_states, "Proporción de Estados")
                st.plotly_chart(fig_donut, use_container_width=True, key="inter_states_donut")
            
            # Tabla detallada
            st.markdown("#### Detalles de Estados")
            states_df = pd.DataFrame(
                [(state, count, f"{count/total_inter*100:.1f}%") 
                 for state, count in sorted(inter_states.items(), key=lambda x: x[1], reverse=True)],
                columns=["Estado", "Cantidad", "Porcentaje"]
            )
            st.dataframe(states_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### Distribución por Operador")
        st.markdown("*Análisis de interacciones separadas por operador de telefonía*")
        if inter_operators:
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = create_horizontal_bar_chart(inter_operators, "Interacciones por Operador")
                st.plotly_chart(fig_bar, use_container_width=True, key="inter_operators_bar")
            with col2:
                fig_donut = create_donut_chart(inter_operators, "Proporción por Operador")
                st.plotly_chart(fig_donut, use_container_width=True, key="inter_operators_donut")
            
            # Tabla detallada
            st.markdown("#### Detalles por Operador")
            op_df = pd.DataFrame(
                [(op, count, f"{count/total_inter*100:.1f}%") 
                 for op, count in sorted(inter_operators.items(), key=lambda x: x[1], reverse=True)],
                columns=["Operador", "Cantidad", "Porcentaje"]
            )
            st.dataframe(op_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Distribución por Código Corto")
        st.markdown("*Análisis de campaña por código corto utilizado*")
        if inter_codigos:
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = create_horizontal_bar_chart(inter_codigos, "Interacciones por Código")
                st.plotly_chart(fig_bar, use_container_width=True, key="inter_codigos_bar")
            with col2:
                fig_donut = create_donut_chart(inter_codigos, "Proporción por Código Corto")
                st.plotly_chart(fig_donut, use_container_width=True, key="inter_codigos_donut")
            
            # Tabla detallada
            st.markdown("#### Detalles por Código Corto")
            cod_df = pd.DataFrame(
                [(cod, count, f"{count/total_inter*100:.1f}%") 
                 for cod, count in sorted(inter_codigos.items(), key=lambda x: x[1], reverse=True)],
                columns=["Código Corto", "Cantidad", "Porcentaje"]
            )
            st.dataframe(cod_df, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### Flujo de Interacciones (Diagrama Sankey)")
        st.markdown("*Visualiza cómo fluyen las interacciones entre diferentes estados y canales*")
        try:
            source, target, value = get_interacciones_interaction_flow()
            if source and target and value:
                fig = create_sankey_diagram(source, target, value, "Flujo de Interacciones")
                st.plotly_chart(fig, use_container_width=True, key="inter_sankey")
            else:
                st.info("No hay suficientes datos para el Sankey")
        except Exception as e:
            st.error(f"Error en Sankey: {e}")
    
    with tab5:
        st.markdown("### Muestra de Datos Interacciones")
        inter_df = get_interacciones_data(sample=True, sample_size=100)
        if not inter_df.empty:
            st.write(f"**Mostrando 100 primeros registros de {total_inter:,} totales**")
            st.dataframe(inter_df, use_container_width=True)
    
    with tab6:
        st.markdown("### 💭 Análisis de Sentimientos con IA")
        st.markdown("*Clasificación automática de mensajes: Positivos, Negativos, Neutrales*")
        st.info("⚠️ Este análisis usa OpenAI API. Procesando un subconjunto de mensajes únicos.")
        
        # Botón para iniciar análisis
        if st.button("🚀 Iniciar Análisis de Sentimientos", key="sentiment_analysis_btn"):
            try:
                from sentiment_analyzer import analyze_sentiment, get_sentiment_summary
                
                st.write("⏳ Obteniendo mensajes únicos de interacciones...")
                unique_msgs = get_unique_messages(limit=500)
                
                if not unique_msgs:
                    st.warning("No hay mensajes disponibles para analizar")
                else:
                    st.write(f"📊 Analizando {len(unique_msgs)} mensajes únicos...")
                    
                    progress_bar = st.progress(0)
                    
                    sentiments = []
                    for i, msg in enumerate(unique_msgs):
                        sentiment = analyze_sentiment(msg, use_cache=True)
                        sentiments.append(sentiment)
                        progress = (i + 1) / len(unique_msgs)
                        progress_bar.progress(progress)
                    
                    st.success(f"✅ Análisis completado para {len(sentiments)} mensajes")
                    
                    summary = get_sentiment_summary(sentiments)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("💚 Positivos", f"{summary['positivos']:,}", 
                                 f"{summary['porcentajes']['positivos']:.1f}%")
                    with col2:
                        st.metric("❤️ Negativos", f"{summary['negativos']:,}", 
                                 f"{summary['porcentajes']['negativos']:.1f}%")
                    with col3:
                        st.metric("💛 Neutrales", f"{summary['neutrales']:,}", 
                                 f"{summary['porcentajes']['neutrales']:.1f}%")
                    with col4:
                        st.metric("🎯 Confianza Promedio", f"{summary['confianza_promedio']:.1%}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        sentiments_dict = {
                            'Positivos': summary['positivos'],
                            'Negativos': summary['negativos'],
                            'Neutrales': summary['neutrales']
                        }
                        fig_sentiment = create_pie_chart(sentiments_dict, "Distribución de Sentimientos")
                        st.plotly_chart(fig_sentiment, use_container_width=True)
                    
                    with col2:
                        fig_sentiment_bar = create_status_bar_chart(sentiments_dict, "Sentimientos por Categoría")
                        st.plotly_chart(fig_sentiment_bar, use_container_width=True)
                    
                    st.markdown("#### 📋 Detalle de Sentimientos")
                    sentiments_df = pd.DataFrame(sentiments)
                    sentiments_df = sentiments_df.rename(columns={
                        'mensaje': 'Mensaje',
                        'sentimiento': 'Sentimiento',
                        'confianza': 'Confianza',
                        'razon': 'Razón'
                    })
                    
                    def color_sentimiento(row):
                        if row['Sentimiento'] == 'positivo':
                            return ['background-color: #90EE90'] * len(row)
                        elif row['Sentimiento'] == 'negativo':
                            return ['background-color: #FFB6C6'] * len(row)
                        else:
                            return ['background-color: #FFFACD'] * len(row)
                    
                    st.dataframe(sentiments_df.style.apply(color_sentimiento, axis=1), 
                               use_container_width=True, hide_index=True)
                    
            except ImportError as e:
                st.error(f"❌ Error: El módulo sentiment_analyzer no está disponible")
            except Exception as e:
                st.error(f"❌ Error durante análisis: {str(e)}")
                st.warning("Verifica que tu API key de OpenAI esté configurada en secretos")
        else:
            st.info("Haz clic en el botón 🚀 para iniciar el análisis automático de sentimientos")
            
            st.markdown("#### 📊 Estadísticas de Mensajes (sin análisis IA aún)")
            op_stats = get_sentiment_stats_by_operator()
            cod_stats = get_sentiment_stats_by_codigo()
            
            if op_stats:
                st.markdown("**Por Operador:**")
                op_df = pd.DataFrame([
                    {'Operador': op, 'Total Mensajes': stats['total_mensajes'], 
                     'Únicos': stats['mensajes_unicos']}
                    for op, stats in op_stats.items()
                ]).sort_values('Total Mensajes', ascending=False)
                st.dataframe(op_df, use_container_width=True, hide_index=True)
            
            if cod_stats:
                st.markdown("**Por Código Corto:**")
                cod_df = pd.DataFrame([
                    {'Código': cod, 'Total Mensajes': stats['total_mensajes'], 
                     'Únicos': stats['mensajes_unicos']}
                    for cod, stats in cod_stats.items()
                ]).sort_values('Total Mensajes', ascending=False)
                st.dataframe(cod_df, use_container_width=True, hide_index=True)


def render_sidebar():
    """Renderiza la barra lateral con información mejorada."""
    with st.sidebar:
        st.markdown("## ⚙️ CONFIGURACIÓN Y REFERENCIA")
        
        st.markdown("""
        ---
        ### 📊 Acerca de esta Aplicación
        
        **Visualizador interactivo de campañas de comunicación**
        
        Análisis completo de estados e interacciones en canales SMS, WhatsApp e Interacciones de Mensajes.
        
        ---
        """)
        
        st.markdown("### 📈 Características Principales")
        st.markdown("""
        ✅ **SMS** - 315K+ registros analizados
        
        ✅ **WhatsApp** - 1.9K mensajes procesados
        
        ✅ **Interacciones** - 315K+ registros de interacción
        
        ✅ **Diagramas Sankey** - Flujos mejorados
        
        ✅ **Engagement** - Métricas de clicks
        
        ✅ **Data Quality** - Validaciones avanzadas
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas en Caché")
        
        # Botón para limpiar caché
        if st.button("🔄 Recargar Datos (Limpiar Caché)", help="Haz clic para forzar recarga de todos los datos"):
            st.cache_data.clear()
            st.rerun()
        
        try:
            total_sms = count_total_sms_records()
            whatsapp_stats = get_whatsapp_statistics()
            total_inter = count_total_interacciones_records()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📱 SMS", f"{total_sms:,}")
                st.metric("💌 Interacciones", f"{total_inter:,}")
            with col2:
                st.metric("💬 WhatsApp", f"{whatsapp_stats['total']:,}")
            
        except:
            st.info("⏳ Calculando estadísticas...")
        
        st.markdown("---")
        st.markdown("""
        ### 🔑 Diccionario de Colores
        
        **Estados SMS/WhatsApp:**
        - 🟢 Entregado = Éxito
        - 🟡 Procesando = En curso
        - 🔴 Fallido = Error
        - 🟣 Leído = Interacción
        - ⚫ Otros = Casos especiales
        """)
        
        st.markdown("---")
        st.markdown("""
        ### 📝 Notas Técnicas
        
        **Optimizaciones:**
        - Muestreo estadístico (10K registros)
        - Caché de resultados
        - Datos extrapolados
        
        **Fecha:** 2026
        **Sistema:** Cuántico Tecnología
        """)


        st.markdown("---")
        st.markdown('<div style="text-align: center; color: #999; font-size: 0.8rem;"><p>© 2026 Todos los derechos reservados</p></div>', unsafe_allow_html=True)


def main():
    """Función principal."""
    setup_page()
    render_sidebar()
    
    render_header()
    render_sms_section()
    render_whatsapp_section()
    render_interacciones_section()
    
    # Footer
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.85rem; padding: 2rem 0;">
        <p>📊 <strong>Análisis de Campañas de Comunicación</strong></p>
        <p>Estados de Interacción © 2026 | Cuántico Tecnología</p>
        <p style="color: #aaa; margin-top: 0.5rem;">Datos optimizados con muestreo estadístico</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
