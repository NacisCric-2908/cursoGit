# Guía Rápida de Git 🚀

## 🔧 **Configuración Inicial**
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
git config --global core.editor "code --wait"  # VS Code como editor
git config --list  # Ver configuración
```

## 📁 **Iniciar/Clonar Repositorio**
```bash
git init                    # Iniciar repo local
git clone <url>            # Clonar repo remoto
git clone <url> <nombre>   # Clonar con nombre personalizado
```

## 💾 **Cambios Básicos**
```bash
git status                 # Ver estado de archivos
git add <archivo>         # Agregar archivo específico
git add .                 # Agregar todos los archivos
git commit -m "mensaje"   # Commit con mensaje
git commit -am "mensaje"  # Add + commit (solo archivos trackeados)
```

## 🌿 **Ramas (Branches)**
```bash
git branch                # Listar ramas locales
git branch -a            # Listar todas las ramas (locales + remotas)
git branch <nombre>      # Crear nueva rama
git checkout <rama>      # Cambiar de rama
git checkout -b <rama>   # Crear y cambiar a nueva rama
git merge <rama>        # Fusionar rama a la actual
git branch -d <rama>    # Eliminar rama
```

## 📤 **Remotos**
```bash
git remote -v            # Ver repositorios remotos
git remote add origin <url>  # Agregar remoto
git push -u origin <rama>    # Subir rama y establecer upstream
git push                 # Subir cambios
git pull                 # Traer y fusionar cambios
git fetch                # Traer cambios sin fusionar
```

## 🔄 **Sincronización**
```bash
git push origin <rama>   # Subir rama específica
git pull origin <rama>   # Traer rama específica
git fetch origin         # Traer todos los cambios
```

## 📜 **Historial**
```bash
git log                  # Ver historial completo
git log --oneline       # Historial resumido
git log --graph         # Historial con árbol
git diff                # Cambios sin stage
git diff --staged      # Cambios en stage
git show <commit>      # Ver cambios de un commit
```

## 🧹 **Deshacer Cambios**
```bash
git restore <archivo>           # Descartar cambios sin stage
git restore --staged <archivo>  # Quitar archivo del stage
git reset --soft HEAD~1        # Deshacer commit manteniendo cambios
git reset --hard HEAD~1        # Deshacer commit y eliminar cambios
git revert <commit>            # Nuevo commit que revierte cambios
```

## 📦 **Stash (Guardado Temporal)**
```bash
git stash               # Guardar cambios temporalmente
git stash list         # Ver lista de stashes
git stash pop          # Recuperar y eliminar último stash
git stash apply        # Recuperar sin eliminar
git stash drop         # Eliminar stash
```

## 🏷️ **Tags**
```bash
git tag                 # Listar tags
git tag <nombre>       # Crear tag ligero
git tag -a <nombre> -m "mensaje"  # Tag anotado
git push origin <tag>  # Subir tag específico
git push --tags        # Subir todos los tags
```

## 🚨 **Casos Comunes**

### **Subir cambios por primera vez:**
```bash
git init
git add .
git commit -m "primer commit"
git remote add origin <url>
git push -u origin main
```

### **Actualizar repo local:**
```bash
git pull origin main
```

### **Crear feature branch:**
```bash
git checkout -b feature/nueva
# hacer cambios
git add .
git commit -m "nueva funcionalidad"
git push origin feature/nueva
```

## 💡 **Tips Rápidos**
- `git help <comando>` - Ayuda sobre comando
- `git log --oneline --graph --all` - Ver historial completo bonito
- `.gitignore` - Archivo para ignorar archivos/carpetas
- `git commit --amend` - Modificar último commit
- `git reset HEAD~1` - Deshacer último commit (manteniendo cambios)

## 🎯 **Flujo de Trabajo Típico**
```bash
# 1. Actualizar
git pull origin main

# 2. Crear rama
git checkout -b mi-rama

# 3. Hacer cambios y commit
git add .
git commit -m "descripción"

# 4. Subir rama
git push origin mi-rama

# 5. (En GitHub/GitLab) Crear Pull Request
```

---

✨ *Esta guía cubre los comandos más utilizados de Git. ¡Perfecta para tener como referencia rápida!* ✨
