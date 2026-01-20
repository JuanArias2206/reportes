# 🚀 Guía para Subir el Proyecto a GitHub

Esta guía te ayudará a subir tu proyecto de análisis de mensajería a GitHub paso a paso.

## 📋 Pre-requisitos

- [x] Tener Git instalado
- [x] Tener cuenta de GitHub
- [ ] Crear repositorio en GitHub (sigue los pasos abajo)

## 🔧 Instalación de Git (si no lo tienes)

### macOS
```bash
# Usando Homebrew
brew install git

# O usando Xcode Command Line Tools
xcode-select --install
```

### Linux
```bash
sudo apt-get install git  # Ubuntu/Debian
sudo yum install git      # CentOS/RHEL
```

### Windows
Descarga desde: https://git-scm.com/download/win

## 📦 Pasos para Subir a GitHub

### 1. Crear Repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en el botón verde "New" o "+"
3. Llena el formulario:
   - **Repository name**: `reportes-mensajeria` (o el que prefieras)
   - **Description**: "Sistema de análisis de mensajería SMS/WhatsApp con validación de números colombianos"
   - **Visibility**: Private (recomendado si tienes datos sensibles) o Public
   - **NO** marques "Initialize this repository with a README" (ya tienes uno)
4. Haz clic en "Create repository"

### 2. Configurar Git Localmente (primera vez)

```bash
# Configurar tu nombre y email (solo una vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# Verificar configuración
git config --global --list
```

### 3. Inicializar Repositorio Local

```bash
# Ve a la carpeta del proyecto
cd /Users/mac/Documents/trabajo/cuantico/reportes

# Inicializar Git (si no está inicializado)
git init

# Verificar archivos que se van a subir
git status
```

### 4. Preparar Archivos

```bash
# Agregar todos los archivos (excepto los del .gitignore)
git add .

# Ver qué archivos se agregarán
git status

# Si quieres ver más detalles
git diff --cached
```

### 5. Hacer el Primer Commit

```bash
# Crear commit con mensaje descriptivo
git commit -m "🎉 Initial commit: Sistema completo de análisis de mensajería

- Aplicación Streamlit con análisis de SMS, WhatsApp e Interacciones
- Validador de números telefónicos colombianos
- Optimizaciones de rendimiento (2-3s de carga)
- Análisis de calidad de datos (DQ)
- Detección de patrones sospechosos
- Documentación completa"
```

### 6. Conectar con GitHub

```bash
# Reemplaza 'tu-usuario' con tu nombre de usuario de GitHub
git remote add origin https://github.com/tu-usuario/reportes-mensajeria.git

# Verificar que se agregó correctamente
git remote -v
```

### 7. Subir los Archivos

```bash
# Primera vez: subir y establecer tracking
git push -u origin main

# Si te pide credenciales, usa tu usuario y Personal Access Token
# (no tu contraseña - GitHub ya no acepta contraseñas)
```

### 8. Configurar Personal Access Token (si es necesario)

Si Git te pide autenticación:

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Selecciona los scopes:
   - `repo` (todos)
   - `workflow` (opcional)
4. Copia el token generado
5. Úsalo como contraseña cuando Git lo pida

## 🔄 Comandos Git para el Día a Día

### Ver Estado
```bash
git status              # Ver archivos modificados
git log --oneline       # Ver historial de commits
git diff               # Ver cambios no committeados
```

### Agregar Cambios
```bash
git add archivo.py          # Agregar archivo específico
git add scripts/            # Agregar carpeta
git add .                   # Agregar todo
git add -p                  # Agregar interactivamente
```

### Hacer Commits
```bash
git commit -m "Mensaje descriptivo"
git commit -am "Mensaje"  # Add + commit de archivos tracked
```

### Subir Cambios
```bash
git push                # Subir commits al remoto
git push origin main    # Especificar branch
```

### Descargar Cambios
```bash
git pull                # Descargar y fusionar cambios
git fetch              # Solo descargar sin fusionar
```

### Ramas (Branches)
```bash
git branch                    # Listar ramas
git branch nombre-rama        # Crear rama
git checkout nombre-rama      # Cambiar a rama
git checkout -b nueva-rama    # Crear y cambiar
git merge otra-rama           # Fusionar rama
```

## 📝 Buenas Prácticas

### Mensajes de Commit

Usa prefijos claros:
```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Cambios en documentación
style: Formato, punto y coma, etc.
refactor: Refactorización de código
test: Agregar pruebas
chore: Mantenimiento
```

Ejemplos:
```bash
git commit -m "feat: Agregar validación de números colombianos"
git commit -m "fix: Corregir error en diagrama Sankey"
git commit -m "docs: Actualizar README con ejemplos"
```

### Commits Frecuentes

- Haz commits pequeños y frecuentes
- Cada commit debe ser una unidad lógica de cambio
- No mezcles múltiples features en un commit

### .gitignore

Asegúrate de que `.gitignore` está configurado:
```bash
# Verificar que está ignorando los archivos correctos
git status --ignored

# Si ves archivos que NO deberían estar (como data/*.csv)
# agrégalos al .gitignore y luego:
git rm --cached archivo-a-ignorar
git commit -m "chore: Actualizar .gitignore"
```

## 🔒 Seguridad y Privacidad

### ⚠️ IMPORTANTE: Datos Sensibles

Antes de hacer push, verifica que NO estés subiendo:
- ❌ Archivos CSV con datos reales (`data/*.csv`)
- ❌ Credenciales o API keys
- ❌ Información personal
- ❌ Archivos grandes innecesarios

```bash
# Ver archivos que se van a subir
git status

# Si encuentras algo que no debería estar:
git reset HEAD archivo.csv          # Quitar del staging
echo "archivo.csv" >> .gitignore    # Agregar al .gitignore
```

### Borrar Archivo que Ya Subiste por Error

```bash
# Borrar del repositorio pero mantener localmente
git rm --cached archivo-sensible.csv
git commit -m "chore: Remover archivo sensible"
git push

# Agregar al .gitignore
echo "archivo-sensible.csv" >> .gitignore
git add .gitignore
git commit -m "chore: Actualizar .gitignore"
git push
```

### Si Ya Subiste Datos Sensibles

Si accidentalmente subiste datos sensibles a GitHub:

1. **Cambiar a Private** el repositorio inmediatamente
2. **Borrar el historial** con git-filter-repo o BFG Repo-Cleaner
3. **Considerar** eliminar y recrear el repositorio

## 🌲 Estructura de Branches Recomendada

```
main (producción)
├── develop (desarrollo)
│   ├── feature/nueva-funcionalidad
│   ├── feature/otro-feature
│   └── hotfix/correccion-urgente
```

```bash
# Crear rama de desarrollo
git checkout -b develop

# Crear feature branch
git checkout -b feature/exportar-excel

# Cuando termines el feature
git checkout develop
git merge feature/exportar-excel
git branch -d feature/exportar-excel

# Subir develop
git push origin develop
```

## 🆘 Comandos de Emergencia

### Deshacer Último Commit (sin perder cambios)
```bash
git reset --soft HEAD~1
```

### Deshacer Cambios en un Archivo
```bash
git checkout -- archivo.py
```

### Volver a un Commit Anterior
```bash
git log --oneline           # Ver commits
git reset --hard abc123     # Volver a commit abc123
```

### Limpiar Archivos No Tracked
```bash
git clean -n    # Ver qué se borraría
git clean -f    # Borrar archivos
git clean -fd   # Borrar archivos y carpetas
```

## 📚 Recursos Adicionales

- **Documentación Git**: https://git-scm.com/doc
- **GitHub Docs**: https://docs.github.com
- **Atlassian Git Tutorial**: https://www.atlassian.com/git/tutorials
- **Oh My Git!** (Juego para aprender): https://ohmygit.org/

## ✅ Checklist Final

Antes de subir a GitHub, verifica:

- [ ] `.gitignore` está configurado correctamente
- [ ] No hay datos sensibles en los archivos
- [ ] README.md está completo y actualizado
- [ ] LICENSE está incluido
- [ ] requirements.txt está actualizado
- [ ] Los archivos grandes están excluidos
- [ ] El código funciona localmente
- [ ] Las pruebas pasan
- [ ] La documentación está al día

## 🎉 ¡Listo!

Tu proyecto debería estar ahora en GitHub. Visita:
```
https://github.com/tu-usuario/reportes-mensajeria
```

Para compartir tu proyecto:
```
git clone https://github.com/tu-usuario/reportes-mensajeria.git
```

---

**¿Necesitas ayuda?** Abre un issue o consulta la documentación de GitHub.
