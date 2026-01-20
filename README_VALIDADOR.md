# 🇨🇴 Validador de Números Telefónicos Colombia

## ⚡ Inicio Rápido

```bash
# 1. Ver ejemplo de uso
python ejemplo_validador.py

# 2. Ejecutar pruebas
python test_validator.py

# 3. Abrir aplicación web
streamlit run scripts/validador_app.py
```

## 📦 Archivos Incluidos

- **`scripts/phone_validator.py`** - Módulo principal de validación
- **`scripts/validador_app.py`** - Aplicación Streamlit interactiva
- **`test_validator.py`** - Suite completa de pruebas
- **`ejemplo_validador.py`** - Ejemplos prácticos de uso
- **`VALIDADOR_NUMEROS.md`** - Documentación completa

## 🚀 Uso Básico

### Validar un número

```python
from scripts.phone_validator import validar_numero_colombiano

resultado = validar_numero_colombiano("+573001234567")

print(resultado['valido'])    # True
print(resultado['operador'])  # "Tigo"
```

### Validar lista de números

```python
from scripts.phone_validator import validar_lista_numeros

numeros = ["3001234567", "3151234567", "2123456789"]
df = validar_lista_numeros(numeros)

print(df[['numero_completo', 'valido', 'operador']])
```

## ✅ Características

- ✅ Limpieza automática de formato
- 📱 Validación de 10 dígitos después de +57
- 🔍 Detección de patrones sospechosos
- 📡 Identificación de operadores (Tigo, Movistar, Claro, etc.)
- 📊 Análisis estadístico completo
- 🔄 Detección de duplicados

## 📡 Operadores Soportados

| Operador | Prefijos |
|----------|----------|
| Tigo | 300-306 |
| Movistar | 310-314, 316-319, 321-323 |
| Claro | 315, 320, 324-325 |
| Avantel | 350-352 |
| ETB | 353-355 |
| WOM | 356-357 |
| Virgin Mobile | 328-329 |
| Éxito Móvil | 358-359 |
| Flash Mobile | 334 |

## 🔍 Patrones Sospechosos Detectados

- Todos los dígitos iguales: `3111111111`
- Termina en muchos ceros: `3001230000`
- Secuencias numéricas: `3012345678`, `3098765432`
- Patrones repetitivos: `3012121212`
- Dígitos consecutivos: `3001111123`

## 📖 Ejemplos

### Válidos
```
+573001234567    ✅ Tigo
3151234567       ✅ Claro (sin +57)
57 320 123 4567  ✅ Claro (con espacios)
```

### Inválidos
```
573725270507   ❌ Prefijo no reconocido
57312345       ❌ Muy corto
2123456789     ❌ No es celular (no empieza con 3)
```

### Válidos pero Sospechosos
```
3111111111     ⚠️ Todos iguales
3012121212     ⚠️ Patrón alternante
3001230000     ⚠️ Termina en muchos ceros
```

## 📊 Resultado de Validación

```python
{
    'numero_original': '+573001234567',
    'numero_limpio': '3001234567',
    'numero_completo': '+573001234567',
    'valido': True,
    'categoria': 'Válido',
    'operador': 'Tigo',
    'mensaje_error': '',
    'sospechoso': False,
    'razon_sospecha': ''
}
```

## 🌐 Aplicación Streamlit

La aplicación web incluye:

1. **Validar Número Individual** - Con detalles técnicos
2. **Validar Lista** - Con estadísticas y gráficos
3. **Documentación** - Reglas y ejemplos completos

## 📘 Documentación Completa

Ver [VALIDADOR_NUMEROS.md](VALIDADOR_NUMEROS.md) para:
- Guía completa de uso
- API detallada
- Casos de prueba
- Personalización
- Integración con otras apps

## 🧪 Pruebas

```bash
# Suite completa
python test_validator.py

# Ejemplo práctico
python ejemplo_validador.py
```

## 📝 Notas

- ⚠️ Solo valida números móviles (comienzan con 3)
- ⚠️ Números sospechosos son válidos pero requieren revisión
- ⚠️ Prefijos pueden cambiar, verificar con MinTIC

## 🤝 Integración

Para integrar con tu app actual:

```python
from scripts.phone_validator import validar_numero_colombiano

# En tu función de análisis
df['validacion'] = df['telefono'].apply(validar_numero_colombiano)
df['operador'] = df['validacion'].apply(lambda x: x['operador'])
```

---

**Desarrollado con Python + Pandas + Streamlit**
