# Guía 6 · CI/CD con GitHub Actions, GitHub Pages y SonarQube

> **Propósito:** entender la teoría de CI/CD y de la calidad de código, y montar un pipeline real sobre el proyecto de la **Guía 5**: lint → tests unitarios → tests de integración → análisis con SonarQube → publicación en GitHub Pages.
>
> **Requisitos:** el proyecto `gestor-tareas` de la Guía 5 en un repositorio **público** configurado según la Guía 3.
>
> **Todos los workflows de esta guía fueron validados** con `actionlint`. Las versiones de las acciones (`@v6`, `@v7`) eran las vigentes en noviembre de 2026; si alguna da error, revisa su versión actual en el [Marketplace](https://github.com/marketplace?type=actions).

---

## Índice

**Teoría**
1. [CI, Continuous Delivery y Continuous Deployment](#1-ci-continuous-delivery-y-continuous-deployment)
2. [Anatomía de un pipeline](#2-anatomía-de-un-pipeline)
3. [GitHub Actions: conceptos](#3-github-actions-conceptos)
4. [YAML en 5 minutos](#4-yaml-en-5-minutos)
5. [Calidad de código y SonarQube](#5-calidad-de-código-y-sonarqube)
6. [SonarQube Cloud vs SonarQube Community Build](#6-sonarqube-cloud-vs-sonarqube-community-build)

**Práctica**

7. [Práctica 1: workflow de CI con tests](#7-práctica-1-workflow-de-ci-con-tests)
8. [Práctica 2: análisis con SonarQube Cloud](#8-práctica-2-análisis-con-sonarqube-cloud)
9. [Práctica 3: despliegue en GitHub Pages](#9-práctica-3-despliegue-en-github-pages)
10. [Práctica 4: SonarQube Community Build en local con Docker](#10-práctica-4-sonarqube-community-build-en-local)
11. [Hacer obligatorios los checks](#11-hacer-obligatorios-los-checks)
12. [Referencia de GitHub Actions](#12-referencia-de-github-actions)
13. [Problemas frecuentes](#13-problemas-frecuentes)

---

# TEORÍA

## 1. CI, Continuous Delivery y Continuous Deployment

| Práctica | Definición | Pregunta que responde |
|---|---|---|
| **Integración Continua (CI)** | Cada cambio que se integra al repositorio se **construye y prueba automáticamente** | ¿Este cambio rompe algo? |
| **Entrega Continua (Continuous Delivery)** | Además, el código queda **siempre listo para desplegar**; el paso a producción es **manual** (un botón) | ¿Podríamos publicar ahora mismo? |
| **Despliegue Continuo (Continuous Deployment)** | Cada cambio que pasa el pipeline **se despliega solo** en producción, sin intervención humana | ¿Ya está en producción? |

```
 Código → Build → Tests → Análisis → Artefacto → [Aprobación manual] → Producción
 └────────────── CI ──────────────┘
 └──────────────────── Continuous Delivery ───────────────────────────┘
 └──────────────────── Continuous Deployment (sin aprobación manual) ─┘
```

**¿Por qué CI/CD?**
- Errores detectados en minutos, no en semanas.
- Integraciones pequeñas y frecuentes = menos conflictos (encaja con los microcommits).
- Despliegues repetibles y aburridos: siempre igual, sin "pasos que solo sabe hacer Juan".
- Retroalimentación rápida: cada PR muestra ✅ o ❌.

**Relación con DevOps:** DevOps es una cultura que une desarrollo (Dev) y operaciones (Ops). CI/CD es su práctica técnica central, junto con la infraestructura como código, el monitoreo y los contenedores.

---

## 2. Anatomía de un pipeline

```mermaid
flowchart LR
    A[Push / PR] --> B[Checkout]
    B --> C[Lint]
    C --> D[Tests unitarios]
    D --> E[Tests de integración]
    E --> F[Cobertura]
    F --> G[SonarQube<br/>Quality Gate]
    G --> H{¿Rama main?}
    H -- No --> I[Fin: ✅ en el PR]
    H -- Sí --> J[Build imagen Docker]
    J --> K[Deploy]
    K --> L[Smoke test /health]
```

Principios:
- **Falla rápido:** lo barato primero (lint, unitarios), lo caro después.
- **Construye una vez, despliega muchas:** la misma imagen Docker va a todos los entornos.
- **El pipeline es código:** vive en el repositorio (`.github/workflows/`), se versiona y se revisa con PR.
- **Rojo = se detiene todo:** nadie fusiona con el CI fallando.

---

## 3. GitHub Actions: conceptos

| Concepto | Qué es | En el YAML |
|---|---|---|
| **Workflow** | Proceso automatizado definido en un archivo YAML dentro de `.github/workflows/` | El archivo completo |
| **Evento** | Lo que dispara el workflow: push, PR, tag, horario, manual | `on:` |
| **Job** | Conjunto de pasos que corre en **una máquina**. Los jobs corren en paralelo salvo que uno dependa de otro | `jobs:` |
| **Step** | Un paso: un comando o una acción | `steps:` |
| **Action** | Paso reutilizable publicado por alguien (checkout, setup-python...) | `uses:` |
| **Runner** | La máquina que ejecuta el job. **GitHub-hosted** (máquina virtual de GitHub, se borra al terminar) o **self-hosted** (tu propia máquina, Guía 7) | `runs-on:` |
| **Artefacto** | Archivo que un job guarda para otro job o para descargar | `upload-artifact` |
| **Secreto** | Valor cifrado (tokens) | `${{ secrets.X }}` |
| **Environment** | Entorno de despliegue con reglas y secretos propios | `environment:` |
| **Matriz** | Ejecutar el mismo job con varias combinaciones (versiones de Python, SO) | `strategy.matrix` |
| **`GITHUB_TOKEN`** | Token automático que GitHub crea en cada ejecución, con los permisos de `permissions:` | `${{ secrets.GITHUB_TOKEN }}` |

### Eventos más usados

```yaml
on:
  push:
    branches: [main, develop]
    tags: ["v*"]                 # al subir un tag v1.0.0
    paths-ignore: ["**.md"]      # no correr si solo cambió documentación
  pull_request:
    branches: [develop, test, main]
  workflow_dispatch:             # botón "Run workflow" manual
  schedule:
    - cron: "0 6 * * 1"          # lunes 6:00 UTC
  workflow_run:                  # cuando otro workflow termina
    workflows: ["CI"]
    types: [completed]
```

### Minutos gratuitos

En **repositorios públicos**, los runners estándar de GitHub son **gratuitos**. Los runners self-hosted siempre son gratuitos (usan tu máquina).

---

## 4. YAML en 5 minutos

```yaml
# comentario
clave: valor
texto: "con comillas si tiene caracteres especiales: como estos"
numero: 3
booleano: true
lista:
  - uno
  - dos
lista_corta: [uno, dos]
objeto:
  nombre: Ana
  edad: 30
texto_multilinea: |
  línea 1
  línea 2
texto_plegado: >
  todo esto se une
  en una sola línea
```

> ⚠️ **YAML usa espacios, nunca tabulaciones.** La indentación define la estructura: un espacio de más o de menos rompe el archivo.

---

## 5. Calidad de código y SonarQube

### 5.1 ¿Qué es el análisis estático?

Examinar el código **sin ejecutarlo** para encontrar errores, vulnerabilidades y malas prácticas. Complementa a los tests: los tests verifican el comportamiento; el análisis estático, la calidad interna.

### 5.2 Qué mide SonarQube

SonarQube clasifica los problemas por la **cualidad del software** que afectan:

| Cualidad | Qué detecta | Ejemplo |
|---|---|---|
| **Seguridad** (vulnerabilidades) | Código explotable | SQL armado concatenando texto del usuario, contraseñas en el código |
| **Fiabilidad** (bugs) | Código que probablemente falla | Variable usada antes de asignarse, condición siempre verdadera |
| **Mantenibilidad** (code smells) | Código difícil de entender o cambiar | Funciones enormes, complejidad alta, código duplicado, nombres confusos |

Además:
- **Security Hotspots:** código sensible que **una persona debe revisar** (no necesariamente es un error). Ejemplo: uso de expresiones regulares, configuración de CORS.
- **Severidad:** Blocker, High, Medium, Low, Info.
- **Calificaciones (A–E):** A es la mejor. Hay una para seguridad, fiabilidad y mantenibilidad.
- **Cobertura:** la importa de tu reporte de tests (`coverage.xml`).
- **Duplicaciones:** porcentaje de líneas duplicadas.
- **Deuda técnica:** tiempo estimado para corregir todos los code smells.
- **Complejidad ciclomática / cognitiva:** qué tan difícil es seguir el flujo del código.

### 5.3 Quality Profile y Quality Gate

- **Quality Profile:** el conjunto de **reglas** que se aplican por lenguaje (por defecto, *Sonar way*).
- **Quality Gate:** las **condiciones para aprobar**. Si no se cumplen, el análisis falla y el pipeline se pone en rojo.

El Quality Gate por defecto (*Sonar way*) se aplica al **código nuevo** y exige, aproximadamente:

| Condición sobre el código nuevo | Valor |
|---|---|
| Problemas nuevos | 0 |
| Security Hotspots revisados | 100 % |
| Cobertura | ≥ 80 % |
| Líneas duplicadas | ≤ 3 % |

### 5.4 Clean as You Code

Filosofía de SonarQube: **no te obsesiones con el código heredado; asegúrate de que todo código nuevo sea limpio**. Por eso el Quality Gate se evalúa sobre el *new code* (lo cambiado desde la versión anterior o en los últimos N días). Con el tiempo, el proyecto completo mejora.

---

## 6. SonarQube Cloud vs SonarQube Community Build

Usaremos **las dos**, cada una con un propósito distinto.

| | **SonarQube Cloud** (antes SonarCloud) | **SonarQube Community Build** (antes Community Edition) |
|---|---|---|
| Dónde corre | En los servidores de Sonar (SaaS) | En tu máquina o servidor (Docker) |
| Costo | Gratis para **repositorios públicos** | Gratis y de código abierto (LGPL) |
| Instalación | Ninguna: inicias sesión con GitHub | La administras tú (Docker, base de datos, actualizaciones) |
| Integración con GitHub Actions | Directa: el runner de GitHub llega a la nube | Difícil: GitHub no puede llegar a tu `localhost:9000` (salvo runner self-hosted) |
| Análisis de PR y ramas | Depende del plan: en el plan **Free** puede estar limitado a la rama principal; Sonar anunció un plan **OSS gratuito para proyectos públicos** con análisis de ramas y PR. Revisa el plan de tu organización | **No**: solo analiza **una rama** (la principal) |
| Comentarios en el PR | Sí (en los planes que analizan PRs) | No |
| Lenguajes | Más de 30 | Menos (no incluye C, C++, Swift, entre otros) |
| Datos | En la nube de Sonar | Se quedan en tu máquina |
| Funciona sin internet | No | Sí |

### ¿Por qué usar cada una?

- **SonarQube Cloud → para el pipeline de CI.** Es la opción realista para integrar el análisis en GitHub Actions sin montar infraestructura: el Quality Gate se convierte en un check del PR y bloquea código de mala calidad. Así trabajan la mayoría de proyectos open source.
- **SonarQube Community Build → para aprender cómo funciona por dentro y para entornos privados.** Muchas empresas no pueden enviar su código a la nube (bancos, gobierno, salud) y lo instalan en sus propios servidores. Montarlo con Docker te enseña la arquitectura (servidor web, motor de búsqueda, base de datos, scanner) y te deja analizar sin depender de internet. Además, con el runner self-hosted de la Guía 7 podrías conectarlo a tu CI (bonus).

---

# PRÁCTICA

> Todo lo que sigue se hace **respetando el flujo**: crea un issue, una rama `feature/<n>-...`, microcommits y PR hacia `develop`.

## 7. Práctica 1: workflow de CI con tests

### 7.1 Crear el workflow

```bash
git switch develop && git pull
git switch -c feature/8-workflow-ci
mkdir -p .github/workflows
```

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  pull_request:
    branches: [develop, test, main]
  push:
    branches: [develop, test, main]
  workflow_dispatch:

# Mínimo privilegio: el GITHUB_TOKEN solo puede leer el código
permissions:
  contents: read

# Si subes otro commit a la misma rama, cancela la ejecución anterior
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6                 # descarga el código
      - uses: actions/setup-python@v6             # instala Python
        with:
          python-version: "3.12"
          cache: pip                              # cachea dependencias entre ejecuciones
      - run: pip install ruff==0.8.4
      - name: Revisar estilo y errores
        run: ruff check src tests

  tests:
    name: tests
    runs-on: ubuntu-latest
    needs: lint                                   # solo corre si lint pasó
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: pip
      - name: Instalar dependencias
        run: pip install -r requirements-dev.txt
      - name: Tests unitarios
        run: pytest -m unit --cov --cov-report=
      - name: Tests de integración
        run: pytest -m integration --cov --cov-append --cov-report=xml --cov-report=html --cov-report=term --cov-fail-under=80
      - name: Guardar reporte de cobertura
        uses: actions/upload-artifact@v4
        with:
          name: cobertura
          path: |
            coverage.xml
            htmlcov/

  sonarqube:
    name: sonarqube
    runs-on: ubuntu-latest
    needs: tests
    # Los PR desde forks no reciben secretos: en ese caso se omite el análisis
    if: ${{ github.event_name == 'push' || github.event.pull_request.head.repo.full_name == github.repository }}
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0                          # SonarQube necesita el historial completo
      - name: Descargar reporte de cobertura
        uses: actions/download-artifact@v4
        with:
          name: cobertura
      - name: Análisis con SonarQube Cloud
        uses: SonarSource/sonarqube-scan-action@v7
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.qualitygate.wait=true
```

**Cómo leerlo:**

- Se dispara en PRs y pushes hacia `develop`, `test` y `main`, y también manualmente.
- `lint` → `tests` → `sonarqube` corren en cadena gracias a `needs`.
- En `tests`, los unitarios y los de integración son **pasos separados**: en la interfaz verás cuál falló. `--cov-append` suma la cobertura de ambos.
- `--cov-fail-under=80` hace fallar el job si la cobertura baja del 80 %.
- El reporte se guarda como **artefacto**: lo usa el job de SonarQube y también puedes descargarlo desde la ejecución.
- `-Dsonar.qualitygate.wait=true` hace que el paso **falle si el Quality Gate falla**.

> El job `sonarqube` fallará hasta que completes la [Práctica 2](#8-práctica-2-análisis-con-sonarqube-cloud). Puedes hacer primero la práctica 2 o comentar ese job temporalmente.

### 7.2 Subir y ver el pipeline

```bash
git add .github/workflows/ci.yml
git commit -m "ci: agrega workflow con lint, tests unitarios y de integración"
git push -u origin feature/8-workflow-ci
gh pr create --base develop --fill
```

1. En el PR, sección de checks al final: verás `CI / lint`, `CI / tests`, `CI / sonarqube`.
2. Pestaña **Actions** del repo → clic en la ejecución → clic en un job → despliega cada paso para ver los logs.
3. Al final de la ejecución, sección **Artifacts** → descarga `cobertura` y abre `htmlcov/index.html`.

### 7.3 Provocar un fallo (aprendizaje)

1. En tu rama, rompe un test a propósito (por ejemplo, cambia `66.67` por `66.66` en `test_logica.py`).
2. Commit y push: el PR se pone en ❌ y el botón de merge queda bloqueado (si ya configuraste los checks obligatorios, [sección 11](#11-hacer-obligatorios-los-checks)).
3. Abre el log: pytest muestra exactamente qué esperaba y qué obtuvo.
4. Corrige con otro commit (`fix(test): ...`) y observa cómo vuelve a ✅.

### 7.4 Extra: tests contra un PostgreSQL real en el CI

Si tu proyecto usa una base de datos de verdad, el runner puede levantarla como **servicio**:

```yaml
  tests-postgres:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: tareas_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U test"
          --health-interval 5s
          --health-retries 10
    env:
      DATABASE_URL: postgresql://test:test@localhost:5432/tareas_test
    steps:
      - uses: actions/checkout@v6
      - run: echo "Aquí van tus tests de integración, que leen DATABASE_URL"
```

### 7.5 Extra: matriz de versiones

```yaml
  tests:
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
```

---

## 8. Práctica 2: análisis con SonarQube Cloud

### 8.1 Crear la cuenta e importar el repositorio

1. Entra a <https://sonarcloud.io> → **Log in → GitHub** y autoriza.
2. **+ (arriba a la derecha) → Analyze new project** (o *Import an organization*).
3. Importa tu **organización** de GitHub (tu cuenta personal cuenta como organización). Instala la app de SonarQube Cloud en GitHub y dale acceso **solo al repositorio** del proyecto.
4. Elige el plan **gratuito** (Free u OSS, según lo que ofrezca para proyectos públicos).
5. Selecciona el repositorio → **Set up**.
6. **Definición de código nuevo (new code):** elige *Previous version* (todo lo cambiado desde la última versión) o *Number of days* (por ejemplo, 30). Para el proyecto final, *Previous version* encaja con los tags.

### 8.2 Desactivar el análisis automático

SonarQube Cloud ofrece un **Automatic Analysis** que no usa tu CI y **no importa la cobertura**. Como queremos el análisis dentro del pipeline:

**Project → Administration → Analysis Method → desactiva "Automatic Analysis"** y elige **GitHub Actions**. Si no lo desactivas, el análisis del workflow fallará con un mensaje indicando que el análisis automático está activo.

### 8.3 Crear el token y el secreto

1. En la pantalla del método **GitHub Actions**, SonarQube Cloud te muestra un `SONAR_TOKEN` (o créalo en **My Account → Security → Generate Tokens**).
2. En GitHub: **Settings → Secrets and variables → Actions → New repository secret**:
   - Name: `SONAR_TOKEN`
   - Secret: el token copiado.

### 8.4 Archivo de configuración

En la raíz del repositorio, `sonar-project.properties`:

```properties
# Los copias de la pantalla de configuración de SonarQube Cloud
sonar.projectKey=<usuario>_gestor-tareas
sonar.organization=<usuario>

sonar.projectName=Gestor de Tareas
sonar.sources=src
sonar.tests=tests
sonar.python.version=3.12
sonar.python.coverage.reportPaths=coverage.xml
sonar.sourceEncoding=UTF-8
```

| Propiedad | Para qué |
|---|---|
| `sonar.projectKey` / `sonar.organization` | Identifican tu proyecto en SonarQube Cloud |
| `sonar.sources` | Código de producción que se analiza |
| `sonar.tests` | Código de tests (se analiza con reglas de tests y no cuenta para cobertura) |
| `sonar.python.coverage.reportPaths` | Dónde está el reporte de cobertura |
| `sonar.exclusions` | Archivos a ignorar, por ejemplo `**/migrations/**` |

Para otros lenguajes, la propiedad de cobertura cambia: JS/TS `sonar.javascript.lcov.reportPaths=coverage/lcov.info`, Java `sonar.coverage.jacoco.xmlReportPaths=...`, C# `sonar.cs.opencover.reportsPaths=...`, Go `sonar.go.coverage.reportPaths=coverage.out`.

```bash
git add sonar-project.properties
git commit -m "ci: agrega configuración de SonarQube Cloud"
git push
```

### 8.5 Ver los resultados

1. En el PR, el job `sonarqube` termina en ✅ si el Quality Gate pasa.
2. En SonarQube Cloud, abre tu proyecto:
   - **Overview:** Quality Gate (Passed/Failed), código nuevo vs código total.
   - **Issues:** cada problema con su explicación, la regla y cómo corregirlo.
   - **Security Hotspots:** revísalos y márcalos como *Safe* o *Fixed*.
   - **Measures:** cobertura, duplicaciones, complejidad, tamaño.
   - **Code:** navega los archivos con las líneas cubiertas/no cubiertas marcadas.
3. Dependiendo del plan, también verás el análisis del PR y un comentario automático de SonarQube en GitHub.

### 8.6 Insignia para el README

**Project → Information → Badges** (o la URL directa):

```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=<projectKey>&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=<projectKey>)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=<projectKey>&metric=coverage)](https://sonarcloud.io/summary/new_code?id=<projectKey>)
```

### 8.7 Ejercicio: provocar issues

Agrega en `logica.py` y sube en una rama de prueba:

```python
def buscar(conexion, texto):
    password = "admin123"                                       # secreto en el código
    return conexion.execute(f"SELECT * FROM tareas WHERE titulo = '{texto}'")  # inyección SQL
```

Observa qué reporta SonarQube, cómo cambia el Quality Gate y en qué categoría cae cada problema. Luego **no fusiones ese PR** (ciérralo).

---

## 9. Práctica 3: despliegue en GitHub Pages

GitHub Pages hospeda **sitios estáticos** (HTML, CSS, JS) gratis en repos públicos. No sirve para backends (Flask, Node con servidor), pero sí para documentación, frontends estáticos y **reportes**. Aquí publicaremos un sitio con el reporte de cobertura actualizado en cada cambio de `main`. Es un ejemplo de **Continuous Deployment**: nadie aprieta un botón.

### 9.1 Activar Pages

**Settings → Pages → Build and deployment → Source: GitHub Actions.**

### 9.2 Página de inicio

`docs/index.html`:

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gestor de Tareas · Reportes</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 720px; margin: 3rem auto; padding: 0 1rem; line-height: 1.6; }
    a.boton { display: inline-block; padding: .6rem 1rem; border-radius: .5rem; background: #2563eb; color: #fff; text-decoration: none; }
    footer { margin-top: 3rem; color: #666; font-size: .9rem; }
  </style>
</head>
<body>
  <h1>Gestor de Tareas</h1>
  <p>Sitio publicado automáticamente por GitHub Actions cada vez que se actualiza <code>main</code>.</p>
  <p><a class="boton" href="cobertura/index.html">Ver reporte de cobertura de tests</a></p>
  <footer>Commit <code>__COMMIT__</code> · generado el __FECHA__</footer>
</body>
</html>
```

### 9.3 Workflow

`.github/workflows/pages.yml`:

```yaml
name: Publicar en GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write        # publicar en Pages
  id-token: write     # verificar que el despliegue viene de este workflow

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  construir:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - name: Ejecutar tests y generar reporte HTML
        run: pytest --cov --cov-report=html
      - name: Armar el sitio
        run: |
          mkdir -p sitio
          cp docs/index.html sitio/
          cp -r htmlcov sitio/cobertura
          sed -i "s/__COMMIT__/${GITHUB_SHA::7}/; s/__FECHA__/$(date -u +'%Y-%m-%d %H:%M UTC')/" sitio/index.html
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v4
        with:
          path: sitio

  desplegar:
    needs: construir
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Desplegar
        id: deployment
        uses: actions/deploy-pages@v4
```

### 9.4 Llevarlo a producción siguiendo el flujo

```bash
git add docs/index.html .github/workflows/pages.yml
git commit -m "ci: publica reporte de cobertura en GitHub Pages"
git push
# PR feature → develop, luego develop → test, luego test → main
```

Cuando el PR hacia `main` se fusiona:
1. **Actions** muestra el workflow *Publicar en GitHub Pages*.
2. El job `desplegar` muestra la URL: `https://<usuario>.github.io/<repo>/`.
3. La página muestra el commit desplegado: cambia algo, llévalo a `main` y comprueba que el commit cambia solo.

> **Ambiente `github-pages`:** GitHub lo crea automáticamente y, por defecto, solo permite desplegar desde la rama por defecto. Si el despliegue falla con *"Branch is not allowed to deploy"*, revisa **Settings → Environments → github-pages → Deployment branches**.

---

## 10. Práctica 4: SonarQube Community Build en local

### 10.1 Preparar el sistema

SonarQube usa Elasticsearch internamente, que exige un límite de memoria virtual más alto:

```bash
sudo sysctl -w vm.max_map_count=524288
sudo sysctl -w fs.file-max=131072
# Para que sea permanente:
echo "vm.max_map_count=524288" | sudo tee /etc/sysctl.d/99-sonarqube.conf
echo "fs.file-max=131072" | sudo tee -a /etc/sysctl.d/99-sonarqube.conf
```

Necesitas al menos **4 GB de RAM libres** recomendables.

### 10.2 Levantarlo con Docker Compose

Crea una carpeta **fuera** de tu proyecto (por ejemplo `~/sonarqube`) con `compose.yaml`:

```yaml
services:
  sonarqube:
    image: sonarqube:community
    container_name: sonarqube
    depends_on:
      - db
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    ports:
      - "9000:9000"
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs

  db:
    image: postgres:16-alpine
    container_name: sonarqube-db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    volumes:
      - postgresql_data:/var/lib/postgresql/data

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  postgresql_data:
```

```bash
cd ~/sonarqube
docker compose up -d
docker compose logs -f sonarqube     # espera "SonarQube is operational" (1–3 min)
```

> La arquitectura que acabas de levantar: un **servidor web** (puerto 9000), un **motor de búsqueda** (Elasticsearch, interno), una **base de datos** (PostgreSQL) y, más adelante, el **scanner** (un cliente que analiza el código y envía los resultados).

### 10.3 Configuración inicial

1. Abre <http://localhost:9000> → usuario `admin`, contraseña `admin` → te obliga a cambiarla.
2. **Create a local project** (o *Create project → Local project*):
   - Project display name: `Gestor de Tareas`
   - Project key: `gestor-tareas`
   - Main branch name: `main`
3. New code: *Use the global setting* → **Create project**.
4. Analysis method: **Locally** → **Generate a token** → cópialo.

### 10.4 Analizar el proyecto

Desde la carpeta de tu proyecto, genera la cobertura y ejecuta el scanner **en un contenedor** (no hay que instalar nada):

```bash
cd ~/ruta/gestor-tareas
pytest --cov --cov-report=xml

docker run --rm --network host \
  -e SONAR_HOST_URL="http://localhost:9000" \
  -e SONAR_TOKEN="<tu-token-local>" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=gestor-tareas \
  -Dsonar.sources=src \
  -Dsonar.tests=tests \
  -Dsonar.python.version=3.12 \
  -Dsonar.python.coverage.reportPaths=coverage.xml
```

> Los parámetros por línea de comandos tienen prioridad sobre `sonar-project.properties`. Así el mismo repositorio sirve para Cloud (archivo) y Community (comando), sin que `sonar.organization` moleste.

Al terminar, el log dice `ANALYSIS SUCCESSFUL` con un enlace. Recarga <http://localhost:9000>.

### 10.5 Comparar

Responde (útil para la defensa del proyecto final):
- ¿Los resultados coinciden con los de SonarQube Cloud? ¿Por qué podrían diferir? (versiones de reglas, perfiles, alcance del código nuevo).
- ¿Qué pasa si analizas otra rama en Community? (sobrescribe el análisis: solo existe una rama).
- ¿Qué ventajas tendría Community para una empresa con código confidencial?

### 10.6 Apagar

```bash
cd ~/sonarqube
docker compose down          # conserva los datos
docker compose down -v       # borra todo
```

---

## 11. Hacer obligatorios los checks

Cuando el CI haya corrido al menos una vez:

1. **Settings → Rules → Rulesets → `proteccion-ramas-permanentes`** (Guía 3).
2. ✅ **Require status checks to pass → Add checks** → busca y agrega: `lint`, `tests`, `sonarqube`.
3. Opcional: ✅ **Require branches to be up to date before merging**.
4. **Save changes**.

Desde ahora, **ningún PR hacia `develop`, `test` o `main` se puede fusionar si el CI está en rojo**. Esa es la "revisión automática" que reemplaza la aprobación de otra persona.

---

## 12. Referencia de GitHub Actions

### Contextos y expresiones

| Expresión | Valor |
|---|---|
| `${{ github.ref_name }}` | Nombre de la rama o tag (`main`, `v1.0.0`) |
| `${{ github.sha }}` | Hash del commit |
| `${{ github.event_name }}` | `push`, `pull_request`... |
| `${{ github.repository }}` | `usuario/repo` |
| `${{ github.actor }}` | Quién disparó el workflow |
| `${{ secrets.NOMBRE }}` | Un secreto |
| `${{ vars.NOMBRE }}` | Una variable |
| `${{ needs.job.outputs.x }}` | Salida de otro job |
| `${{ runner.os }}` | Sistema operativo del runner |

### Condiciones

```yaml
if: github.ref == 'refs/heads/main'
if: startsWith(github.ref, 'refs/tags/v')
if: github.event_name == 'push'
if: failure()          # solo si algo falló antes
if: always()           # siempre, aunque haya fallado
```

### Pasar datos entre pasos y jobs

```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      tag: ${{ steps.calc.outputs.tag }}
    steps:
      - id: calc
        run: echo "tag=v-${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"
  usar:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "La versión es ${{ needs.version.outputs.tag }}"
```

### Acciones más usadas

| Acción | Para qué |
|---|---|
| `actions/checkout` | Descargar el código |
| `actions/setup-python`, `setup-node`, `setup-java`, `setup-go` | Instalar el lenguaje |
| `actions/cache` | Cachear dependencias |
| `actions/upload-artifact` / `download-artifact` | Compartir archivos entre jobs |
| `docker/login-action` | Iniciar sesión en un registro |
| `docker/metadata-action` | Generar tags de imagen automáticamente |
| `docker/build-push-action` | Construir y subir imágenes |
| `actions/configure-pages`, `upload-pages-artifact`, `deploy-pages` | GitHub Pages |
| `SonarSource/sonarqube-scan-action` | SonarQube |

### Validar workflows en local (opcional)

- **actionlint** (<https://github.com/rhysd/actionlint>): encuentra errores de sintaxis y expresiones.
- **act** (<https://github.com/nektos/act>): ejecuta workflows en tu máquina con Docker.

---

## 13. Problemas frecuentes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'tareas'` | pytest no encuentra `src/` | Revisa `pythonpath = ["src"]` en `pyproject.toml` |
| El workflow no aparece en Actions | Archivo fuera de `.github/workflows/` o YAML inválido | Revisa la ruta y la indentación |
| SonarQube: *"Automatic Analysis is enabled"* | El análisis automático choca con el del CI | Desactívalo (8.2) |
| SonarQube: cobertura 0 % | No encuentra `coverage.xml` o las rutas no coinciden | `relative_files = true` en `pyproject.toml`; descarga el artefacto en la raíz |
| SonarQube: `Not authorized` | Falta `SONAR_TOKEN` o está mal | Revisa el secreto |
| SonarQube: *Project not found* | `projectKey` u `organization` incorrectos | Cópialos de la página del proyecto |
| Pages: 404 | Pages no está en modo *GitHub Actions* o aún no termina | Revisa Settings → Pages |
| Pages: *Branch is not allowed to deploy* | Reglas del ambiente `github-pages` | Settings → Environments → github-pages |
| Community Build no arranca: `max virtual memory areas vm.max_map_count [65530] is too low` | Límite del kernel | `sudo sysctl -w vm.max_map_count=524288` |
| El check no aparece en "Add checks" | El job nunca corrió | Ejecuta el workflow una vez y vuelve a buscar |
