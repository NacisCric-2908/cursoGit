# Guía 3 · Configuración del repositorio en GitHub (práctica)

> **Propósito:** guía paso a paso. Al terminarla tendrás un repositorio público con licencia, README, plantillas, ramas protegidas (nadie puede hacer push a `main`), seguridad activada y un tablero Kanban funcionando.
>
> **Tiempo estimado:** 1 a 2 horas.
>
> **Nota:** la interfaz de GitHub cambia de vez en cuando. Si un botón no está exactamente donde dice la guía, busca la sección con el mismo nombre en el menú lateral de **Settings**.

---

## Índice

1. [Crear el repositorio](#paso-1-crear-el-repositorio)
2. [Elegir la licencia](#paso-2-elegir-la-licencia)
3. [Escribir el README](#paso-3-escribir-el-readme)
4. [Crear las ramas permanentes](#paso-4-crear-las-ramas-permanentes)
5. [Ajustes generales de Pull Requests](#paso-5-ajustes-generales-de-pull-requests)
6. [Reglas de protección de ramas (rulesets)](#paso-6-reglas-de-protección-de-ramas)
7. [Permisos de GitHub Actions](#paso-7-permisos-de-github-actions)
8. [Seguridad del código](#paso-8-seguridad-del-código)
9. [Plantillas de PR e issues](#paso-9-plantillas-de-pr-e-issues)
10. [Labels y milestone](#paso-10-labels-y-milestone)
11. [Tablero Kanban con GitHub Projects](#paso-11-tablero-kanban-con-github-projects)
12. [Secretos y variables](#paso-12-secretos-y-variables)
13. [Verificación final](#paso-13-verificación-final)

---

## Paso 1. Crear el repositorio

1. En GitHub, arriba a la derecha: **+ → New repository**.
2. Completa:
   - **Repository name:** en minúsculas con guiones (`gestor-tareas`).
   - **Description:** una línea clara.
   - **Visibility:** **Public** (obligatorio: las reglas de protección, GitHub Pages y SonarQube Cloud son gratuitos en repos públicos).
   - ✅ **Add a README file**.
   - **Add .gitignore:** la plantilla de tu lenguaje (Python, Node...).
   - **Choose a license:** ver paso 2.
3. **Create repository**.
4. Clónalo:

```bash
git clone git@github.com:<usuario>/gestor-tareas.git
cd gestor-tareas
```

---

## Paso 2. Elegir la licencia

Sin licencia, legalmente **nadie puede usar, copiar ni modificar tu código**, aunque sea público. Como estamos en un grupo de software libre, usa una licencia libre.

| Licencia | Tipo | En pocas palabras | Úsala si... |
|---|---|---|---|
| **GPL-3.0** | Copyleft fuerte | Cualquiera puede usarlo y modificarlo, pero las versiones derivadas **deben seguir siendo libres** con la misma licencia | Quieres que tu código y sus derivados sigan siendo libres |
| **AGPL-3.0** | Copyleft de red | Como GPL, pero también obliga a liberar el código si se ofrece **como servicio web** | Tu proyecto es una aplicación web |
| **MIT** | Permisiva | Haz lo que quieras, solo conserva el aviso de copyright | Quieres máxima adopción |
| **Apache-2.0** | Permisiva | Como MIT, más protección explícita de patentes | Proyectos con posibles patentes |

Ayuda para decidir: <https://choosealicense.com>

**Si no la agregaste al crear el repo:** pestaña **Code → Add file → Create new file** → nombre `LICENSE` → aparece el botón **Choose a license template** → elige → **Review and submit**.

> Mientras no tengas las reglas activas (paso 6) puedes hacer commits directos a `main`. Este es el único momento en que se permite.

---

## Paso 3. Escribir el README

El README es la portada del proyecto. Debe permitir que alguien **sin contexto** entienda, instale y ejecute el proyecto.

Plantilla mínima (adáptala):

````markdown
# Gestor de Tareas

![CI](https://github.com/<usuario>/<repo>/actions/workflows/ci.yml/badge.svg)
![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=<project-key>&metric=alert_status)
![License](https://img.shields.io/github/license/<usuario>/<repo>)

Aplicación web para gestionar tareas personales.

## Tabla de contenido
- [Tecnologías](#tecnologías)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso con Docker](#uso-con-docker)
- [Pruebas](#pruebas)
- [Flujo de ramas](#flujo-de-ramas)
- [CI/CD](#cicd)
- [Despliegues](#despliegues)
- [Licencia](#licencia)

## Tecnologías
Python 3.12, Flask, SQLite, Docker, GitHub Actions.

## Requisitos
- Docker 27+ y Docker Compose
- (Opcional) Python 3.12 para desarrollo local

## Instalación
```bash
git clone git@github.com:<usuario>/<repo>.git
cd <repo>
cp .env.example .env
```

## Uso con Docker
```bash
docker compose up -d --build
# Abrir http://localhost:8000
```

## Pruebas
```bash
pytest --cov
```

## Flujo de ramas
`feature/*` → `develop` → `test` → `main`. Hotfix: `hotfix/*` → `main` y `develop`.
(Puedes incluir el diagrama mermaid de la Guía 2.)

## CI/CD
Describe cada workflow: qué lo dispara y qué hace.

## Despliegues
- Producción (Render): https://<app>.onrender.com
- Servidor propio: http://localhost:8000 (actualizado automáticamente desde `main`)

## Autor
Nombre - [@usuario](https://github.com/usuario)

## Licencia
Distribuido bajo la licencia GPL-3.0. Ver `LICENSE`.
````

> Las insignias (badges) del CI y SonarQube funcionarán cuando configures esas partes (Guía 6).

---

## Paso 4. Crear las ramas permanentes

```bash
git switch main
git pull
git switch -c develop
git push -u origin develop
git switch -c test
git push -u origin test
git switch develop
git branch -a
```

Deben aparecer `main`, `develop` y `test` locales y remotas.

**Rama por defecto:** déjala en `main` (**Settings → General → Default branch**). Así:
- Las palabras `Closes #n` cierran issues cuando el cambio llega a producción.
- SonarQube Cloud analizará `main` como rama principal.

> Consecuencia: al abrir un PR, GitHub propone `main` como destino. **Cámbialo siempre a `develop`** para las features.

---

## Paso 5. Ajustes generales de Pull Requests

**Settings → General → sección "Pull Requests":**

| Opción | Valor | Por qué |
|---|---|---|
| Allow merge commits | ✅ | Es la estrategia del curso (conserva microcommits) |
| Allow squash merging | ❌ (opcional) | Evita perder microcommits por error |
| Allow rebase merging | ❌ (opcional) | Igual |
| Always suggest updating pull request branches | ✅ | Muestra botón para actualizar la rama con su base |
| **Automatically delete head branches** | **❌ DESACTIVADO** | Las ramas se conservan para la evaluación |

---

## Paso 6. Reglas de protección de ramas

GitHub tiene dos sistemas: *Branch protection rules* (clásico) y **Rulesets** (moderno). Usaremos **Rulesets**.

### ¿Por qué 0 aprobaciones?

GitHub **no permite que el autor apruebe su propio PR**. Si exiges 1 aprobación trabajando solo, **nunca podrás fusionar**. La solución es:

- **Exigir PR** (no se puede hacer push directo) ✅
- **0 aprobaciones requeridas** ✅
- **CI obligatorio en verde** ✅ (la "revisión automática")
- **Conversaciones resueltas** ✅ (obliga a cerrar tus comentarios de autorrevisión)

La autorrevisión queda como evidencia en los comentarios y en la checklist del PR (Guía 2, sección 6).

### 6.1 Ruleset para las ramas permanentes

1. **Settings → Rules → Rulesets → New ruleset → New branch ruleset**.
2. **Ruleset name:** `proteccion-ramas-permanentes`.
3. **Enforcement status:** **Active**.
4. **Bypass list:** **déjala vacía**. Si te agregas, podrías saltarte las reglas (y el evaluador lo verá).
5. **Target branches → Add target → Include by pattern**, agrega tres patrones: `main`, `develop`, `test`.
6. En **Branch rules** marca:

| Regla | Valor | Qué impide / exige |
|---|---|---|
| ✅ Restrict deletions | — | Nadie puede borrar la rama |
| ✅ Require a pull request before merging | Required approvals: **0** | Prohíbe el push directo; todo entra por PR |
| ↳ ✅ Require conversation resolution before merging | — | Todos los comentarios del PR deben estar resueltos |
| ↳ Allowed merge methods | Merge (y lo que hayas permitido en el paso 5) | |
| ✅ Require status checks to pass | *(se completa en la Guía 6, cuando exista el CI)* | El CI debe pasar para fusionar |
| ✅ Block force pushes | — | Nadie puede reescribir el historial |
| ☐ Require linear history | **NO marcar** | Es incompatible con los merge commits del curso |
| ☐ Require signed commits | Opcional (bonus) | Solo commits firmados (Guía 1, sección 1) |

7. **Create**.

### 6.2 Ruleset para conservar ramas de trabajo

Para que tampoco se borren las `feature/*` y `hotfix/*` (necesarias en la evaluación):

1. **New branch ruleset** → nombre `conservar-ramas-trabajo` → **Active** → bypass vacío.
2. Target: `feature/**` y `hotfix/**`.
3. Marca solo **Restrict deletions**.
4. **Create**.

> No marques aquí *Require a pull request*: en tus ramas de trabajo **sí** debes poder hacer push directo.

### 6.3 Agregar los checks obligatorios (después de la Guía 6)

Cuando tu workflow de CI haya corrido al menos una vez:

1. Edita `proteccion-ramas-permanentes` → **Require status checks to pass** → **Add checks**.
2. Escribe el nombre del job (por ejemplo `tests`) y selecciónalo.
3. Opcional: ✅ **Require branches to be up to date before merging**.
4. **Save changes**.

---

## Paso 7. Permisos de GitHub Actions

**Settings → Actions → General:**

| Sección | Valor | Por qué |
|---|---|---|
| Actions permissions | Allow all actions and reusable workflows | Para usar acciones del Marketplace |
| **Approval for running fork pull request workflows from contributors** | **Require approval for all external contributors** | **Crítico** para el runner self-hosted: evita que un desconocido haga un fork, abra un PR y ejecute código en tu PC |
| Workflow permissions | Read repository contents and packages permissions | Mínimo privilegio. Cada workflow pedirá permisos extra con `permissions:` |
| Allow GitHub Actions to create and approve pull requests | ❌ | Que un bot no se salte la revisión |

---

## Paso 8. Seguridad del código

**Settings → Security → Advanced Security** (en algunas cuentas aparece como **Code security**). En repos públicos todo esto es gratuito:

| Opción | Acción | Qué hace |
|---|---|---|
| Dependency graph | Enable | Mapa de tus dependencias |
| Dependabot alerts | Enable | Te avisa si una dependencia tiene vulnerabilidades conocidas |
| Dependabot security updates | Enable | Abre PRs automáticos para actualizar dependencias vulnerables |
| Secret scanning | Enable | Detecta tokens y contraseñas subidos |
| **Push protection** | Enable | **Bloquea** el push si contiene un secreto detectable |
| CodeQL analysis (Code scanning) | Set up → Default | Análisis estático de seguridad (complementa a SonarQube) |

Opcional: archivo `SECURITY.md` en la raíz con instrucciones para reportar vulnerabilidades.

---

## Paso 9. Plantillas de PR e issues

Crea estos archivos en una rama `feature/1-configuracion-repositorio` (el primer issue del tablero) y súbelos con un PR a `develop`. **Es tu primer PR del proyecto.**

### Plantilla de Pull Request · `.github/pull_request_template.md`

```markdown
## ¿Qué cambia?
<!-- Lista corta de cambios -->

## ¿Por qué?
<!-- Motivo del cambio -->

## ¿Cómo probarlo?
1.
2.

## Issue relacionado
Closes #

## Checklist de autorrevisión
- [ ] Revisé todos los archivos en "Files changed" y los marqué como "Viewed"
- [ ] Dejé al menos un comentario de revisión (o confirmé que no había cambios por hacer)
- [ ] No hay código de depuración ni comentado de más
- [ ] No subí secretos (.env, tokens, contraseñas)
- [ ] Los tests pasan localmente
- [ ] El CI está en verde
- [ ] La rama destino (base) es la correcta
- [ ] Actualicé la documentación si era necesario
```

### Plantillas de issues · `.github/ISSUE_TEMPLATE/`

`feature.md`:

```markdown
---
name: Funcionalidad
about: Nueva funcionalidad o tarea
title: "feat: "
labels: feature
assignees: ""
---

## Descripción
Como <tipo de usuario> quiero <acción> para <beneficio>.

## Criterios de aceptación
- [ ]
- [ ]

## Notas técnicas
```

`bug.md`:

```markdown
---
name: Error
about: Reportar un error
title: "bug: "
labels: bug
assignees: ""
---

## Descripción del error

## Pasos para reproducirlo
1.
2.

## Comportamiento esperado

## Comportamiento actual

## Entorno (rama / versión / despliegue)
```

### Opcional: CODEOWNERS · `.github/CODEOWNERS`

```
* @<tu-usuario>
```

Te asigna automáticamente como revisor de todos los PR.

---

## Paso 10. Labels y milestone

### Labels

**Issues → Labels → New label.** Sugeridas:

| Label | Color sugerido | Uso |
|---|---|---|
| `feature` | Verde | Nueva funcionalidad |
| `bug` | Rojo | Error |
| `hotfix` | Rojo oscuro | Error urgente en producción |
| `docs` | Azul | Documentación |
| `ci/cd` | Morado | Pipelines y despliegues |
| `docker` | Celeste | Contenedores |
| `test` | Amarillo | Pruebas |

### Milestone

**Issues → Milestones → New milestone:**
- Title: `Entrega final`
- Due date: `2026-11-25`

Asigna todos los issues a este milestone; GitHub mostrará el porcentaje de avance.

---

## Paso 11. Tablero Kanban con GitHub Projects

### 11.1 Crear el proyecto

1. En tu **perfil** (o desde el repo: pestaña **Projects → Link a project → New project**).
2. Elige la plantilla **Kanban** (o **Board**).
3. Nombre: `Proyecto final - <nombre>`.
4. **Create project**.

### 11.2 Configurar columnas

El tablero se basa en el campo **Status**. Ajusta las columnas así (menú `...` de cada columna para renombrar, o **+** para agregar):

| Columna | Significado |
|---|---|
| **Backlog** | Ideas y tareas identificadas, sin priorizar |
| **Todo** | Tareas priorizadas para hacer pronto |
| **In progress** | En desarrollo (existe la rama `feature/*`) |
| **In review** | PR abierto, en autorrevisión o esperando CI |
| **Done** | PR fusionado |

Opcional: en **In progress** pon un **límite WIP** (por ejemplo 2). El límite WIP evita empezar muchas cosas sin terminar ninguna; es el corazón de Kanban.

### 11.3 Vincular el repositorio

En el proyecto: menú `...` (arriba a la derecha) → **Settings → Manage access** o, desde el repo, pestaña **Projects → Link a project**. Así los issues del repo pueden agregarse al tablero.

### 11.4 Automatizaciones (Workflows)

Proyecto → `...` → **Workflows**. Activa:

| Workflow | Configuración |
|---|---|
| **Item added to project** | Status → `Todo` |
| **Auto-add to project** | Filtro `is:issue,pr is:open` del repo → los issues y PR nuevos entran solos |
| **Item closed** | Status → `Done` |
| **Pull request merged** | Status → `Done` |

> **Importante:** como la rama por defecto es `main`, un `Closes #7` en un PR hacia `develop` **no cierra el issue** al fusionar. Tienes dos opciones:
> 1. Al fusionar el PR en `develop`, cierra el issue manualmente con un comentario: *"Resuelto en #8"*.
> 2. Agrega también los PR al tablero: con el workflow **Pull request merged** el PR pasa a *Done*.
>
> El issue se cierra solo cuando el cambio llega a `main`.

### 11.5 Campos adicionales (opcional)

**+ → New field** en la vista de tabla:
- **Priority:** Single select (Alta, Media, Baja).
- **Estimate:** Number (horas).
- **Iteration:** sprints de una semana.

### 11.6 Cómo se usa día a día

1. Creas el issue con la plantilla → entra a **Todo**.
2. Creas la rama `feature/<n>-...` → mueves la tarjeta a **In progress**.
3. Abres el PR (con `Closes #n` o vinculando el issue en **Development**) → **In review**.
4. Fusionas → **Done**.

### 11.7 Backlog inicial sugerido para el proyecto final

| # | Issue |
|---|---|
| 1 | Configurar repositorio (licencia, README, plantillas, reglas) |
| 2 | Estructura inicial del proyecto |
| 3+ | Funcionalidades de tu aplicación (una por issue) |
| … | Dockerfile y docker-compose |
| … | Tests unitarios |
| … | Tests de integración |
| … | Workflow de CI |
| … | Integración con SonarQube |
| … | Despliegue en Vercel (bonus) |
| … | CD a Render |
| … | Runner self-hosted y CD a servidor propio |
| … | Documentación final en README |

---

## Paso 12. Secretos y variables

**Settings → Secrets and variables → Actions:**

- **Secrets** (cifrados, no se ven tras guardarlos): tokens y URLs privadas. Ejemplos del curso: `SONAR_TOKEN`, `RENDER_DEPLOY_HOOK`, `VERCEL_TOKEN`.
- **Variables** (texto visible): valores no sensibles, como `APP_URL`.

Se usan en los workflows así: `${{ secrets.SONAR_TOKEN }}`, `${{ vars.APP_URL }}`.

### Environments (recomendado)

**Settings → Environments → New environment** → `production`:
- Puedes guardar secretos solo para ese entorno.
- **Deployment branches and tags:** "Selected branches" → `main`. Así **solo `main` puede desplegar a producción**.
- En la pestaña **Code** del repo aparecerá un historial de despliegues.

---

## Paso 13. Verificación final

Prueba que todo funcione. **Estos errores son la prueba de que lo configuraste bien:**

```bash
# 1. Push directo a main → debe ser RECHAZADO
git switch main
git commit --allow-empty -m "test: prueba de protección"
git push
# remote: error: GH013: Repository rule violations found for refs/heads/main.
# remote: - Changes must be made through a pull request.
git reset --hard origin/main      # deshacer el commit de prueba

# 2. Borrar develop en el remoto → debe ser RECHAZADO
git push origin --delete develop

# 3. Force push a test → debe ser RECHAZADO
```

### Checklist

- [ ] Repositorio **público**
- [ ] `LICENSE` presente
- [ ] `README.md` con al menos instalación, uso y licencia
- [ ] `.gitignore` adecuado
- [ ] Ramas `main`, `develop`, `test` creadas
- [ ] "Automatically delete head branches" **desactivado**
- [ ] Ruleset de ramas permanentes **activo**, sin bypass
- [ ] Ruleset de conservación de `feature/**` y `hotfix/**`
- [ ] Push directo a `main` rechazado (probado)
- [ ] Aprobación de workflows de forks: "all external contributors"
- [ ] Dependabot, secret scanning y push protection activos
- [ ] Plantilla de PR y de issues subidas **mediante PR**
- [ ] Labels y milestone creados
- [ ] Tablero Kanban con 5 columnas y automatizaciones
- [ ] Backlog inicial cargado en el tablero
