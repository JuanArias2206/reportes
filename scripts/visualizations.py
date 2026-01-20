"""
Módulo para crear visualizaciones y gráficos.
Incluye Sankey, gráficos de barras, estadísticas, etc.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
import streamlit as st
from config import COLORS


def create_sankey_diagram(source: List, target: List, value: List, title: str = "") -> go.Figure:
    """Crea un diagrama de Sankey mejorado para visualizar flujos de estados."""
    if not source or not target or not value:
        return go.Figure().add_annotation(text="No hay datos para visualizar")
    
    # Obtener todos los nodos únicos
    all_nodes = list(set(source + target))
    
    # Separar nodos en origen y destino para mejor organización
    source_nodes = list(set(source))
    target_nodes = list(set(target))
    
    # Organizar nodos: primero origen (izquierda), luego destino (derecha)
    nodes = []
    node_positions_x = []
    node_positions_y = []
    
    # Nodos de origen a la izquierda (x=0.001)
    for i, node in enumerate(source_nodes):
        nodes.append(node)
        node_positions_x.append(0.001)
        node_positions_y.append(0.5)  # Centrado verticalmente
    
    # Nodos de destino a la derecha (x=0.999)
    # Ordenar por importancia: Delivered, Failed, Read, Processing, otros
    priority_order = ['Delivered', 'Entregado', 'Failed', 'Fallido', 
                      'Read', 'Leído', 'Processing', 'Procesando', 'ProcEnviados']
    
    def get_priority(node):
        for idx, keyword in enumerate(priority_order):
            if keyword in str(node):
                return idx
        return len(priority_order)
    
    sorted_targets = sorted(target_nodes, key=get_priority)
    
    # Distribuir nodos de destino verticalmente
    for i, node in enumerate(sorted_targets):
        if node not in nodes:  # Evitar duplicados
            nodes.append(node)
            node_positions_x.append(0.999)
            # Distribuir uniformemente entre 0.1 y 0.9
            y_pos = 0.1 + (i / max(len(sorted_targets) - 1, 1)) * 0.8
            node_positions_y.append(y_pos)
    
    # Colores mejorados para nodos según estado
    node_colors = []
    for node in nodes:
        node_str = str(node).lower()
        if "enviado" in node_str and ("inicio" in node_str or "origen" in node_str):
            node_colors.append("#2196F3")  # Azul sólido (origen)
        elif "delivered" in node_str or "entregado" in node_str:
            node_colors.append("#4CAF50")  # Verde sólido
        elif "read" in node_str or "leído" in node_str:
            node_colors.append("#9C27B0")  # Violeta sólido
        elif "failed" in node_str or "fallido" in node_str:
            node_colors.append("#F44336")  # Rojo sólido
        elif "processing" in node_str or "procesando" in node_str or "procenviados" in node_str:
            node_colors.append("#FF9800")  # Naranja sólido
        elif "negro" in node_str or "negra" in node_str:
            node_colors.append("#3F51B5")  # Indigo sólido
        else:
            node_colors.append("#9E9E9E")  # Gris sólido
    
    # Crear índices de source/target
    source_idx = [nodes.index(s) for s in source]
    target_idx = [nodes.index(t) for t in target]
    
    # Colores de links según el destino (más transparentes)
    link_colors = []
    for s, t in zip(source, target):
        t_str = str(t).lower()
        if "delivered" in t_str or "entregado" in t_str:
            link_colors.append("rgba(76, 175, 80, 0.25)")
        elif "failed" in t_str or "fallido" in t_str:
            link_colors.append("rgba(244, 67, 54, 0.25)")
        elif "read" in t_str or "leído" in t_str:
            link_colors.append("rgba(156, 39, 176, 0.25)")
        elif "processing" in t_str or "procesando" in t_str:
            link_colors.append("rgba(255, 152, 0, 0.25)")
        else:
            link_colors.append("rgba(158, 158, 158, 0.2)")
    
    # Crear labels con valores para mejor legibilidad
    node_labels = []
    node_values = {}
    
    # Calcular valores totales por nodo
    for s, t, v in zip(source, target, value):
        if s not in node_values:
            node_values[s] = 0
        if t not in node_values:
            node_values[t] = 0
        node_values[s] += v
        node_values[t] += v
    
    # Crear labels con nombre y valor
    for node in nodes:
        val = node_values.get(node, 0) // 2  # Dividir por 2 porque se cuenta entrada y salida
        node_labels.append(f"{node}\n({val:,})")
    
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=40,
            thickness=20,
            line=dict(color="white", width=2),
            label=node_labels,
            color=node_colors,
            x=node_positions_x,
            y=node_positions_y,
            hovertemplate='<b>%{label}</b><extra></extra>',
        ),
        link=dict(
            source=source_idx,
            target=target_idx,
            value=value,
            color=link_colors,
            hovertemplate='<b>%{source.label}</b> → <b>%{target.label}</b><br>Cantidad: %{value:,.0f}<extra></extra>',
        ),
        textfont=dict(color="#000000", size=14, family="Arial Black"),
    )])
    
    fig.update_layout(
        title={
            "text": f"<b>{title or 'Flujo de Estados'}</b>",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "color": "#1f77b4", "family": "Arial"}
        },
        font=dict(size=14, family="Arial", color="#000000"),
        height=500,
        paper_bgcolor="rgba(255, 255, 255, 1)",
        plot_bgcolor="rgba(255, 255, 255, 1)",
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode="closest",
    )
    
    return fig



def create_status_bar_chart(data: Dict[str, int], title: str = "") -> go.Figure:
    """Crea un gráfico de barras con estados y sus conteos."""
    if not data:
        return go.Figure().add_annotation(text="No hay datos disponibles")
    
    df = pd.DataFrame(list(data.items()), columns=["Estado", "Cantidad"])
    df["Color"] = df["Estado"].map(lambda x: COLORS.get(x, "#808080"))
    
    fig = px.bar(
        df,
        x="Estado",
        y="Cantidad",
        color="Estado",
        color_discrete_map={row["Estado"]: row["Color"] for _, row in df.iterrows()},
        title=title or "Distribución de Estados",
        labels={"Cantidad": "Cantidad de Mensajes", "Estado": "Estado"},
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor="rgba(240, 240, 240, 1)",
        plot_bgcolor="rgba(240, 240, 240, 1)",
    )
    
    return fig


def create_pie_chart(data: Dict[str, int], title: str = "") -> go.Figure:
    """Crea un gráfico de pastel con distribución de estados."""
    if not data:
        return go.Figure().add_annotation(text="No hay datos disponibles")
    
    labels = list(data.keys())
    values = list(data.values())
    colors = [COLORS.get(label, "#808080") for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textposition="inside",
        textinfo="label+percent",
    )])
    
    fig.update_layout(
        title=title or "Distribución de Estados",
        height=500,
        paper_bgcolor="rgba(240, 240, 240, 1)",
    )
    
    return fig


def create_time_series_chart(df: pd.DataFrame, date_col: str, title: str = "") -> go.Figure:
    """Crea un gráfico de serie temporal."""
    if df.empty or date_col not in df.columns:
        return go.Figure().add_annotation(text="No hay datos disponibles")
    
    df_time = df.copy()
    df_time[date_col] = pd.to_datetime(df_time[date_col], errors="coerce")
    df_time = df_time.dropna(subset=[date_col]).sort_values(date_col)
    
    if df_time.empty:
        return go.Figure().add_annotation(text="No hay datos válidos")
    
    daily_counts = df_time.groupby(df_time[date_col].dt.date).size()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_counts.index,
        y=daily_counts.values,
        mode='lines+markers',
        name='Mensajes',
        line=dict(color="#2196F3", width=2),
        marker=dict(size=6),
    ))
    
    fig.update_layout(
        title=title or "Mensajes por Fecha",
        xaxis_title="Fecha",
        yaxis_title="Cantidad de Mensajes",
        height=400,
        paper_bgcolor="rgba(240, 240, 240, 1)",
        plot_bgcolor="rgba(240, 240, 240, 1)",
    )
    
    return fig


def create_statistics_cards(title: str, total: int, stats: Dict[str, int]) -> None:
    """Muestra tarjetas de estadísticas en Streamlit."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Mensajes", f"{total:,}")
    
    cols = [col2, col3, col4]
    for idx, (state, count) in enumerate(stats.items()):
        if idx < len(cols):
            with cols[idx]:
                percentage = (count / total * 100) if total > 0 else 0
                st.metric(state, f"{count:,}", f"{percentage:.1f}%")


def create_comparison_chart(sms_stats: Dict, whatsapp_stats: Dict) -> go.Figure:
    """Crea un gráfico comparativo entre SMS y WhatsApp."""
    all_states = set(sms_stats.get("states", {}).keys()) | set(whatsapp_stats.get("states", {}).keys())
    
    data = {
        "Estado": list(all_states),
        "SMS": [sms_stats.get("states", {}).get(s, 0) for s in all_states],
        "WhatsApp": [whatsapp_stats.get("states", {}).get(s, 0) for s in all_states],
    }
    
    df = pd.DataFrame(data)
    
    fig = go.Figure(data=[
        go.Bar(name="SMS", x=df["Estado"], y=df["SMS"], marker_color="#2196F3"),
        go.Bar(name="WhatsApp", x=df["Estado"], y=df["WhatsApp"], marker_color="#4CAF50"),
    ])
    
    fig.update_layout(
        title="Comparativa: SMS vs WhatsApp",
        barmode="group",
        height=400,
        paper_bgcolor="rgba(240, 240, 240, 1)",
        plot_bgcolor="rgba(240, 240, 240, 1)",
    )
    
    return fig

# ========== NUEVAS VISUALIZACIONES MEJORADAS ==========

def create_horizontal_bar_chart(data: Dict[str, int], title: str = "") -> go.Figure:
    """Crea un gráfico de barras horizontales (mejor para textos largos)."""
    if not data:
        return go.Figure().add_annotation(text="No hay datos disponibles")
    
    # Ordenar datos y crear DataFrame
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_data, columns=["Categoría", "Cantidad"])
    
    # Calcular altura dinámica basada en número de items
    min_height = 300
    height = max(min_height, len(df) * 35 + 150)
    
    # Crear gráfico con Plotly
    fig = go.Figure(data=[
        go.Bar(
            y=df["Categoría"],
            x=df["Cantidad"],
            orientation="h",
            marker=dict(
                color=df["Cantidad"],
                colorscale="Viridis",
                showscale=False,
                line=dict(color="rgba(100,100,100,0.3)", width=1),
            ),
            text=df["Cantidad"],
            textposition="auto",
            hovertemplate='<b>%{y}</b><br>Cantidad: %{x:,}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title={
            "text": title or "Distribución",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 14, "color": "#1f77b4", "family": "Arial"}
        },
        xaxis_title="Cantidad",
        yaxis_title="",
        height=height,
        paper_bgcolor="rgba(250, 250, 250, 1)",
        plot_bgcolor="rgba(245, 245, 245, 1)",
        showlegend=False,
        margin=dict(l=180, r=20, t=60, b=20),
        font=dict(size=11, family="Arial", color="#333"),
        hovermode="closest",
    )
    
    fig.update_yaxes(tickfont=dict(size=10))
    fig.update_xaxes(tickfont=dict(size=10))
    
    return fig


def create_donut_chart(data: Dict[str, int], title: str = "") -> go.Figure:
    """Crea un gráfico de donut (dona) mejorado."""
    if not data:
        return go.Figure().add_annotation(text="No hay datos disponibles")
    
    labels = list(data.keys())
    values = list(data.values())
    colors = [COLORS.get(label, f"rgba({hash(label) % 256}, {hash(label) % 256 // 2}, {hash(label) % 256 // 3}, 0.8)") 
              for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color="#fff", width=3)),
        textposition="auto",
        textinfo="label+percent+value",
        hole=0.4,
        hovertemplate='<b>%{label}</b><br>Cantidad: %{value:,}<br>Porcentaje: %{percent}<extra></extra>',
    )])
    
    fig.update_layout(
        title=title or "Distribución",
        height=500,
        paper_bgcolor="rgba(240, 240, 240, 1)",
        font=dict(size=11),
    )
    
    return fig


def create_stacked_bar_chart(data_dict: Dict[str, Dict[str, int]], title: str = "") -> go.Figure:
    """Crea un gráfico de barras apiladas para múltiples categorías."""
    if not data_dict:
        return go.Figure().add_annotation(text="No hay datos disponibles")
    
    # Convertir datos para plotly
    categories = list(data_dict.keys())
    all_states = set()
    for states in data_dict.values():
        all_states.update(states.keys())
    
    all_states = sorted(list(all_states))
    
    fig = go.Figure()
    
    for state in all_states:
        values = [data_dict[cat].get(state, 0) for cat in categories]
        fig.add_trace(go.Bar(
            name=str(state),
            x=categories,
            y=values,
            hovertemplate='<b>%{x}</b><br>' + state + ': %{y:,}<extra></extra>',
        ))
    
    fig.update_layout(
        barmode="stack",
        title=title or "Distribución Apilada",
        height=500,
        xaxis_title="Categoría",
        yaxis_title="Cantidad",
        paper_bgcolor="rgba(240, 240, 240, 1)",
        plot_bgcolor="rgba(240, 240, 240, 1)",
    )
    
    return fig


def create_metric_cards(metrics: Dict[str, str]) -> None:
    """Muestra tarjetas de métricas en una fila."""
    cols = st.columns(len(metrics))
    for idx, (metric_name, metric_value) in enumerate(metrics.items()):
        with cols[idx]:
            st.metric(metric_name, metric_value)