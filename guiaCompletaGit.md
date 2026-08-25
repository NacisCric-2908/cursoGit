# Guía Completa y Definitiva de Git y GitHub/GitLab 🚀

Esta guía unifica y expande toda la información necesaria para dominar **Git**, **GitHub** y **GitLab** desde cero hasta un flujo de trabajo profesional, adaptada para múltiples sistemas operativos y distribuciones.

---

## 📋 Índice
1. [Instalación de Git y Herramientas Esenciales](#1-instalación-de-git-y-herramientas-esenciales)
2. [Configuración Inicial de Git](#2-configuración-inicial-de-git)
3. [Configuración de Llaves SSH (GitHub y GitLab)](#3-configuración-de-llaves-ssh-github-y-gitlab)
4. [Flujo de Trabajo Básico y Local](#4-flujo-de-trabajo-básico-y-local)
5. [Ramas (Branches) y Fusión (Merge/Rebase)](#5-ramas-branches-y-fusión-mergerebase)
6. [Trabajo con Repositorios Remotos y Colaboración](#6-trabajo-con-repositorios-remotos-y-colaboración)
7. [Deshacer Cambios y Recuperación (¡Salvar el día!)](#7-deshacer-cambios-y-recuperación-salvar-el-día)
8. [Uso de MAN y LESS para Documentación](#8-uso-de-man-y-less-para-documentación)
9. [Herramientas CLI Oficiales (gh y glab)](#9-herramientas-cli-oficiales-gh-y-glab)
10. [Buenas Prácticas y Commits Convencionales](#10-buenas-prácticas-y-commits-convencionales)
11. [Solución de Problemas Comunes](#11-solución-de-problemas-comunes)

---

## 1. Instalación de Git y Herramientas Esenciales

### 🐧 Linux
Elige el comando correspondiente a tu distribución para instalar Git junto con utilidades útiles (`man` para ayuda, `less` como paginador y `tree` para ver directorios):

*   **Debian / Ubuntu / Pop!_OS / Mint:**
    ```bash
    sudo apt update && sudo apt install -y git man less tree
    ```
*   **Arch Linux / Manjaro:**
    ```bash
    sudo pacman -Syu && sudo pacman -S --needed git man-db less tree
    # Opcional (documentación extra de Git en Arch):
    sudo pacman -S git-man git-docs
    ```
*   **Fedora / RHEL / CentOS:**
    ```bash
    sudo dnf install -y git man-db less tree
    ```
*   **openSUSE / SUSE Linux:**
    ```bash
    sudo zypper install -y git man less tree
    ```

### 🍎 macOS
Si utilizas **Homebrew**, ejecuta:
```bash
brew install git tree
```
*Nota: macOS ya incluye `man` y `less` por defecto.*

### 🪟 Windows
Descarga e instala **Git for Windows** desde [git-scm.com](https://git-scm.com/). Esto instalará **Git Bash**, un entorno de terminal que emula la línea de comandos de Linux e incluye `git`, `less` y utilidades Unix.

---

## 2. Configuración Inicial de Git

Antes de crear commits, debes identificarte. Estos datos se adjuntarán a tu historial de cambios.

```bash
# Configurar identidad global
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Definir la rama predeterminada al inicializar (se recomienda 'main')
git config --global init.defaultBranch main

# Configurar el editor de texto por defecto (ejemplos)
git config --global core.editor "code --wait"      # VS Code
# git config --global core.editor "nano"            # Nano

# Listar toda la configuración activa
git config --list
```

---

## 3. Configuración de Llaves SSH (GitHub y GitLab)

El uso de llaves SSH te permite interactuar con repositorios remotos sin ingresar tu contraseña o token cada vez.

### Paso 1: Generar la llave SSH (Algoritmo ED25519 recomendado)
```bash
ssh-keygen -t ed25519 -C "tu@email.com"
# Presiona Enter para aceptar la ubicación por defecto (~/.ssh/id_ed25519)
# Opcional: Escribe una frase de contraseña (passphrase) por seguridad
```

### Paso 2: Iniciar el agente SSH y añadir tu llave
```bash
# Iniciar agente en segundo plano
eval "$(ssh-agent -s)"

# Añadir la llave privada generada al agente
ssh-add ~/.ssh/id_ed25519
```

### Paso 3: Configurar el archivo SSH Config (Opcional pero muy útil)
Crea o edita el archivo `~/.ssh/config` para gestionar tus accesos fácilmente:
```bash
nano ~/.ssh/config
```
Añade el siguiente contenido:
```text
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
```
Asegura los permisos correctos en directorios de configuración de SSH (crítico en Linux/macOS):
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### Paso 4: Añadir la llave pública a tu plataforma web
Copia el contenido de tu llave pública:
```bash
cat ~/.ssh/id_ed25519.pub
```
1.  **GitHub**: Ve a *Settings* → *SSH and GPG keys* → *New SSH key* → Pega el contenido y guarda.
2.  **GitLab**: Ve a *Preferences* → *SSH Keys* → *Add new key* → Pega el contenido y guarda.

### Paso 5: Probar la conexión
```bash
ssh -T git@github.com
# Salida esperada: Hi username! You've successfully authenticated...

ssh -T git@gitlab.com
# Salida esperada: Welcome to GitLab, @username!
```

---

## 4. Flujo de Trabajo Básico y Local

El ciclo de vida local consta de tres áreas: **Directorio de Trabajo** (Working Directory), **Área de Preparación** (Staging Area) y **Repositorio** (Git Directory).

```bash
git init                    # Inicializar un nuevo repositorio local
git status                 # Ver el estado de los archivos y cambios

# Preparación (Staging)
git add <archivo>          # Preparar un archivo específico
git add .                  # Preparar todos los cambios del directorio actual

# Confirmación (Commit)
git commit -m "Mensaje"    # Registrar cambios con un mensaje descriptivo
git commit -am "Mensaje"   # Añadir y confirmar en un solo paso (solo archivos ya trackeados)

# Visualización del Historial
git log                    # Historial completo
git log --oneline          # Historial simplificado en una línea
git log --graph --all --oneline # Árbol visual del historial de todas las ramas
git diff                   # Diferencias de archivos no preparados (Working Dir vs Stage)
git diff --staged          # Diferencias en el área de preparación (Stage vs Commit)
```

---

## 5. Ramas (Branches) y Fusión (Merge/Rebase)

Las ramas permiten desarrollar funcionalidades de manera aislada sin alterar el código principal.

```bash
git branch                 # Listar ramas locales
git branch -a              # Listar todas las ramas (locales y remotas)
git branch <nombre>        # Crear una nueva rama
git checkout <rama>        # Cambiar a la rama especificada
git checkout -b <rama>     # Crear una nueva rama y cambiar a ella inmediatamente

# Fusión (Merge)
# (Estando en la rama receptora, ej. main)
git merge <rama-feature>   # Fusionar cambios de la rama-feature a la rama actual

# Rebase (Reorganizar el historial de commits)
# (Estando en la rama de desarrollo o feature)
git rebase main            # Aplica tus cambios de feature encima de los últimos de main

# Eliminar ramas
git branch -d <rama>       # Eliminar rama local (seguro: advierte si no se ha fusionado)
git branch -D <rama>       # Eliminar rama local (forzado)
```

---

## 6. Trabajo con Repositorios Remotos y Colaboración

### Configuración del Remoto
```bash
git remote -v                     # Ver servidores remotos configurados
git remote add origin <url-ssh>   # Asociar un repositorio remoto
```

### Clonación y Descargas
```bash
git clone <url-ssh>               # Clonar un repositorio completo
git clone -b <rama> <url-ssh>     # Clonar una rama específica
git clone --depth 1 <url-ssh>     # Clonar solo el último commit (historial limitado, útil para descargas rápidas)
git clone --recurse-submodules <url-ssh> # Clonar incluyendo submódulos del proyecto
```

### Empujar y Traer Cambios
```bash
git push -u origin main           # Subir la rama local por primera vez y rastrear remota
git push                          # Subir commits locales a la rama remota rastreada
git fetch                         # Descargar metadatos y ramas del remoto (sin modificar tu código local)
git pull                          # Descargar y fusionar los cambios del remoto (fetch + merge)
```

### Flujo de Sincronización de un Fork (Contribución)
Si has hecho un *Fork* de un proyecto original en GitHub/GitLab:
```bash
# 1. Añadir el repositorio original como remoto "upstream"
git remote add upstream git@github.com:autor_original/proyecto.git

# 2. Descargar cambios del repositorio original
git fetch upstream

# 3. Traer los cambios de la rama principal original a tu rama local
git checkout main
git merge upstream/main  # o usando: git rebase upstream/main

# 4. Subir la actualización a tu propio Fork remoto (origin)
git push origin main
```

---

## 7. Deshacer Cambios y Recuperación (¡Salvar el día!)

Git cuenta con mecanismos para enmendar errores y recuperar estados anteriores del código.

```bash
# Restaurar archivos locales
git restore <archivo>             # Descartar los cambios no guardados en el Stage de un archivo
git restore --staged <archivo>    # Quitar un archivo del Stage (Staging Area), manteniendo su contenido

# Modificar el último commit
git commit --amend -m "Nuevo mensaje" # Cambiar el mensaje del último commit o agregar archivos olvidados al mismo

# Revertir y Resetear
git revert <hash-commit>          # Crear un nuevo commit que deshace los cambios del commit especificado (seguro para remotos)
git reset --soft HEAD~1           # Deshacer el último commit local, manteniendo tus archivos en Staging
git reset --mixed HEAD~1          # Deshacer el último commit local, manteniendo los cambios pero fuera de Staging
git reset --hard HEAD~1           # Deshacer el último commit local y BORRAR todos los cambios del directorio de trabajo (usar con cuidado)

# Limpieza de archivos no rastreados
git clean -fd                     # Elimina directorios (-d) y archivos (-f) no rastreados por Git

# Herramientas de rescate de emergencia
git reflog                        # Muestra el historial completo de acciones locales (incluso commits eliminados o resets).
# Permite volver a cualquier punto usando: git reset --hard <hash-reflog>

# Stash (Guardado temporal sin hacer commit)
git stash                         # Guardar cambios actuales temporalmente y limpiar Working Dir
git stash list                    # Listar stashes guardados
git stash pop                     # Aplicar el último stash y eliminarlo de la lista
git stash apply                   # Aplicar el último stash sin borrarlo
git stash drop                    # Eliminar un stash específico
```

---

## 8. Uso de MAN y LESS para Documentación

Puedes consultar toda la ayuda de Git sin necesidad de conexión a internet usando el manual interactivo del sistema.

```bash
# Comandos de ayuda generales
man git                           # Manual completo de Git
man gittutorial                   # Tutorial introductorio de Git
man gitworkflows                  # Flujos de trabajo recomendados

# Ayuda para comandos específicos
man git-commit
man git-rebase
# Alternativa rápida:
git help <comando>
```

### ⌨️ Atajos clave en MAN (paginador `less`):
*   `Espacio` / `Re Pág` / `Av Pág`: Navegar por la página.
*   `/palabra`: Buscar una palabra específica hacia adelante.
*   `?palabra`: Buscar una palabra específica hacia atrás.
*   `n`: Ir a la siguiente coincidencia encontrada.
*   `N`: Ir a la coincidencia anterior.
*   `g`: Ir al inicio del documento.
*   `G`: Ir al final del documento.
*   `q`: Salir de la documentación.

---

## 9. Herramientas CLI Oficiales (gh y glab)

Interactúa con las plataformas de desarrollo directamente desde tu terminal.

### GitHub CLI (`gh`)
*   **Instalación**:
    *   Ubuntu/Debian: `sudo apt install gh`
    *   Arch: `sudo pacman -S github-cli`
    *   Fedora: `sudo dnf install gh`
    *   Windows: `winget install --id GitHub.cli`
*   **Uso básico**:
    ```bash
    gh auth login              # Iniciar sesión y autenticar terminal
    gh repo create             # Crear un repositorio de forma interactiva
    gh pr create               # Crear un Pull Request
    gh pr checkout <num>       # Traer la rama de un PR específico para probarla localmente
    gh issue list              # Listar problemas en el repositorio
    ```

### GitLab CLI (`glab`)
*   **Instalación**:
    *   Ubuntu/Debian: `sudo apt install glab`
    *   Arch: `yay -S glab` (Desde AUR)
    *   Fedora: `sudo dnf install glab`
    *   Windows: `scoop install glab` o `winget install glab`
*   **Uso básico**:
    ```bash
    glab auth login            # Autenticar con tu cuenta de GitLab
    glab repo clone user/repo  # Clonar un repositorio
    glab mr create             # Crear un Merge Request
    glab mr list               # Listar Merge Requests pendientes
    glab pipeline status       # Ver el estado actual de los pipelines de CI/CD
    ```

---

## 10. Buenas Prácticas y Commits Convencionales

Mantener un historial legible y estructurado facilita la colaboración y automatización de notas de versión (changelogs).

### Estructura de Commit Semántico (Conventional Commits)
Un commit se compone de un tipo, un ámbito (opcional) y una descripción clara:

```text
tipo(ámbito): descripción corta en minúsculas e imperativo
```

#### Tipos comunes:
*   `feat`: Nueva funcionalidad.
*   `fix`: Corrección de un error o bug.
*   `docs`: Cambios exclusivos en la documentación.
*   `style`: Cambios estéticos, de formato o de estilo de código (sin cambiar lógica).
*   `refactor`: Modificaciones de código que no corrigen errores ni añaden funcionalidades (ej. optimizar rendimiento, renombrar variables).
*   `test`: Añadir o modificar pruebas unitarias o de integración.
*   `chore`: Tareas de mantenimiento o configuración del proyecto (ej. actualizar dependencias).

### Alias recomendados para tu Git
Ahorra tiempo creando abreviaturas para tus comandos más largos:
```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.last 'log -1 HEAD'
git config --global alias.graph "log --graph --oneline --decorate --all"
```

---

## 11. Solución de Problemas Comunes

### 🔴 Error: "Permission denied (publickey)" al usar SSH
1.  Verifica que el agente SSH se está ejecutando: `eval "$(ssh-agent -s)"`
2.  Asegúrate de haber añadido tu llave privada: `ssh-add -l` (si no aparece, ejecuta `ssh-add ~/.ssh/id_ed25519`).
3.  Verifica si copiaste la llave pública correcta en la web (`id_ed25519.pub`).
4.  Realiza un test de diagnóstico:
    ```bash
    ssh -vT git@github.com
    ```

### 🔴 Error: He hecho un commit en la rama equivocada
Si hiciste commits en `main` que debían ir en una rama de feature:
```bash
# 1. Crea la rama de feature con el estado actual
git branch feature/nueva-idea

# 2. Deshaz el último commit en main (los cambios vuelven a estar listos)
git checkout main
git reset --hard HEAD~1   # Ojo: esto borra el commit en main.

# 3. Ve a tu nueva rama
git checkout feature/nueva-idea
```

### 🔴 Error: Guardar credenciales HTTPS en caché
Si no usas SSH y quieres evitar escribir tu contraseña constantemente:
```bash
# Guardar temporalmente en caché por 1 hora (3600 segundos)
git config --global credential.helper 'cache --timeout=3600'

# Guardar de manera permanente en disco (No recomendado en computadoras públicas)
git config --global credential.helper store
```
