"""
Módulo para validación de números telefónicos de Colombia.
Validación completa de números móviles con detección de operadores y patrones sospechosos.
"""

import re
import pandas as pd
from typing import Dict, List, Tuple
from collections import Counter


# Definición de prefijos válidos por operador (después del +57 y 3)
PREFIJOS_OPERADORES = {
    'Tigo': [
        (300, 306),  # 300-306
    ],
    'Movistar': [
        (310, 314),  # 310-314
        (316, 319),  # 316-319
        (321, 323),  # 321-323
    ],
    'Claro': [
        (315, 315),  # 315
        (320, 320),  # 320
        (324, 325),  # 324-325
    ],
    'Avantel': [
        (350, 352),  # 350-352
    ],
    'ETB': [
        (353, 355),  # 353-355
    ],
    'WOM': [
        (356, 357),  # 356-357
    ],
    'Virgin Mobile': [
        (328, 329),  # 328-329
    ],
    'Éxito Móvil': [
        (358, 359),  # 358-359
    ],
    'Flash Mobile': [
        (334, 334),  # 334
    ],
}


def limpiar_numero(numero: str) -> str:
    """
    Limpia el número telefónico eliminando caracteres no numéricos.
    
    Args:
        numero: Número telefónico a limpiar
        
    Returns:
        Número limpio solo con dígitos
    """
    if pd.isna(numero):
        return ""
    
    # Convertir a string y limpiar
    numero_str = str(numero).strip()
    
    # Eliminar espacios, guiones, paréntesis, puntos
    numero_limpio = re.sub(r'[^\d+]', '', numero_str)
    
    return numero_limpio


def extraer_numero_movil(numero_limpio: str) -> Tuple[str, bool]:
    """
    Extrae el número móvil sin código de país.
    
    Args:
        numero_limpio: Número ya limpio
        
    Returns:
        Tupla (número_sin_codigo, tiene_prefijo_57)
    """
    # Remover el + si existe
    numero_limpio = numero_limpio.replace('+', '')
    
    # Si comienza con 57 (código Colombia), removerlo
    if numero_limpio.startswith('57'):
        return numero_limpio[2:], True
    
    return numero_limpio, False


def identificar_operador(numero_movil: str) -> str:
    """
    Identifica el operador basado en el prefijo del número.
    
    Args:
        numero_movil: Número sin código de país (10 dígitos)
        
    Returns:
        Nombre del operador o 'Desconocido'
    """
    if len(numero_movil) < 3:
        return 'Desconocido'
    
    # Obtener prefijo de 3 dígitos
    try:
        prefijo = int(numero_movil[:3])
    except ValueError:
        return 'Desconocido'
    
    # Buscar en rangos de operadores
    for operador, rangos in PREFIJOS_OPERADORES.items():
        for inicio, fin in rangos:
            if inicio <= prefijo <= fin:
                return operador
    
    return 'Desconocido'


def detectar_patron_sospechoso(numero_movil: str) -> Tuple[bool, str]:
    """
    Detecta si el número tiene patrones sospechosos.
    
    Args:
        numero_movil: Número sin código de país
        
    Returns:
        Tupla (es_sospechoso, razón)
    """
    if not numero_movil:
        return False, ""
    
    # 1. Todos los dígitos iguales
    if len(set(numero_movil)) == 1:
        return True, "Todos los dígitos son iguales"
    
    # 2. Termina en muchos ceros
    if numero_movil.endswith('0000'):
        return True, "Termina en 4 o más ceros"
    
    # 3. Secuencia ascendente/descendente
    if len(numero_movil) >= 5:
        # Secuencia ascendente: 12345, 23456, etc.
        for i in range(len(numero_movil) - 4):
            secuencia = numero_movil[i:i+5]
            if secuencia in '0123456789':
                return True, "Contiene secuencia ascendente"
            if secuencia in '9876543210':
                return True, "Contiene secuencia descendente"
    
    # 4. Demasiados dígitos repetidos consecutivos
    if re.search(r'(\d)\1{4,}', numero_movil):
        return True, "Más de 4 dígitos consecutivos iguales"
    
    # 5. Patrón repetitivo (ABABABAB)
    if len(numero_movil) >= 8:
        # Patrón de 2 dígitos repetidos (ej: 12121212)
        primer_par = numero_movil[:2]
        if numero_movil[:8] == primer_par * 4:
            return True, f"Patrón repetitivo ({primer_par} x 4)"
        
        # Buscar secuencias alternantes dentro del número (mínimo 6 dígitos)
        for i in range(len(numero_movil) - 5):
            segmento = numero_movil[i:i+6]
            # Verificar si es patrón ABABAB
            if (segmento[0] == segmento[2] == segmento[4] and 
                segmento[1] == segmento[3] == segmento[5] and 
                segmento[0] != segmento[1]):
                return True, f"Patrón alternante detectado: {segmento[0]}{segmento[1]} x 3"
    
    return False, ""


def validar_numero_colombiano(numero: str) -> Dict:
    """
    Valida un número telefónico colombiano completo.
    
    Args:
        numero: Número telefónico a validar
        
    Returns:
        Diccionario con resultado de validación:
        - numero_original: número tal como vino
        - numero_limpio: número limpio (sin +57)
        - numero_completo: número con +57
        - valido: True/False
        - categoria: categoría del número
        - operador: operador detectado
        - mensaje_error: mensaje de error si aplica
        - sospechoso: True si tiene patrón sospechoso
        - razon_sospecha: razón si es sospechoso
    """
    resultado = {
        'numero_original': numero,
        'numero_limpio': '',
        'numero_completo': '',
        'valido': False,
        'categoria': 'No procesado',
        'operador': 'N/A',
        'mensaje_error': '',
        'sospechoso': False,
        'razon_sospecha': '',
    }
    
    # 1. Limpiar número
    numero_limpio = limpiar_numero(numero)
    
    if not numero_limpio:
        resultado['categoria'] = 'Vacío'
        resultado['mensaje_error'] = 'Número vacío o nulo'
        return resultado
    
    # 2. Extraer número móvil (sin +57)
    numero_movil, tiene_57 = extraer_numero_movil(numero_limpio)
    resultado['numero_limpio'] = numero_movil
    resultado['numero_completo'] = f'+57{numero_movil}'
    
    # 3. Validar que solo tenga dígitos
    if not numero_movil.isdigit():
        resultado['categoria'] = 'Formato inválido'
        resultado['mensaje_error'] = 'Contiene caracteres no numéricos después de limpiar'
        return resultado
    
    # 4. Validar longitud (debe ser 10 dígitos)
    if len(numero_movil) != 10:
        resultado['categoria'] = 'Longitud inválida'
        resultado['mensaje_error'] = f'Longitud inválida: {len(numero_movil)} dígitos (esperado: 10)'
        return resultado
    
    # 5. Validar que comience con 3 (celular)
    if not numero_movil.startswith('3'):
        resultado['categoria'] = 'No es celular'
        resultado['mensaje_error'] = 'No comienza con 3 (no es celular)'
        return resultado
    
    # 6. Identificar operador
    operador = identificar_operador(numero_movil)
    resultado['operador'] = operador
    
    if operador == 'Desconocido':
        resultado['categoria'] = 'Prefijo inválido'
        prefijo = numero_movil[:3]
        resultado['mensaje_error'] = f'Prefijo {prefijo} no corresponde a ningún operador colombiano'
        return resultado
    
    # 7. Detectar patrones sospechosos
    es_sospechoso, razon = detectar_patron_sospechoso(numero_movil)
    resultado['sospechoso'] = es_sospechoso
    resultado['razon_sospecha'] = razon
    
    # 8. Si llegó aquí, es válido
    resultado['valido'] = True
    resultado['categoria'] = 'Válido'
    
    if es_sospechoso:
        resultado['categoria'] = 'Válido (Sospechoso)'
    
    return resultado


def validar_lista_numeros(numeros: List[str]) -> pd.DataFrame:
    """
    Valida una lista completa de números y retorna un DataFrame.
    
    Args:
        numeros: Lista de números a validar
        
    Returns:
        DataFrame con resultados de validación
    """
    resultados = []
    
    for numero in numeros:
        resultado = validar_numero_colombiano(numero)
        resultados.append(resultado)
    
    df = pd.DataFrame(resultados)
    
    return df


def analizar_resultados(df_validacion: pd.DataFrame) -> Dict:
    """
    Analiza los resultados de validación y genera estadísticas.
    
    Args:
        df_validacion: DataFrame con resultados de validación
        
    Returns:
        Diccionario con estadísticas
    """
    total = len(df_validacion)
    
    if total == 0:
        return {'total': 0}
    
    validos = df_validacion['valido'].sum()
    invalidos = total - validos
    
    # Contar por categoría
    categorias = df_validacion['categoria'].value_counts().to_dict()
    
    # Contar por operador (solo válidos)
    operadores = df_validacion[df_validacion['valido']]['operador'].value_counts().to_dict()
    
    # Contar sospechosos
    sospechosos = df_validacion['sospechoso'].sum()
    
    # Detectar repetidos
    numeros_limpios = df_validacion['numero_limpio'].dropna()
    repeticiones = Counter(numeros_limpios)
    numeros_repetidos = {num: count for num, count in repeticiones.items() if count > 1}
    
    estadisticas = {
        'total': total,
        'validos': int(validos),
        'invalidos': int(invalidos),
        'porcentaje_validos': round(validos / total * 100, 2),
        'porcentaje_invalidos': round(invalidos / total * 100, 2),
        'categorias': categorias,
        'operadores': operadores,
        'sospechosos': int(sospechosos),
        'porcentaje_sospechosos': round(sospechosos / total * 100, 2),
        'numeros_repetidos': len(numeros_repetidos),
        'top_repetidos': dict(sorted(numeros_repetidos.items(), key=lambda x: x[1], reverse=True)[:10]),
    }
    
    return estadisticas


# ==================== EJEMPLO DE USO CON STREAMLIT ====================

def ejemplo_streamlit():
    """
    Ejemplo de cómo usar este módulo en Streamlit.
    """
    import streamlit as st
    
    st.title("🇨🇴 Validador de Números Telefónicos Colombia")
    
    st.markdown("""
    ### Validación Completa de Números Móviles
    
    **Características:**
    - ✅ Limpieza automática de formato
    - 📱 Identificación de operador
    - 🔍 Detección de patrones sospechosos
    - 📊 Análisis estadístico completo
    """)
    
    # Opción 1: Entrada manual
    st.subheader("Validar Número Individual")
    numero_input = st.text_input("Ingresa un número:", placeholder="+573001234567")
    
    if numero_input:
        resultado = validar_numero_colombiano(numero_input)
        
        if resultado['valido']:
            st.success(f"✅ Número válido: {resultado['numero_completo']}")
            st.info(f"**Operador:** {resultado['operador']}")
            
            if resultado['sospechoso']:
                st.warning(f"⚠️ Patrón sospechoso: {resultado['razon_sospecha']}")
        else:
            st.error(f"❌ Número inválido")
            st.warning(f"**Categoría:** {resultado['categoria']}")
            st.info(f"**Error:** {resultado['mensaje_error']}")
    
    st.markdown("---")
    
    # Opción 2: Carga de archivo
    st.subheader("Validar Lista de Números")
    
    # Crear lista de ejemplo
    numeros_ejemplo = [
        "573001234567",  # Válido Tigo
        "3151234567",    # Válido Claro (sin +57)
        "+573201234567", # Válido Claro
        "573111111111",  # Válido Movistar pero sospechoso
        "573725270507",  # Prefijo inválido
        "57312345",      # Longitud inválida
        "573501234567",  # Válido Avantel
        "2123456789",    # No es celular
    ]
    
    if st.button("🔍 Validar Números de Ejemplo"):
        # Validar
        df_resultados = validar_lista_numeros(numeros_ejemplo)
        
        # Mostrar estadísticas
        stats = analizar_resultados(df_resultados)
        
        st.subheader("📊 Estadísticas")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total", stats['total'])
        with col2:
            st.metric("Válidos", stats['validos'], f"{stats['porcentaje_validos']}%")
        with col3:
            st.metric("Inválidos", stats['invalidos'], f"{stats['porcentaje_invalidos']}%")
        with col4:
            st.metric("Sospechosos", stats['sospechosos'])
        
        # Mostrar por operador
        if stats['operadores']:
            st.subheader("📡 Distribución por Operador")
            st.bar_chart(stats['operadores'])
        
        # Mostrar por categoría
        st.subheader("🏷️ Distribución por Categoría")
        st.bar_chart(stats['categorias'])
        
        # Mostrar resultados detallados
        st.subheader("📋 Resultados Detallados")
        
        # Filtros
        filtro = st.selectbox("Filtrar por:", ["Todos", "Válidos", "Inválidos", "Sospechosos"])
        
        if filtro == "Válidos":
            df_mostrar = df_resultados[df_resultados['valido']]
        elif filtro == "Inválidos":
            df_mostrar = df_resultados[~df_resultados['valido']]
        elif filtro == "Sospechosos":
            df_mostrar = df_resultados[df_resultados['sospechoso']]
        else:
            df_mostrar = df_resultados
        
        st.dataframe(
            df_mostrar[['numero_original', 'numero_completo', 'categoria', 
                       'operador', 'mensaje_error', 'razon_sospecha']],
            use_container_width=True,
            hide_index=True
        )
        
        # Opción de descarga
        csv = df_resultados.to_csv(index=False)
        st.download_button(
            "📥 Descargar Resultados CSV",
            csv,
            "validacion_numeros.csv",
            "text/csv",
            key='download-csv'
        )


if __name__ == "__main__":
    # Prueba rápida
    numeros_prueba = [
        "573001234567",
        "+573151234567",
        "3201234567",
        "573111111111",
        "573725270507",
    ]
    
    print("=" * 60)
    print("VALIDADOR DE NÚMEROS TELEFÓNICOS COLOMBIA")
    print("=" * 60)
    
    for numero in numeros_prueba:
        resultado = validar_numero_colombiano(numero)
        print(f"\n📱 {numero}")
        print(f"   Limpio: {resultado['numero_limpio']}")
        print(f"   Válido: {'✅' if resultado['valido'] else '❌'}")
        print(f"   Categoría: {resultado['categoria']}")
        print(f"   Operador: {resultado['operador']}")
        if resultado['mensaje_error']:
            print(f"   Error: {resultado['mensaje_error']}")
        if resultado['sospechoso']:
            print(f"   ⚠️ Sospechoso: {resultado['razon_sospecha']}")
    
    print("\n" + "=" * 60)
    print("\nPara usar en Streamlit, importa y llama a ejemplo_streamlit()")
