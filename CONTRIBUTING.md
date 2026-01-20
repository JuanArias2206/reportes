# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto! Esta guía te ayudará a empezar.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Pull Requests](#pull-requests)
- [Estilo de Código](#estilo-de-código)
- [Estructura del Proyecto](#estructura-del-proyecto)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta profesional y respetuoso. Al participar, te comprometes a:

- Ser respetuoso y considerado
- Aceptar críticas constructivas
- Enfocarte en lo mejor para la comunidad
- Mostrar empatía hacia otros miembros

## 🚀 Cómo Contribuir

### 1. Fork el Proyecto

```bash
# Hacer fork en GitHub, luego clonar
git clone https://github.com/tu-usuario/reportes-mensajeria.git
cd reportes-mensajeria
```

### 2. Crear una Rama

```bash
git checkout -b feature/nombre-descriptivo
```

Tipos de ramas:
- `feature/` - Nueva funcionalidad
- `fix/` - Corrección de bug
- `docs/` - Documentación
- `refactor/` - Refactorización
- `test/` - Pruebas

### 3. Hacer Cambios

- Escribe código limpio y documentado
- Sigue el estilo del proyecto
- Agrega pruebas si es necesario
- Actualiza la documentación

### 4. Commit

```bash
git add .
git commit -m "tipo: Descripción breve

Descripción más detallada si es necesario"
```

### 5. Push y Pull Request

```bash
git push origin feature/nombre-descriptivo
```

Luego abre un Pull Request en GitHub.

## 🐛 Reportar Bugs

Si encuentras un bug, abre un **issue** con:

### Título
`[BUG] Descripción breve del problema`

### Contenido
```markdown
**Descripción del Bug**
Descripción clara del problema.

**Para Reproducir**
Pasos para reproducir:
1. Ir a '...'
2. Hacer clic en '...'
3. Scroll down to '...'
4. Ver error

**Comportamiento Esperado**
Lo que debería pasar.

**Comportamiento Actual**
Lo que está pasando.

**Screenshots**
Si aplica, agrega screenshots.

**Entorno**
- OS: [e.g. macOS 14.0]
- Python: [e.g. 3.11.5]
- Streamlit: [e.g. 1.28.1]
- Navegador: [e.g. Chrome 120]

**Contexto Adicional**
Cualquier otra información relevante.
```

## 💡 Sugerir Mejoras

Para sugerir una mejora, abre un **issue** con:

### Título
`[FEATURE] Descripción de la mejora`

### Contenido
```markdown
**¿La mejora está relacionada con un problema?**
Descripción clara del problema. Ej: "Siempre me frustra cuando [...]"

**Solución Propuesta**
Descripción clara de lo que quieres que pase.

**Alternativas Consideradas**
Otras soluciones que consideraste.

**Contexto Adicional**
Screenshots, mockups, o ejemplos.
```

## 🔀 Pull Requests

### Checklist

Antes de enviar un PR, verifica:

- [ ] El código sigue el estilo del proyecto
- [ ] Agregaste/actualizaste pruebas si es necesario
- [ ] Todas las pruebas pasan localmente
- [ ] Actualizaste la documentación
- [ ] Los commits tienen mensajes descriptivos
- [ ] No hay archivos innecesarios (archivos temporales, logs, etc.)
- [ ] El PR tiene una descripción clara

### Template de PR

```markdown
## Descripción
Descripción clara de los cambios.

## Tipo de Cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que rompe compatibilidad)
- [ ] Documentación

## ¿Cómo se ha probado?
Describe las pruebas realizadas.

## Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] He realizado auto-review de mi código
- [ ] He comentado mi código donde es necesario
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He agregado pruebas
- [ ] Las pruebas existentes pasan localmente
```

## 🎨 Estilo de Código

### Python

Seguimos [PEP 8](https://pep8.org/) con algunas adaptaciones:

```python
# Importaciones
import os
import sys
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st

from scripts.utils import helper_function

# Constantes
MAX_RECORDS = 10000
DEFAULT_ENCODING = 'utf-8'

# Funciones
def function_name(param1: str, param2: int) -> bool:
    """
    Descripción breve de la función.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ValueError: Si param2 es negativo
    """
    if param2 < 0:
        raise ValueError("param2 debe ser positivo")
    
    # Implementación
    result = some_operation(param1, param2)
    return result

# Clases
class MyClass:
    """Descripción de la clase."""
    
    def __init__(self, name: str):
        """Inicializador."""
        self.name = name
    
    def method(self) -> str:
        """Método de ejemplo."""
        return f"Hello, {self.name}"
```

### Nombres

- **Variables**: `snake_case` - `user_name`, `total_count`
- **Funciones**: `snake_case` - `load_data()`, `process_file()`
- **Clases**: `PascalCase` - `DataLoader`, `PhoneValidator`
- **Constantes**: `UPPER_SNAKE_CASE` - `MAX_SIZE`, `DEFAULT_PATH`

### Comentarios

```python
# Comentario de una línea para explicar algo breve

# Comentario más largo que explica algo complejo
# y requiere múltiples líneas para aclarar
# el propósito o el razonamiento.

"""
Docstring para módulos, clases y funciones.
Explica qué hace, parámetros, retorno, y excepciones.
"""
```

### Organización de Archivos

```python
"""
Docstring del módulo.
Descripción de qué hace este archivo.
"""

# Imports estándar
import os
import sys

# Imports de terceros
import pandas as pd
import streamlit as st

# Imports locales
from scripts.config import CONFIG
from scripts.utils import helper

# Constantes
CONSTANT_VALUE = 100

# Funciones
def main_function():
    """Función principal."""
    pass

# Código principal
if __name__ == "__main__":
    main_function()
```

## 📁 Estructura del Proyecto

```
reportes/
├── scripts/               # Código fuente
│   ├── __init__.py
│   ├── app.py            # App principal
│   ├── config.py         # Configuración
│   ├── data_loader.py    # Carga de datos
│   ├── visualizations.py # Visualizaciones
│   ├── utils.py          # Utilidades
│   └── phone_validator.py # Validador
├── data/                 # Datos (no en repo)
├── tests/                # Pruebas (crear si no existe)
├── docs/                 # Documentación
├── requirements.txt      # Dependencias
├── setup.sh             # Script de setup
└── README.md            # Documentación principal
```

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Todas las pruebas
python test_validator.py

# Prueba específica
python -m pytest tests/test_specific.py

# Con cobertura
python -m pytest --cov=scripts tests/
```

### Escribir Pruebas

```python
import unittest
from scripts.phone_validator import validar_numero_colombiano

class TestPhoneValidator(unittest.TestCase):
    """Pruebas para el validador de teléfonos."""
    
    def test_valid_phone(self):
        """Prueba con número válido."""
        result = validar_numero_colombiano("+573001234567")
        self.assertTrue(result['valido'])
        self.assertEqual(result['operador'], 'Tigo')
    
    def test_invalid_phone(self):
        """Prueba con número inválido."""
        result = validar_numero_colombiano("123")
        self.assertFalse(result['valido'])

if __name__ == '__main__':
    unittest.main()
```

## 📝 Documentación

### Actualizar Docs

Si tus cambios afectan la funcionalidad:

1. Actualiza el README.md
2. Actualiza documentos en `docs/`
3. Agrega ejemplos de uso
4. Actualiza comentarios en el código

### Formato de Documentación

Usa Markdown con:
- Títulos claros
- Ejemplos de código
- Screenshots si es visual
- Links a recursos relacionados

## 🔍 Code Review

Todos los PRs pasan por code review. El reviewer verificará:

- ✅ Código claro y bien documentado
- ✅ Pruebas adecuadas
- ✅ Sin regresiones
- ✅ Siguiendo el estilo del proyecto
- ✅ Documentación actualizada

## 📊 Performance

Si tus cambios afectan el rendimiento:

1. Mide el rendimiento antes y después
2. Documenta las mejoras
3. Considera el uso de memoria
4. Prueba con datasets grandes

## 🔒 Seguridad

- No incluyas credenciales en el código
- No subas datos sensibles
- Usa variables de entorno para secrets
- Valida todas las entradas de usuario

## ❓ Preguntas

Si tienes preguntas:

1. Revisa la documentación existente
2. Busca en issues cerrados
3. Abre un nuevo issue con `[QUESTION]`
4. Pregunta en las discusiones de GitHub

## 🙏 Agradecimientos

¡Gracias por contribuir! Cada contribución, grande o pequeña, es valiosa.

## 📜 Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la misma licencia MIT del proyecto.
