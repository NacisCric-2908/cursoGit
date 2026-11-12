# Gestor de Tareas (proyecto de ejemplo)

Proyecto de referencia para las guías del curso de Git/GitHub. Es una API REST en Python/Flask con SQLite que incluye todo lo que pide el proyecto final: tests unitarios y de integración, Docker, CI con SonarQube, GitHub Pages y CD a Render y a un servidor propio con runner self-hosted.

> Reemplaza `usuario` por tu usuario de GitHub en `sonar-project.properties` y `compose.prod.yaml`.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la aplicación |
| GET | `/version` | Commit desplegado |
| GET | `/tareas` | Lista de tareas |
| POST | `/tareas` | Crea una tarea `{"titulo": "...", "prioridad": "baja\|media\|alta"}` |
| PATCH | `/tareas/<id>/completar` | Marca una tarea como completada |
| DELETE | `/tareas/<id>` | Elimina una tarea |
| GET | `/progreso` | Porcentaje de tareas completadas |

## Desarrollo local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -m unit                 # tests unitarios
pytest -m integration          # tests de integración
pytest --cov                   # todos, con cobertura
ruff check src tests           # linter
```

## Con Docker

```bash
docker compose up -d --build
curl localhost:8000/health
```

## Estructura

```
src/tareas/        código de la aplicación (lógica, repositorio, API)
tests/unit/        tests unitarios (con mocks)
tests/integration/ tests de integración (SQLite real)
.github/workflows/ ci.yml, cd.yml, pages.yml
scripts/           desplegar.sh (servidor propio), reporte_sonar.sh
docs/              página publicada en GitHub Pages
```

## Licencia

GPL-3.0 (agrega el archivo LICENSE al crear tu repositorio).
