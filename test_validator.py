"""
Script de prueba para el validador de números telefónicos colombianos.
Ejecutar: python test_validator.py
"""

from scripts.phone_validator import (
    validar_numero_colombiano,
    validar_lista_numeros,
    analizar_resultados,
    limpiar_numero,
    identificar_operador,
    detectar_patron_sospechoso
)

def test_limpieza():
    """Prueba la función de limpieza de números."""
    print("\n" + "="*60)
    print("TEST 1: Limpieza de Números")
    print("="*60)
    
    casos = [
        "+57 300 123 4567",
        "57-300-123-4567",
        "(57) 300 123 4567",
        "300.123.4567",
        "  +57 300 123 4567  ",
    ]
    
    for caso in casos:
        limpio = limpiar_numero(caso)
        print(f"Original: '{caso}' → Limpio: '{limpio}'")

def test_identificacion_operador():
    """Prueba la identificación de operadores."""
    print("\n" + "="*60)
    print("TEST 2: Identificación de Operadores")
    print("="*60)
    
    casos = [
        ("3001234567", "Tigo"),
        ("3101234567", "Movistar"),
        ("3151234567", "Claro"),
        ("3201234567", "Claro"),
        ("3501234567", "Avantel"),
        ("3541234567", "ETB"),
        ("3561234567", "WOM"),
        ("3281234567", "Virgin Mobile"),
        ("3725270507", "Desconocido"),
    ]
    
    for numero, esperado in casos:
        operador = identificar_operador(numero)
        resultado = "✅" if operador == esperado else "❌"
        print(f"{resultado} {numero} → {operador} (esperado: {esperado})")

def test_patrones_sospechosos():
    """Prueba la detección de patrones sospechosos."""
    print("\n" + "="*60)
    print("TEST 3: Detección de Patrones Sospechosos")
    print("="*60)
    
    casos = [
        ("3001234567", False),  # Normal
        ("3111111111", True),   # Todos iguales
        ("3001230000", True),   # Muchos ceros
        ("3012345678", True),   # Secuencia ascendente
        ("3098765432", True),   # Secuencia descendente
        ("3001111123", True),   # Dígitos consecutivos
        ("3012121212", True),   # Patrón repetitivo
    ]
    
    for numero, esperado_sospechoso in casos:
        sospechoso, razon = detectar_patron_sospechoso(numero)
        resultado = "✅" if sospechoso == esperado_sospechoso else "❌"
        print(f"{resultado} {numero} → Sospechoso: {sospechoso}")
        if sospechoso:
            print(f"    Razón: {razon}")

def test_validacion_completa():
    """Prueba la validación completa de números."""
    print("\n" + "="*60)
    print("TEST 4: Validación Completa")
    print("="*60)
    
    casos = [
        # (número, debe_ser_valido, categoria_esperada)
        ("573001234567", True, "Válido"),
        ("+573151234567", True, "Válido"),
        ("3201234567", True, "Válido"),
        ("57 310 123 4567", True, "Válido"),
        ("3111111111", True, "Válido (Sospechoso)"),
        ("573725270507", False, "Prefijo inválido"),
        ("57312345", False, "Longitud inválida"),
        ("2123456789", False, "No es celular"),
        ("", False, "Vacío"),
        ("abc123", False, "Formato inválido"),
    ]
    
    for numero, esperado_valido, categoria in casos:
        resultado = validar_numero_colombiano(numero)
        check = "✅" if resultado['valido'] == esperado_valido else "❌"
        print(f"\n{check} Número: {numero}")
        print(f"   Válido: {resultado['valido']} (esperado: {esperado_valido})")
        print(f"   Categoría: {resultado['categoria']}")
        print(f"   Operador: {resultado['operador']}")
        if resultado['mensaje_error']:
            print(f"   Error: {resultado['mensaje_error']}")
        if resultado['sospechoso']:
            print(f"   ⚠️ Sospechoso: {resultado['razon_sospecha']}")

def test_validacion_lista():
    """Prueba la validación de una lista completa."""
    print("\n" + "="*60)
    print("TEST 5: Validación de Lista Completa")
    print("="*60)
    
    numeros = [
        "573001234567",      # Válido Tigo
        "3151234567",        # Válido Claro
        "+573201234567",     # Válido Claro
        "57 310 123 4567",   # Válido Movistar
        "573111111111",      # Válido pero sospechoso
        "573501234567",      # Válido Avantel
        "573541234567",      # Válido ETB
        "573561234567",      # Válido WOM
        "573725270507",      # Inválido: prefijo
        "57312345",          # Inválido: longitud
        "2123456789",        # Inválido: no celular
        "",                  # Vacío
        "3001234567",        # Válido Tigo
        "3001234567",        # Duplicado
    ]
    
    df = validar_lista_numeros(numeros)
    stats = analizar_resultados(df)
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total procesados: {stats['total']}")
    print(f"   Válidos: {stats['validos']} ({stats['porcentaje_validos']}%)")
    print(f"   Inválidos: {stats['invalidos']} ({stats['porcentaje_invalidos']}%)")
    print(f"   Sospechosos: {stats['sospechosos']}")
    print(f"   Repetidos: {stats['numeros_repetidos']}")
    
    print(f"\n📡 POR OPERADOR:")
    for operador, cantidad in stats['operadores'].items():
        print(f"   {operador}: {cantidad}")
    
    print(f"\n🏷️ POR CATEGORÍA:")
    for categoria, cantidad in stats['categorias'].items():
        print(f"   {categoria}: {cantidad}")
    
    if stats['top_repetidos']:
        print(f"\n🔄 NÚMEROS REPETIDOS:")
        for numero, veces in stats['top_repetidos'].items():
            print(f"   {numero}: {veces} veces")
    
    print(f"\n📋 MUESTRA DE RESULTADOS:")
    print(df[['numero_original', 'numero_completo', 'valido', 'categoria', 'operador']].head(10).to_string(index=False))

def test_casos_edge():
    """Prueba casos extremos y bordes."""
    print("\n" + "="*60)
    print("TEST 6: Casos Extremos (Edge Cases)")
    print("="*60)
    
    casos = [
        None,                    # None
        "",                      # Vacío
        "   ",                   # Solo espacios
        "57",                    # Solo código país
        "573",                   # Muy corto
        "57300123456789",        # Muy largo
        "++++57300123456",       # Múltiples +
        "57-300-123-45-67",      # Guiones variados
        "057 300 123 4567",      # Con 0 inicial
        "573001234567890",       # Demasiado largo
        "57abc3001234567",       # Letras en medio
        "+57(300)123-4567",      # Formato mixto
    ]
    
    for caso in casos:
        try:
            resultado = validar_numero_colombiano(caso)
            print(f"\n📱 Caso: {repr(caso)}")
            print(f"   Válido: {resultado['valido']}")
            print(f"   Categoría: {resultado['categoria']}")
            if resultado['mensaje_error']:
                print(f"   Error: {resultado['mensaje_error']}")
        except Exception as e:
            print(f"\n❌ Caso: {repr(caso)}")
            print(f"   Error inesperado: {e}")

def main():
    """Ejecuta todos los tests."""
    print("\n" + "🇨🇴"*30)
    print("SUITE DE PRUEBAS: Validador de Números Telefónicos Colombia")
    print("🇨🇴"*30)
    
    test_limpieza()
    test_identificacion_operador()
    test_patrones_sospechosos()
    test_validacion_completa()
    test_validacion_lista()
    test_casos_edge()
    
    print("\n" + "="*60)
    print("✅ SUITE DE PRUEBAS COMPLETADA")
    print("="*60)
    print("\nPara ejecutar la aplicación Streamlit:")
    print("  streamlit run scripts/validador_app.py")
    print("\n")

if __name__ == "__main__":
    main()
