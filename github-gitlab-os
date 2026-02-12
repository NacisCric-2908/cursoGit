# Guía Rápida de GitHub/GitLab 🚀

## 📦 **Instalación de Herramientas Básicas**

### **Linux (Ubuntu/Debian)**
```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade

# Instalar Git
sudo apt install git

# Instalar herramientas esenciales
sudo apt install man     # Sistema de documentación
sudo apt install less    # Paginador (generalmente ya incluido)
sudo apt install tree    # Visualizar estructura de directorios

# Verificar instalaciones
git --version
man git
less --version
```

### **Linux (Arch/Manjaro)**
```bash
# Actualizar sistema
sudo pacman -Syu

# Instalar Git
sudo pacman -S git

# Instalar herramientas esenciales
sudo pacman -S man-db    # Sistema de documentación
sudo pacman -S less      # Paginador
sudo pacman -S tree      # Visualizar estructura de directorios

# Alternativas desde AUR (usando yay)
yay -S git-man           # Documentación extra de git
yay -S git-docs         # Documentación completa

# Verificar instalaciones
git --version
man git
less --version
```

### **Windows**
```bash
# Descargar Git Bash desde:
# https://git-scm.com/download/win

# Git Bash incluye:
# - Git
# - MINGW (terminal estilo Linux)
# - Less (paginador)
# - Utilidades básicas Unix

# Verificar instalación (en Git Bash)
git --version
less --version
```

## 🔑 **Configuración de LLaves SSH**

### **Linux (Ubuntu/Debian y Arch)**
```bash
# 1. Generar llave SSH (ED25519 recomendado)
ssh-keygen -t ed25519 -C "tu@email.com"
# Presiona Enter para ubicación default (~/.ssh/id_ed25519)
# Opcional: Agregar contraseña

# Alternativa: Usar RSA si hay compatibilidad
ssh-keygen -t rsa -b 4096 -C "tu@email.com"

# 2. Iniciar agente SSH
eval "$(ssh-agent -s)"

# 3. Agregar llave al agente
ssh-add ~/.ssh/id_ed25519

# 4. Ver llave pública
cat ~/.ssh/id_ed25519.pub
# Copiar todo el contenido (empieza con ssh-ed25519)
```

### **Windows (Git Bash)**
```bash
# 1. Generar llave SSH
ssh-keygen -t ed25519 -C "tu@email.com"
# Presiona Enter para ubicación default

# 2. Iniciar agente SSH
eval $(ssh-agent -s)

# 3. Agregar llave al agente
ssh-add ~/.ssh/id_ed25519

# 4. Ver llave pública
cat ~/.ssh/id_ed25519.pub
# Copiar todo el contenido
```

### **Configuración adicional SSH (Linux/Arch)**
```bash
# Crear/editar config file
nano ~/.ssh/config

# Agregar configuración básica
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# Permisos correctos
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

## 🌐 **Agregar SSH a GitHub/GitLab**

### **GitHub**
```
1. Settings → SSH and GPG keys → New SSH key
2. Título: "Mi Laptop" (o nombre descriptivo)
3. Key: Pegar llave pública (cat ~/.ssh/id_ed25519.pub)
4. Add SSH key
```

### **GitLab**
```
1. Preferences → SSH Keys
2. Key: Pegar llave pública
3. Title: "Mi Laptop"
4. Add key
```

### **Probar conexión**
```bash
# GitHub
ssh -T git@github.com
# Output esperado: Hi username! You've successfully authenticated...

# GitLab
ssh -T git@gitlab.com
# Output esperado: Welcome to GitLab, @username!
```

## 📚 **Uso de MAN y LESS**

### **MAN (Manual Pages)**
```bash
# Navegación básica
man git          # Manual completo de git
man git-commit   # Manual específico de commit
man git-add      # Manual de git add
man -k git      # Buscar comandos relacionados con git
man -k ssh      # Buscar comandos relacionados con ssh

# En Arch, documentación extra
man git-checkout # Ya disponible con git
man git-branch

# Atajos en MAN (usa less)
# q = salir
# /palabra = buscar
# n = siguiente resultado
# N = anterior resultado
# g = inicio
# G = final
# h = ayuda de atajos
```

### **LESS (Paginador)**
```bash
# Comandos LESS útiles
git log --oneline | less                    # Paginar commits
git diff | less                            # Paginar diferencias
git help -a | less                        # Paginar ayuda
git status -v | less                      # Paginar status verbose
git show HEAD | less                      # Ver último commit

# Atajos LESS
# Espacio = página siguiente
# b = página anterior
# / = buscar hacia adelante
# ? = buscar hacia atrás
# & = filtrar líneas
# v = editar en $EDITOR
# F = seguir archivo (como tail -f)
# Ctrl+C = cancelar
```

## 🚀 **Comandos GitHub/GitLab Esenciales**

### **Clonar repositorios**
```bash
# Clonar con SSH (recomendado)
git clone git@github.com:usuario/repo.git
git clone git@gitlab.com:usuario/repo.git

# Clonar con HTTPS
git clone https://github.com/usuario/repo.git
git clone https://gitlab.com/usuario/repo.git

# Clonar rama específica
git clone -b develop git@github.com:usuario/repo.git

# Clonar shallow (historial limitado)
git clone --depth 1 git@github.com:usuario/repo.git
```

### **Fork y sincronización**
```bash
# Agregar upstream (fork)
git remote add upstream git@github.com:original/repo.git

# Ver remotos configurados
git remote -v

# Sincronizar fork
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Sincronizar usando rebase
git fetch upstream
git checkout main
git rebase upstream/main
git push origin main --force-with-lease
```

### **Pull Requests/Merge Requests**
```bash
# 1. Crear rama feature
git checkout -b feature/amazing

# 2. Hacer cambios y commit
git add .
git commit -m "feat: add amazing feature"

# 3. Subir rama
git push origin feature/amazing

# 4. En GitHub/GitLab crear PR/MR desde interfaz web

# 5. Si hay cambios solicitados
git add .
git commit -m "fix: review changes"
git push origin feature/amazing

# 6. Después del merge, limpiar
git checkout main
git pull origin main
git branch -d feature/amazing
git push origin --delete feature/amazing
```

## 🛠️ **Configuraciones Útiles**

### **GitHub CLI**
```bash
# Linux (Ubuntu/Debian)
sudo apt install gh

# Linux (Arch/Manjaro)
sudo pacman -S github-cli

# Windows (Git Bash)
winget install --id GitHub.cli

# Autenticar
gh auth login

# Comandos útiles
gh repo create           # Crear repo
gh repo clone usuario/repo  # Clonar repo
gh pr create            # Crear pull request
gh pr list              # Listar pull requests
gh pr checkout 123      # Checkout PR específico
gh issue list           # Ver issues
gh issue create         # Crear issue
gh release list        # Ver releases
```

### **GitLab CLI (glab)**
```bash
# Linux (Ubuntu/Debian)
sudo apt install glab

# Linux (Arch/Manjaro - AUR)
yay -S glab

# Windows (Scoop)
scoop install glab

# Autenticar
glab auth login

# Comandos útiles
glab repo create
glab repo clone usuario/repo
glab mr create          # Merge request
glab mr list           # Listar merge requests
glab mr checkout 123   # Checkout MR específico
glab issue list
glab issue create
glab pipeline list     # Ver pipelines CI/CD
```

## 📋 **Archivo .gitignore Recomendado**

### **Para diferentes lenguajes**
```bash
# Ver plantillas oficiales
gh repo create --help  # Incluye opciones de .gitignore

# O usar comando curl para descargar plantillas
# Python
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Node.js
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

# Java
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Java.gitignore

# Rust
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Rust.gitignore

# Go
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Go.gitignore
```

## 🔍 **Solución de Problemas Comunes**

### **Permiso denegado SSH**
```bash
# Verificar permisos (Linux/Arch)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/config

# Verificar agente SSH
eval "$(ssh-agent -s)"
ssh-add -l  # Listar llaves cargadas
ssh-add ~/.ssh/id_ed25519

# Debug SSH
ssh -vT git@github.com
ssh -vT git@gitlab.com
```

### **Cache de contraseña HTTPS**
```bash
# Cachear contraseña por 1 hora
git config --global credential.helper 'cache --timeout=3600'

# Almacenar contraseña (menos seguro)
git config --global credential.helper store

# En Windows (Git Credential Manager)
git config --global credential.helper manager-core
```

### **Problemas comunes en Arch**
```bash
# SSH agent no persiste
systemctl --user enable ssh-agent
systemctl --user start ssh-agent

# Agregar al ~/.bashrc o ~/.zshrc
if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    eval $(ssh-agent -s) > /dev/null
fi

# Git no encuentra man pages
sudo pacman -S git-man
```

## 🎯 **Flujo de Trabajo Completo**

```bash
# 1. Configurar entorno global
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

# 2. Verificar SSH
ssh -T git@github.com  # o git@gitlab.com

# 3. Clonar/crear repo
git clone git@github.com:usuario/proyecto.git
cd proyecto

# 4. Crear rama feature
git checkout -b feature/nueva

# 5. Trabajar y commit (con buenas prácticas)
git add .
git commit -m "feat: agregar funcionalidad X"
git commit -m "fix: corregir bug en Y"
git commit -m "docs: actualizar README"

# 6. Mantener rama actualizada
git fetch origin
git rebase origin/main  # o git merge origin/main

# 7. Subir cambios
git push origin feature/nueva

# 8. Crear Pull/Merge Request
# Interfaz web: New pull request → Create
# O con CLI:
gh pr create --title "Feature nueva" --body "Descripción"
glab mr create --title "Feature nueva" --description "Descripción"

# 9. Actualizar después de merge
git checkout main
git pull origin main
git branch -d feature/nueva
git push origin --delete feature/nueva
```

## 📖 **Documentación MAN para Git**

```bash
# Ver toda la documentación git offline
man git
man gittutorial  # Tutorial interactivo
man gitworkflows # Flujos de trabajo

# Comandos específicos con ejemplos
man git-add
man git-commit
man git-push
man git-pull
man git-merge
man git-rebase
man git-reset
man git-revert

# Buscar comandos relacionados
man -k git | grep branch
man -k git | grep remote
man -k git | grep log

# En Arch, documentación adicional
man git-credential
man git-http-backend
man git-merge-tree
```

## 🐧 **Comandos específicos para Arch**

### **Manejo de paquetes relacionados con Git**
```bash
# Buscar paquetes relacionados
pacman -Ss git
pacman -Ss github
pacman -Ss gitlab

# Instalar herramientas adicionales
sudo pacman -S git-lfs        # Git Large File Storage
sudo pacman -S git-crypt      # Encriptación para repos
sudo pacman -S git-flow       # Git Flow branching model
sudo pacman -S tig           # Visor interactivo de git
sudo pacman -S meld          # Herramienta de diff

# Desde AUR
yay -S git-extras           # Comandos extra de git
yay -S git-absorb          # Absorber fixups automáticamente
yay -S git-interactive-rebase-tool  # Herramienta TUI para rebase
```

### **Configuración específica para Arch**
```bash
# Alias útiles para Arch
git config --global alias.pacman "!git log --grep='pacman -S'"
git config --global alias.aur "!git log --grep='yay -S'"

# Ver cambios en archivos de configuración del sistema
git config --global alias.sysconf "!sudo git --git-dir=/etc/.git --work-tree=/etc"
```

## 💡 **Tips y Buenas Prácticas**

### **Mensajes de commit convencionales**
```bash
feat:     # Nueva característica
fix:      # Corrección de bug
docs:     # Documentación
style:    # Formato, punto y coma, etc
refactor: # Refactorización de código
test:     # Agregar tests
chore:    # Tareas de mantenimiento
perf:     # Mejora de rendimiento
ci:       # Configuración de CI
build:    # Cambios en sistema de build
revert:   # Revertir commit
```

### **Alias útiles para git**
```bash
# Configurar alias globales
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
git config --global alias.graph "log --graph --oneline --decorate --all"
```

---

✨ *Esta guía completa incluye todo lo necesario para trabajar profesionalmente con GitHub/GitLab en Ubuntu/Debian, Arch/Manjaro y Windows. La combinación de Git, SSH, MAN y LESS te dará un flujo de trabajo eficiente y bien documentado.* ✨

📚 **Recursos adicionales:**
- `man git` - Tu mejor amigo
- `git help -g` - Lista de guías
- `https://docs.github.com` - Documentación oficial
- `https://docs.gitlab.com` - Documentación oficial
