# Guía 1 · Comandos de Git (referencia de consulta)

> **Propósito:** esta guía no se lee de corrido: se consulta. Cada comando trae una explicación corta y un ejemplo. Usa `Ctrl + F` para buscar.
>
> **Convenciones:** lo que va entre `<>` se reemplaza por tu valor (`<rama>` → `feature/login`). Lo que va entre `[]` es opcional.

---

## Índice

1. [Configuración inicial](#1-configuración-inicial)
2. [Crear y clonar repositorios](#2-crear-y-clonar-repositorios)
3. [Estado y cambios del área de trabajo](#3-estado-y-cambios-del-área-de-trabajo)
4. [Staging (preparar cambios)](#4-staging-preparar-cambios)
5. [Commits](#5-commits)
6. [Historial e inspección](#6-historial-e-inspección)
7. [Ramas](#7-ramas)
8. [Fusionar: merge](#8-fusionar-merge)
9. [Reescribir: rebase y cherry-pick](#9-reescribir-rebase-y-cherry-pick)
10. [Deshacer cambios](#10-deshacer-cambios)
11. [Stash (guardar trabajo temporal)](#11-stash-guardar-trabajo-temporal)
12. [Repositorios remotos](#12-repositorios-remotos)
13. [Tags y versiones](#13-tags-y-versiones)
14. [Búsqueda y depuración](#14-búsqueda-y-depuración)
15. [Limpieza y mantenimiento](#15-limpieza-y-mantenimiento)
16. [Archivos especiales: .gitignore y .gitattributes](#16-archivos-especiales)
17. [Submódulos y worktrees](#17-submódulos-y-worktrees)
18. [Alias útiles](#18-alias-útiles)
19. [GitHub CLI (gh)](#19-github-cli-gh)
20. [Recetas para emergencias](#20-recetas-para-emergencias)

---

## 1. Configuración inicial

Git guarda la configuración en tres niveles: **sistema** (`--system`, todos los usuarios), **global** (`--global`, tu usuario) y **local** (`--local`, solo el repositorio actual, tiene prioridad).

| Comando | Qué hace |
|---|---|
| `git config --global user.name "<nombre>"` | Nombre que aparecerá en tus commits |
| `git config --global user.email "<correo>"` | Correo de tus commits (debe coincidir con el de GitHub para que se vinculen a tu perfil) |
| `git config --global init.defaultBranch main` | La rama inicial de los repos nuevos se llamará `main` |
| `git config --global core.editor "nano"` | Editor para mensajes de commit (`vim`, `nano`, `code --wait`) |
| `git config --global pull.rebase false` | `git pull` hará merge (comportamiento clásico). Con `true` hará rebase |
| `git config --global core.autocrlf input` | En Linux: convierte CRLF a LF al hacer commit, evita líos de saltos de línea |
| `git config --global color.ui auto` | Salida con colores |
| `git config --list --show-origin` | Muestra toda la configuración y de qué archivo viene |
| `git config user.email` | Consulta un valor concreto |
| `git config --global --unset <clave>` | Borra una configuración |
| `git config --global --edit` | Abre el archivo `~/.gitconfig` en el editor |

```bash
git config --global user.name "Ana Pérez"
git config --global user.email "ana.perez@correo.com"
git config --global init.defaultBranch main
git config --list
```

### Autenticación con GitHub por SSH

GitHub no acepta contraseña por HTTPS; se usa **token** o **llave SSH**. SSH es lo más cómodo.

```bash
ssh-keygen -t ed25519 -C "ana.perez@correo.com"   # genera la llave (Enter a todo)
cat ~/.ssh/id_ed25519.pub                          # copia esta llave pública
# GitHub → Settings → SSH and GPG keys → New SSH key → pegar
ssh -T git@github.com                              # prueba: "Hi ana! You've successfully authenticated"
```

### Firmar commits (opcional, suma puntos de seguridad)

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
# En GitHub agrega la MISMA llave como "Signing key" (New SSH key → Key type: Signing Key)
```

Los commits firmados aparecen con la etiqueta **Verified** en GitHub.

---

## 2. Crear y clonar repositorios

| Comando | Qué hace |
|---|---|
| `git init` | Convierte la carpeta actual en repositorio (crea `.git/`) |
| `git init <carpeta>` | Crea la carpeta y la inicializa |
| `git clone <url>` | Descarga un repositorio completo con todo su historial |
| `git clone <url> <carpeta>` | Clona en una carpeta con otro nombre |
| `git clone --branch <rama> <url>` | Clona y se ubica en esa rama |
| `git clone --depth 1 <url>` | Clon superficial: solo el último commit (rápido, útil en CI) |

```bash
mkdir mi-proyecto && cd mi-proyecto
git init
git clone git@github.com:ana/mi-proyecto.git
git clone --depth 1 https://github.com/torvalds/linux.git
```

---

## 3. Estado y cambios del área de trabajo

Recuerda las **tres zonas** de Git:

```
Directorio de trabajo  --git add-->  Staging (index)  --git commit-->  Repositorio (.git)
```

| Comando | Qué hace |
|---|---|
| `git status` | Muestra qué archivos cambiaron, cuáles están en staging y cuáles no se rastrean |
| `git status -s` | Versión corta (`M` modificado, `A` añadido, `??` sin rastrear) |
| `git diff` | Diferencias entre el directorio de trabajo y el staging (lo que aún NO has añadido) |
| `git diff --staged` | Diferencias entre staging y el último commit (lo que VAS a commitear) |
| `git diff <rama1> <rama2>` | Diferencias entre dos ramas |
| `git diff <commit1> <commit2> -- <archivo>` | Diferencias de un archivo entre dos commits |
| `git diff --stat` | Resumen: archivos cambiados y número de líneas |
| `git diff --name-only main..develop` | Solo los nombres de archivos que difieren |

```bash
git status -s
#  M app.py
# ?? tests/test_app.py
git diff --staged
git diff main develop --stat
```

---

## 4. Staging (preparar cambios)

| Comando | Qué hace |
|---|---|
| `git add <archivo>` | Añade un archivo al staging |
| `git add .` | Añade todo lo de la carpeta actual hacia abajo |
| `git add -A` | Añade todo el repositorio, incluidos borrados |
| `git add -p` | **Modo interactivo por fragmentos**: decides trozo por trozo qué entra. Clave para microcommits |
| `git add *.py` | Añade por patrón |
| `git restore --staged <archivo>` | Saca un archivo del staging (no pierde cambios) |
| `git rm <archivo>` | Borra el archivo y registra el borrado |
| `git rm --cached <archivo>` | Deja de rastrear el archivo pero lo conserva en disco (útil si subiste un `.env` por error) |
| `git mv <viejo> <nuevo>` | Renombra o mueve un archivo |

```bash
git add -p app.py
# Stage this hunk [y,n,q,a,d,s,e,?]?
#  y = sí   n = no   s = dividir el fragmento   q = salir
git rm --cached .env
echo ".env" >> .gitignore
```

> **Microcommits:** `git add -p` te permite hacer dos commits distintos con cambios de un mismo archivo. Úsalo.

---

## 5. Commits

| Comando | Qué hace |
|---|---|
| `git commit` | Abre el editor para escribir el mensaje |
| `git commit -m "<mensaje>"` | Commit con mensaje en línea |
| `git commit -m "<título>" -m "<cuerpo>"` | Título y cuerpo (cada `-m` es un párrafo) |
| `git commit -am "<mensaje>"` | Añade archivos **ya rastreados** y hace commit (no incluye archivos nuevos) |
| `git commit --amend` | Modifica el último commit (mensaje o contenido). **Solo si no lo has subido** |
| `git commit --amend --no-edit` | Agrega lo que está en staging al último commit sin cambiar el mensaje |
| `git commit --allow-empty -m "<msg>"` | Commit vacío (útil para disparar un pipeline de CI) |
| `git commit -S -m "<msg>"` | Commit firmado |
| `git commit --fixup <hash>` | Crea un commit de corrección para fusionarlo luego con `rebase --autosquash` |

```bash
git commit -m "feat(auth): agrega validación de correo en el registro"
git commit -m "fix(api): corrige error 500 al enviar body vacío" -m "Closes #12"
# Olvidé un archivo en el último commit (aún no hice push):
git add utils.py
git commit --amend --no-edit
```

> Ver la **Guía 2** para el formato de mensajes (Conventional Commits).

---

## 6. Historial e inspección

| Comando | Qué hace |
|---|---|
| `git log` | Historial completo |
| `git log --oneline` | Una línea por commit |
| `git log --oneline --graph --all --decorate` | **Árbol de todas las ramas.** El más útil para entender el repo |
| `git log -n 5` | Últimos 5 commits |
| `git log -p <archivo>` | Historial de un archivo con sus cambios |
| `git log --author="Ana"` | Commits de un autor |
| `git log --since="2026-11-12" --until="2026-11-25"` | Commits en un rango de fechas |
| `git log --grep="fix"` | Commits cuyo mensaje contiene "fix" |
| `git log -S "funcion_x"` | Commits que añadieron o quitaron ese texto ("pickaxe") |
| `git log main..develop` | Commits que están en `develop` y no en `main` |
| `git log --stat` | Archivos modificados por commit |
| `git log --pretty=format:"%h %an %ar %s"` | Formato personalizado (hash, autor, hace cuánto, mensaje) |
| `git shortlog -sn` | Número de commits por autor |
| `git show <hash>` | Detalle de un commit |
| `git show <hash>:<archivo>` | Contenido de un archivo en ese commit |
| `git blame <archivo>` | Quién modificó cada línea y en qué commit |
| `git reflog` | **Historial de todo lo que hizo HEAD**, incluso commits "perdidos". Tu red de seguridad |

```bash
git log --oneline --graph --all
# * 3f2a1c9 (HEAD -> develop) feat: agrega endpoint /health
# | * 9b8e7d6 (main) fix: corrige puerto
# |/
# * 1a2b3c4 chore: estructura inicial

git log --oneline main..develop     # ¿qué falta por llevar a main?
git blame -L 10,20 app.py           # solo las líneas 10 a 20
```

> Consejo: crea el alias `git lg` (ver [sección 18](#18-alias-útiles)).

---

## 7. Ramas

| Comando | Qué hace |
|---|---|
| `git branch` | Lista ramas locales (`*` = actual) |
| `git branch -a` | Lista locales y remotas |
| `git branch -vv` | Ramas con su último commit y la rama remota que siguen |
| `git branch <rama>` | Crea una rama (no se cambia a ella) |
| `git switch <rama>` | Cambia de rama (comando moderno) |
| `git switch -c <rama>` | Crea y cambia a la rama |
| `git switch -c <rama> <origen>` | Crea la rama a partir de otra rama o commit |
| `git switch -` | Vuelve a la rama anterior |
| `git checkout <rama>` | Forma clásica de cambiar de rama |
| `git checkout -b <rama>` | Forma clásica de crear y cambiar |
| `git branch -m <nuevo-nombre>` | Renombra la rama actual |
| `git branch -d <rama>` | Borra una rama ya fusionada |
| `git branch -D <rama>` | Fuerza el borrado (aunque no esté fusionada) |
| `git branch --merged` | Ramas ya fusionadas en la actual |
| `git branch --no-merged` | Ramas aún sin fusionar |
| `git push -u origin <rama>` | Sube la rama y configura el seguimiento |
| `git push origin --delete <rama>` | Borra la rama en el remoto |

```bash
git switch develop
git switch -c feature/7-login            # rama para el issue #7
git push -u origin feature/7-login
git branch -a
git switch -c hotfix/1.0.1 main          # hotfix sale de main
```

> **Para el proyecto final:** NO borres las ramas después de fusionarlas; se usarán para la evaluación.

---

## 8. Fusionar: merge

| Comando | Qué hace |
|---|---|
| `git merge <rama>` | Trae los cambios de `<rama>` a la rama actual |
| `git merge --no-ff <rama>` | Fuerza un commit de merge aunque se pudiera avanzar en línea (conserva la "forma" de la rama en el historial) |
| `git merge --ff-only <rama>` | Solo fusiona si es posible avanzar en línea; si no, falla |
| `git merge --squash <rama>` | Junta todos los cambios en el staging para hacer un único commit |
| `git merge --abort` | Cancela un merge con conflictos y vuelve al estado anterior |
| `git merge --continue` | Continúa tras resolver conflictos |

```bash
git switch develop
git merge --no-ff feature/7-login
```

### Resolver conflictos

```text
<<<<<<< HEAD
puerto = 8000
=======
puerto = 5000
>>>>>>> feature/7-login
```

1. Edita el archivo y deja la versión correcta (borra los marcadores `<<<<<<<`, `=======`, `>>>>>>>`).
2. `git add <archivo>`
3. `git commit` (o `git merge --continue`).

| Comando útil en conflictos | Qué hace |
|---|---|
| `git diff --name-only --diff-filter=U` | Lista los archivos en conflicto |
| `git checkout --ours <archivo>` | Me quedo con mi versión (la de la rama actual) |
| `git checkout --theirs <archivo>` | Me quedo con la versión de la otra rama |
| `git mergetool` | Abre una herramienta visual de fusión |

---

## 9. Reescribir: rebase y cherry-pick

> ⚠️ **Regla de oro:** nunca reescribas historia que ya está en el remoto y que otros usan. En ramas tuyas `feature/*` antes del PR, sí puedes.

| Comando | Qué hace |
|---|---|
| `git rebase <rama>` | Reaplica tus commits encima de `<rama>` (historial lineal) |
| `git rebase -i HEAD~<n>` | **Rebase interactivo**: reordena, une, edita o borra los últimos n commits |
| `git rebase -i --autosquash <base>` | Aplica automáticamente los commits `--fixup` |
| `git rebase --continue` | Continúa tras resolver un conflicto |
| `git rebase --abort` | Cancela el rebase |
| `git rebase --skip` | Salta el commit que causa conflicto |
| `git cherry-pick <hash>` | Copia un commit concreto a la rama actual |
| `git cherry-pick <h1> <h2>` | Copia varios commits |
| `git cherry-pick -x <hash>` | Copia y deja en el mensaje la referencia al commit original |

```bash
# Actualizar mi feature con lo último de develop antes del PR
git switch feature/7-login
git fetch origin
git rebase origin/develop

# Limpiar los últimos 4 commits
git rebase -i HEAD~4
# pick  a1b2c3 feat: formulario
# squash d4e5f6 wip
# reword 7g8h9i fix: typo
# drop  j1k2l3 prueba
```

Opciones del rebase interactivo: `pick` (usar), `reword` (cambiar mensaje), `edit` (parar para modificar), `squash` (unir con el anterior y combinar mensajes), `fixup` (unir y descartar el mensaje), `drop` (eliminar).

---

## 10. Deshacer cambios

| Situación | Comando |
|---|---|
| Descartar cambios de un archivo no añadido | `git restore <archivo>` |
| Descartar TODOS los cambios no añadidos | `git restore .` |
| Sacar un archivo del staging | `git restore --staged <archivo>` |
| Recuperar un archivo como estaba en un commit | `git restore --source <hash> <archivo>` |
| Deshacer el último commit, conservando cambios en staging | `git reset --soft HEAD~1` |
| Deshacer el último commit, conservando cambios sin staging | `git reset HEAD~1` (o `--mixed`) |
| Deshacer el último commit y **borrar** sus cambios | `git reset --hard HEAD~1` ⚠️ |
| Dejar la rama exactamente como el remoto | `git reset --hard origin/<rama>` ⚠️ |
| Revertir un commit ya publicado (crea un commit inverso) | `git revert <hash>` ✅ seguro |
| Revertir un commit de merge | `git revert -m 1 <hash-merge>` |
| Revertir sin commitear aún | `git revert --no-commit <hash>` |

```bash
git reset --soft HEAD~1     # "me equivoqué en el mensaje o quiero dividir el commit"
git revert 9b8e7d6          # en main: deshacer algo que ya está publicado
```

> **reset vs revert:** `reset` mueve la rama hacia atrás (reescribe historia, solo local). `revert` crea un nuevo commit que deshace otro (seguro en ramas compartidas como `main`).

---

## 11. Stash (guardar trabajo temporal)

Guarda cambios a medias para cambiar de rama sin hacer commit.

| Comando | Qué hace |
|---|---|
| `git stash` | Guarda los cambios rastreados y limpia el directorio |
| `git stash push -m "<descripción>"` | Guarda con un nombre |
| `git stash -u` | Incluye archivos sin rastrear |
| `git stash list` | Lista los stashes |
| `git stash show -p stash@{0}` | Muestra el contenido de un stash |
| `git stash pop` | Aplica el último stash y lo borra |
| `git stash apply stash@{1}` | Aplica un stash sin borrarlo |
| `git stash drop stash@{1}` | Borra un stash |
| `git stash clear` | Borra todos |
| `git stash branch <rama>` | Crea una rama a partir de un stash |

```bash
# Estoy en feature/7-login y aparece un bug urgente en producción
git stash push -m "login a medias"
git switch -c hotfix/1.0.1 main
# ... arreglo, commit, PR ...
git switch feature/7-login
git stash pop
```

---

## 12. Repositorios remotos

| Comando | Qué hace |
|---|---|
| `git remote -v` | Lista los remotos y sus URL |
| `git remote add origin <url>` | Agrega un remoto llamado `origin` |
| `git remote set-url origin <url>` | Cambia la URL (por ejemplo, de HTTPS a SSH) |
| `git remote rename <viejo> <nuevo>` | Renombra un remoto |
| `git remote remove <nombre>` | Elimina un remoto |
| `git remote show origin` | Información detallada del remoto |
| `git fetch` | Descarga cambios del remoto **sin fusionarlos** |
| `git fetch --prune` | Descarga y elimina referencias a ramas remotas borradas |
| `git pull` | `fetch` + `merge` de la rama remota en la actual |
| `git pull --rebase` | `fetch` + `rebase` (historial más limpio) |
| `git push` | Sube los commits de la rama actual |
| `git push -u origin <rama>` | Sube y fija la rama remota de seguimiento |
| `git push --tags` | Sube todas las etiquetas |
| `git push --force-with-lease` | Fuerza el push **solo si nadie más subió cambios**. Úsalo en vez de `--force` |

```bash
git remote add origin git@github.com:ana/mi-proyecto.git
git push -u origin main
git fetch --prune
git pull --rebase origin develop
git push --force-with-lease   # tras un rebase de MI rama feature
```

### Trabajar con forks

```bash
git remote add upstream git@github.com:profe/repo-original.git
git fetch upstream
git rebase upstream/main
```

---

## 13. Tags y versiones

Las etiquetas marcan versiones (`v1.0.0`). Se usan para releases y para disparar pipelines.

| Comando | Qué hace |
|---|---|
| `git tag` | Lista las etiquetas |
| `git tag -l "v1.*"` | Lista por patrón |
| `git tag v1.0.0` | Etiqueta ligera (solo un puntero) |
| `git tag -a v1.0.0 -m "<mensaje>"` | **Etiqueta anotada** (autor, fecha, mensaje). Úsala siempre |
| `git tag -a v0.9.0 <hash> -m "<msg>"` | Etiqueta un commit antiguo |
| `git show v1.0.0` | Detalle de la etiqueta |
| `git push origin v1.0.0` | Sube una etiqueta |
| `git push origin --tags` | Sube todas |
| `git tag -d v1.0.0` | Borra localmente |
| `git push origin --delete v1.0.0` | Borra en el remoto |
| `git describe --tags` | Dice en qué versión estás (`v1.0.0-3-g9b8e7d6` = 3 commits después de v1.0.0) |

```bash
git switch main
git pull
git tag -a v1.0.0 -m "Primera versión estable"
git push origin v1.0.0
```

---

## 14. Búsqueda y depuración

| Comando | Qué hace |
|---|---|
| `git grep "<texto>"` | Busca texto en los archivos rastreados |
| `git grep -n "TODO"` | Con número de línea |
| `git bisect start` | Inicia búsqueda binaria del commit que introdujo un bug |
| `git bisect bad` | El commit actual tiene el bug |
| `git bisect good <hash>` | Este commit estaba bien |
| `git bisect run <comando>` | Automatiza la búsqueda con un script (por ejemplo, tus tests) |
| `git bisect reset` | Termina y vuelve a donde estabas |

```bash
git bisect start
git bisect bad                 # ahora falla
git bisect good v1.0.0         # en v1.0.0 funcionaba
git bisect run pytest -q       # Git prueba commits hasta encontrar el culpable
git bisect reset
```

---

## 15. Limpieza y mantenimiento

| Comando | Qué hace |
|---|---|
| `git clean -n` | Muestra qué archivos sin rastrear se borrarían (simulacro) |
| `git clean -fd` | Borra archivos y carpetas sin rastrear ⚠️ |
| `git clean -fdx` | Igual, pero también los ignorados (`.gitignore`) ⚠️ |
| `git gc` | Compacta y optimiza el repositorio |
| `git fsck` | Verifica la integridad |
| `git count-objects -vH` | Tamaño del repositorio |
| `git archive --format=zip HEAD -o proyecto.zip` | Exporta el código sin la carpeta `.git` |

---

## 16. Archivos especiales

### .gitignore

```gitignore
# Entornos y secretos
.env
.venv/
venv/

# Python
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/

# Node
node_modules/
dist/

# Sistema y editores
.DS_Store
.vscode/
.idea/

# Excepción: sí quiero versionar este archivo
!.env.example
```

| Comando | Qué hace |
|---|---|
| `git check-ignore -v <archivo>` | Dice qué regla ignora ese archivo |
| `git ls-files` | Lista los archivos rastreados |
| `git ls-files --others --ignored --exclude-standard` | Lista los ignorados |

Plantillas: <https://github.com/github/gitignore>

### .gitattributes

```gitattributes
* text=auto eol=lf
*.sh text eol=lf
*.png binary
```

---

## 17. Submódulos y worktrees

| Comando | Qué hace |
|---|---|
| `git submodule add <url> <ruta>` | Inserta otro repositorio dentro del tuyo |
| `git submodule update --init --recursive` | Descarga los submódulos tras clonar |
| `git clone --recurse-submodules <url>` | Clona con submódulos |
| `git worktree add ../hotfix hotfix/1.0.1` | Abre otra rama en otra carpeta, sin cambiar la actual |
| `git worktree list` | Lista los worktrees |
| `git worktree remove ../hotfix` | Elimina un worktree |

---

## 18. Alias útiles

```bash
git config --global alias.st "status -s"
git config --global alias.co switch
git config --global alias.br "branch -vv"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
git config --global alias.amend "commit --amend --no-edit"
```

Uso: `git lg`, `git st`, `git last`.

---

## 19. GitHub CLI (gh)

Herramienta oficial para manejar GitHub desde la terminal. Instalación: <https://cli.github.com> (en Ubuntu/Debian, Fedora y Arch está en los repositorios oficiales o en el repo de GitHub).

| Comando | Qué hace |
|---|---|
| `gh auth login` | Inicia sesión |
| `gh repo create <nombre> --public --clone` | Crea un repo público y lo clona |
| `gh repo view --web` | Abre el repo en el navegador |
| `gh issue create -t "<título>" -b "<cuerpo>"` | Crea un issue |
| `gh issue list` | Lista issues |
| `gh pr create --base develop --head feature/7-login --fill` | Crea un PR |
| `gh pr list` | Lista PRs |
| `gh pr view 5 --web` | Abre el PR #5 |
| `gh pr checks` | Estado del CI del PR |
| `gh pr merge 5 --merge` | Fusiona el PR #5 (también `--squash` o `--rebase`) |
| `gh run list` | Ejecuciones de GitHub Actions |
| `gh run watch` | Sigue una ejecución en vivo |
| `gh release create v1.0.0 --generate-notes` | Crea un release con notas automáticas |
| `gh secret set RENDER_DEPLOY_HOOK` | Crea un secreto del repositorio |

---

## 20. Recetas para emergencias

| Problema | Solución |
|---|---|
| Hice commit en `main` en vez de en una rama (sin push) | `git switch -c feature/x` → `git switch main` → `git reset --hard origin/main` |
| Borré una rama sin querer | `git reflog` → buscar el hash → `git switch -c <rama> <hash>` |
| Hice `reset --hard` y perdí commits | `git reflog` → `git reset --hard <hash-anterior>` |
| Subí un secreto (`.env`, token) | **Revoca el secreto de inmediato** (es lo primero). Luego `git rm --cached .env`, agrégalo a `.gitignore` y haz commit. El secreto sigue en el historial; para borrarlo de verdad se usa `git filter-repo` |
| Mi mensaje del último commit está mal (sin push) | `git commit --amend -m "mensaje correcto"` |
| Quiero ver cómo estaba un archivo hace 3 commits | `git show HEAD~3:<archivo>` |
| `git push` rechazado: "non-fast-forward" | `git pull --rebase` y luego `git push` |
| `git push` rechazado: "protected branch" | Está bien: no se hace push a `main`. Crea una rama y abre un PR |
| Detached HEAD | `git switch -c rama-rescate` para conservar el trabajo, o `git switch <rama>` para salir |
| Quiero traer un solo archivo de otra rama | `git restore --source develop -- ruta/archivo` |

---

### Glosario rápido

- **HEAD:** puntero a donde estás parado (normalmente, la punta de tu rama actual).
- **origin:** nombre por defecto del remoto.
- **upstream:** rama remota que sigue tu rama local, o el repo original de un fork.
- **Fast-forward:** fusión donde la rama solo "avanza" sin crear un commit de merge.
- **HEAD~1, HEAD~2:** uno o dos commits antes de HEAD.
- **Hash:** identificador único de un commit (`9b8e7d6...`); bastan los primeros 7 caracteres.
