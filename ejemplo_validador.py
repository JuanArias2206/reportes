"""
Ejemplo rápido de uso del validador de números colombianos.
"""

from scripts.phone_validator import (
    validar_numero_colombiano,
    validar_lista_numeros,
    analizar_resultados
)

print("=" * 70)
print("🇨🇴 VALIDADOR DE NÚMEROS TELEFÓNICOS COLOMBIA - Ejemplo Rápido")
print("=" * 70)

# ==================== EJEMPLO 1: Validar un número ====================
print("\n📱 EJEMPLO 1: Validar un número individual")
print("-" * 70)

numero = "+57 300 123 4567"
resultado = validar_numero_colombiano(numero)

print(f"Número ingresado: {numero}")
print(f"Número completo:  {resultado['numero_completo']}")
print(f"Válido:           {'✅ Sí' if resultado['valido'] else '❌ No'}")
print(f"Operador:         {resultado['operador']}")
print(f"Categoría:        {resultado['categoria']}")

if resultado['sospechoso']:
    print(f"⚠️  Sospechoso:     {resultado['razon_sospecha']}")

# ==================== EJEMPLO 2: Validar lista ====================
print("\n\n📋 EJEMPLO 2: Validar lista de números")
print("-" * 70)

numeros_test = [
    "+573001234567",     # Tigo - válido
    "3151234567",        # Claro - válido (sin +57)
    "57 310 987 6543",   # Movistar - válido (con espacios)
    "3201112233",        # Claro - válido
    "573501234567",      # Avantel - válido
    "3111111111",        # Movistar - válido pero sospechoso
    "3012121212",        # Tigo - válido pero sospechoso (patrón)
    "573725270507",      # Inválido (prefijo no reconocido)
    "57312345",          # Inválido (muy corto)
    "2123456789",        # Inválido (no es celular)
]

print(f"Validando {len(numeros_test)} números...\n")

df_resultados = validar_lista_numeros(numeros_test)
stats = analizar_resultados(df_resultados)

# Mostrar estadísticas
print("📊 ESTADÍSTICAS GENERALES:")
print(f"   Total:          {stats['total']}")
print(f"   ✅ Válidos:      {stats['validos']} ({stats['porcentaje_validos']}%)")
print(f"   ❌ Inválidos:    {stats['invalidos']} ({stats['porcentaje_invalidos']}%)")
print(f"   ⚠️  Sospechosos:  {stats['sospechosos']}")

print("\n📡 POR OPERADOR:")
for operador, cantidad in sorted(stats['operadores'].items(), 
                                  key=lambda x: x[1], 
                                  reverse=True):
    print(f"   {operador:15} {cantidad:3}")

print("\n🏷️  POR CATEGORÍA:")
for categoria, cantidad in sorted(stats['categorias'].items(), 
                                   key=lambda x: x[1], 
                                   reverse=True):
    print(f"   {categoria:25} {cantidad:3}")

# ==================== EJEMPLO 3: Detalles de cada número ====================
print("\n\n🔍 EJEMPLO 3: Detalles de cada número")
print("-" * 70)

for i, row in df_resultados.iterrows():
    icono = "✅" if row['valido'] else "❌"
    print(f"\n{icono} {row['numero_original']}")
    print(f"   Completo:  {row['numero_completo']}")
    print(f"   Operador:  {row['operador']}")
    print(f"   Categoría: {row['categoria']}")
    
    if row['mensaje_error']:
        print(f"   ⚠️  Error:    {row['mensaje_error']}")
    
    if row['sospechoso']:
        print(f"   🔍 Sospecha:  {row['razon_sospecha']}")

# ==================== EJEMPLO 4: Filtrar solo válidos ====================
print("\n\n✅ EJEMPLO 4: Filtrar solo números válidos")
print("-" * 70)

validos = df_resultados[df_resultados['valido']]
print(f"\nNúmeros válidos ({len(validos)} de {len(df_resultados)}):")

for _, row in validos.iterrows():
    sospecha = " ⚠️" if row['sospechoso'] else ""
    print(f"   {row['numero_completo']:20} {row['operador']:15}{sospecha}")

# ==================== EJEMPLO 5: Identificar problemas ====================
print("\n\n❌ EJEMPLO 5: Identificar números con problemas")
print("-" * 70)

invalidos = df_resultados[~df_resultados['valido']]
print(f"\nNúmeros inválidos ({len(invalidos)} de {len(df_resultados)}):")

for _, row in invalidos.iterrows():
    print(f"   {row['numero_original']:20} → {row['mensaje_error']}")

print("\n" + "=" * 70)
print("✅ EJEMPLOS COMPLETADOS")
print("=" * 70)
print("\nPara ejecutar la aplicación web:")
print("   streamlit run scripts/validador_app.py")
print("\nPara ejecutar todas las pruebas:")
print("   python test_validator.py")
print()
