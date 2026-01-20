"""
Aplicación Streamlit para validación de números telefónicos colombianos.
"""

import streamlit as st
import pandas as pd
from phone_validator import (
    validar_numero_colombiano,
    validar_lista_numeros,
    analizar_resultados,
    PREFIJOS_OPERADORES
)

# Configuración de página
st.set_page_config(
    page_title="Validador Números Colombia",
    page_icon="🇨🇴",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #FCD116;
        background: linear-gradient(90deg, #003893 0%, #CE1126 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .valid-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .invalid-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-title"><h1>🇨🇴 Validador de Números Telefónicos Colombia</h1></div>', unsafe_allow_html=True)

# Descripción
st.markdown("""
### Validación Completa de Números Móviles

**Características del Validador:**
- ✅ **Limpieza automática:** Elimina espacios, guiones y caracteres especiales
- 🔢 **Validación de formato:** Verifica longitud y estructura (+57 + 10 dígitos)
- 📱 **Identificación de operador:** Detecta Tigo, Movistar, Claro, Avantel, ETB, WOM y más
- 🔍 **Detección de patrones sospechosos:** Encuentra números con patrones repetitivos
- 📊 **Análisis estadístico:** Genera métricas y reportes completos
- 🔄 **Detección de duplicados:** Identifica números repetidos en la lista
""")

# Crear tabs principales
tab1, tab2, tab3 = st.tabs(["🔍 Validar Número", "📋 Validar Lista", "📘 Documentación"])

# ==================== TAB 1: VALIDAR NÚMERO INDIVIDUAL ====================
with tab1:
    st.subheader("Validar Número Individual")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        numero_input = st.text_input(
            "Ingresa un número telefónico:",
            placeholder="Ejemplo: +573001234567, 3151234567, 57 320 123 4567",
            help="Acepta formato con o sin +57, con o sin espacios/guiones"
        )
    
    if numero_input:
        resultado = validar_numero_colombiano(numero_input)
        
        st.markdown("---")
        
        # Resultado principal
        if resultado['valido']:
            st.markdown(f"""
            <div class="valid-box">
                <h3>✅ Número Válido</h3>
                <p><strong>Número completo:</strong> {resultado['numero_completo']}</p>
                <p><strong>Operador:</strong> {resultado['operador']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if resultado['sospechoso']:
                st.markdown(f"""
                <div class="warning-box">
                    <h4>⚠️ Advertencia: Patrón Sospechoso</h4>
                    <p>{resultado['razon_sospecha']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="invalid-box">
                <h3>❌ Número Inválido</h3>
                <p><strong>Categoría:</strong> {resultado['categoria']}</p>
                <p><strong>Error:</strong> {resultado['mensaje_error']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detalles técnicos
        with st.expander("🔬 Ver Detalles Técnicos"):
            detalles_col1, detalles_col2 = st.columns(2)
            
            with detalles_col1:
                st.write("**Número Original:**", resultado['numero_original'])
                st.write("**Número Limpio:**", resultado['numero_limpio'])
                st.write("**Número Completo:**", resultado['numero_completo'])
            
            with detalles_col2:
                st.write("**Válido:**", "✅ Sí" if resultado['valido'] else "❌ No")
                st.write("**Categoría:**", resultado['categoria'])
                st.write("**Operador:**", resultado['operador'])
            
            if resultado['mensaje_error']:
                st.error(f"**Error:** {resultado['mensaje_error']}")
            
            if resultado['sospechoso']:
                st.warning(f"**Sospechoso:** {resultado['razon_sospecha']}")

# ==================== TAB 2: VALIDAR LISTA ====================
with tab2:
    st.subheader("Validar Lista de Números")
    
    # Opción de entrada
    input_method = st.radio(
        "Método de entrada:",
        ["📝 Pegar lista", "📁 Cargar archivo CSV", "🧪 Usar datos de ejemplo"],
        horizontal=True
    )
    
    numeros_lista = []
    
    if input_method == "📝 Pegar lista":
        texto_numeros = st.text_area(
            "Pega la lista de números (uno por línea):",
            placeholder="573001234567\n3151234567\n+573201234567\n...",
            height=200
        )
        if texto_numeros:
            numeros_lista = [num.strip() for num in texto_numeros.split('\n') if num.strip()]
    
    elif input_method == "📁 Cargar archivo CSV":
        uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'])
        if uploaded_file:
            try:
                df_upload = pd.read_csv(uploaded_file)
                columna = st.selectbox("Selecciona la columna con los números:", df_upload.columns)
                if columna:
                    numeros_lista = df_upload[columna].dropna().astype(str).tolist()
                    st.success(f"✅ {len(numeros_lista)} números cargados")
            except Exception as e:
                st.error(f"Error al leer archivo: {e}")
    
    else:  # Usar datos de ejemplo
        st.info("📌 Usando datos de ejemplo para demostración")
        numeros_lista = [
            "573001234567",      # Válido Tigo
            "3151234567",        # Válido Claro (sin +57)
            "+573201234567",     # Válido Claro (con +57)
            "57 310 123 4567",   # Válido Movistar (con espacios)
            "573111111111",      # Válido pero sospechoso (dígitos repetidos)
            "573501234567",      # Válido Avantel
            "573541234567",      # Válido ETB
            "573561234567",      # Válido WOM
            "573725270507",      # Inválido: prefijo no reconocido
            "57312345",          # Inválido: longitud incorrecta
            "2123456789",        # Inválido: no es celular
            "57300000000",       # Válido pero sospechoso (muchos ceros)
            "3001234567",        # Válido Tigo (sin +57)
            "",                  # Vacío
            "abc123",            # Inválido: caracteres
            "573123456789",      # Válido Movistar
        ]
        st.code('\n'.join(numeros_lista[:5]) + '\n...', language='text')
    
    # Botón de validación
    if st.button("🚀 Validar Lista", type="primary", disabled=len(numeros_lista) == 0):
        with st.spinner('Validando números...'):
            # Validar
            df_resultados = validar_lista_numeros(numeros_lista)
            
            # Analizar
            stats = analizar_resultados(df_resultados)
            
            st.success(f"✅ Validación completada: {stats['total']} números procesados")
            
            st.markdown("---")
            
            # ========== ESTADÍSTICAS GENERALES ==========
            st.subheader("📊 Resumen Estadístico")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("📱 Total", stats['total'])
            with col2:
                st.metric("✅ Válidos", stats['validos'], f"{stats['porcentaje_validos']}%")
            with col3:
                st.metric("❌ Inválidos", stats['invalidos'], f"{stats['porcentaje_invalidos']}%")
            with col4:
                st.metric("⚠️ Sospechosos", stats['sospechosos'])
            with col5:
                st.metric("🔄 Repetidos", stats['numeros_repetidos'])
            
            st.markdown("---")
            
            # ========== GRÁFICOS ==========
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                st.subheader("📡 Distribución por Operador")
                if stats['operadores']:
                    df_operadores = pd.DataFrame(
                        list(stats['operadores'].items()),
                        columns=['Operador', 'Cantidad']
                    ).sort_values('Cantidad', ascending=False)
                    st.bar_chart(df_operadores.set_index('Operador'), use_container_width=True)
                else:
                    st.info("No hay números válidos para mostrar operadores")
            
            with col_graf2:
                st.subheader("🏷️ Distribución por Categoría")
                if stats['categorias']:
                    df_categorias = pd.DataFrame(
                        list(stats['categorias'].items()),
                        columns=['Categoría', 'Cantidad']
                    ).sort_values('Cantidad', ascending=False)
                    st.bar_chart(df_categorias.set_index('Categoría'), use_container_width=True)
            
            # ========== REPETIDOS ==========
            if stats['numeros_repetidos'] > 0:
                st.subheader("🔄 Números Repetidos (Top 10)")
                df_repetidos = pd.DataFrame(
                    list(stats['top_repetidos'].items()),
                    columns=['Número', 'Repeticiones']
                ).sort_values('Repeticiones', ascending=False)
                st.dataframe(df_repetidos, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # ========== RESULTADOS DETALLADOS ==========
            st.subheader("📋 Resultados Detallados")
            
            # Filtros
            col_filtro1, col_filtro2 = st.columns([1, 3])
            
            with col_filtro1:
                filtro = st.selectbox(
                    "Filtrar por:",
                    ["Todos", "Válidos", "Inválidos", "Sospechosos", "Por Operador"]
                )
            
            # Aplicar filtros
            if filtro == "Válidos":
                df_mostrar = df_resultados[df_resultados['valido']].copy()
            elif filtro == "Inválidos":
                df_mostrar = df_resultados[~df_resultados['valido']].copy()
            elif filtro == "Sospechosos":
                df_mostrar = df_resultados[df_resultados['sospechoso']].copy()
            elif filtro == "Por Operador":
                with col_filtro2:
                    operadores_unicos = df_resultados[df_resultados['valido']]['operador'].unique()
                    operador_seleccionado = st.selectbox("Selecciona operador:", operadores_unicos)
                    df_mostrar = df_resultados[df_resultados['operador'] == operador_seleccionado].copy()
            else:
                df_mostrar = df_resultados.copy()
            
            # Mostrar tabla
            st.dataframe(
                df_mostrar[[
                    'numero_original', 'numero_completo', 'valido', 'categoria',
                    'operador', 'sospechoso', 'mensaje_error', 'razon_sospecha'
                ]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "valido": st.column_config.CheckboxColumn("Válido"),
                    "sospechoso": st.column_config.CheckboxColumn("Sospechoso"),
                }
            )
            
            st.caption(f"Mostrando {len(df_mostrar)} de {len(df_resultados)} números")
            
            # ========== DESCARGAS ==========
            st.markdown("---")
            st.subheader("📥 Descargar Resultados")
            
            col_desc1, col_desc2 = st.columns(2)
            
            with col_desc1:
                # CSV completo
                csv_completo = df_resultados.to_csv(index=False)
                st.download_button(
                    "📄 Descargar Resultados Completos (CSV)",
                    csv_completo,
                    "validacion_completa.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col_desc2:
                # CSV solo válidos
                csv_validos = df_resultados[df_resultados['valido']].to_csv(index=False)
                st.download_button(
                    "✅ Descargar Solo Números Válidos (CSV)",
                    csv_validos,
                    "numeros_validos.csv",
                    "text/csv",
                    use_container_width=True
                )

# ==================== TAB 3: DOCUMENTACIÓN ====================
with tab3:
    st.subheader("📘 Documentación del Validador")
    
    st.markdown("""
    ## Reglas de Validación
    
    ### 1. Formato Válido
    Un número colombiano válido debe cumplir:
    - **Longitud:** 10 dígitos (sin contar el +57)
    - **Prefijo país:** Opcional +57 o 57
    - **Primer dígito:** Debe ser 3 (números móviles/celulares)
    - **Prefijo operador:** Debe corresponder a un operador válido
    
    ### 2. Prefijos por Operador
    """)
    
    # Mostrar tabla de operadores
    operadores_info = []
    for operador, rangos in PREFIJOS_OPERADORES.items():
        rangos_str = ', '.join([f"{inicio}-{fin}" if inicio != fin else str(inicio) for inicio, fin in rangos])
        operadores_info.append({
            'Operador': operador,
            'Prefijos': rangos_str
        })
    
    df_operadores_doc = pd.DataFrame(operadores_info)
    st.dataframe(df_operadores_doc, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 3. Patrones Sospechosos
    
    El validador detecta números que, aunque válidos en formato, pueden ser sospechosos:
    
    - **Todos dígitos iguales:** 3111111111
    - **Termina en muchos ceros:** 3001230000
    - **Secuencias ascendentes:** 3012345678
    - **Secuencias descendentes:** 3098765432
    - **Dígitos consecutivos repetidos:** 3001111123
    - **Patrones repetitivos:** 3012121212
    
    ### 4. Categorías de Resultado
    
    | Categoría | Descripción |
    |-----------|-------------|
    | **Válido** | Cumple todas las reglas |
    | **Válido (Sospechoso)** | Válido pero con patrón sospechoso |
    | **Vacío** | Número nulo o vacío |
    | **Formato inválido** | Contiene caracteres no numéricos |
    | **Longitud inválida** | No tiene 10 dígitos |
    | **No es celular** | No comienza con 3 |
    | **Prefijo inválido** | Prefijo no corresponde a operador |
    
    ### 5. Ejemplos
    
    ```python
    # Números válidos
    +573001234567  → Tigo
    3151234567     → Claro (sin +57)
    57 320 123-4567 → Claro (con espacios y guiones)
    
    # Números inválidos
    573725270507   → Prefijo 372 no reconocido
    57312345       → Solo 5 dígitos
    2123456789     → Comienza con 2 (no es celular)
    
    # Válidos pero sospechosos
    3111111111     → Todos los dígitos iguales
    3001230000     → Termina en muchos ceros
    ```
    
    ### 6. Uso Programático
    
    ```python
    from phone_validator import validar_numero_colombiano, validar_lista_numeros
    
    # Validar un número
    resultado = validar_numero_colombiano("+573001234567")
    print(resultado['valido'])    # True
    print(resultado['operador'])  # Tigo
    
    # Validar lista
    numeros = ["3001234567", "3151234567", "3725270507"]
    df = validar_lista_numeros(numeros)
    print(df[['numero_completo', 'valido', 'operador']])
    ```
    """)
    
    st.markdown("---")
    st.info("💡 **Nota:** Este validador usa las reglas actuales de numeración móvil en Colombia. Los prefijos pueden cambiar con el tiempo.")

# Pie de página
st.markdown("---")
st.caption("🇨🇴 Validador de Números Telefónicos Colombia | Desarrollado con Python y Streamlit")
