# Guía 5 · Pruebas de código: teoría y práctica en Python

> **Propósito:** entender qué tipos de pruebas existen, para qué sirve cada uno, y practicar **tests unitarios** y **tests de integración** con `pytest`. El proyecto de esta guía se reutiliza en la **Guía 6** (CI/CD).
>
> **Requisitos:** Python 3.10 o superior y Git.

---

## Índice

1. [¿Por qué probar?](#1-por-qué-probar)
2. [Tipos de pruebas](#2-tipos-de-pruebas)
3. [La pirámide de pruebas](#3-la-pirámide-de-pruebas)
4. [Conceptos clave](#4-conceptos-clave)
5. [Práctica: proyecto "gestor de tareas"](#5-práctica-proyecto-gestor-de-tareas)
6. [Tests unitarios](#6-tests-unitarios)
7. [Tests unitarios con dobles (Mock)](#7-tests-unitarios-con-dobles-mock)
8. [Tests de integración](#8-tests-de-integración)
9. [Ejecutar, filtrar y medir cobertura](#9-ejecutar-filtrar-y-medir-cobertura)
10. [Referencia rápida de pytest](#10-referencia-rápida-de-pytest)
11. [Ejercicios](#11-ejercicios)
12. [Si tu proyecto final no es en Python](#12-si-tu-proyecto-final-no-es-en-python)

---

## 1. ¿Por qué probar?

- **Detectar errores antes que el usuario.** Un error en producción cuesta mucho más que uno en desarrollo.
- **Cambiar sin miedo.** Con buenos tests puedes refactorizar y saber al instante si rompiste algo.
- **Documentación viva.** Un test muestra cómo se usa el código y qué se espera de él.
- **Habilitar CI/CD.** Sin tests automáticos, el despliegue automático es una ruleta: el pipeline no tiene cómo saber si el código funciona.

> "Las pruebas pueden mostrar la presencia de errores, pero nunca su ausencia." — Edsger Dijkstra

---

## 2. Tipos de pruebas

### 2.1 Por nivel (qué tanto del sistema involucran)

| Tipo | Qué prueba | Velocidad | Ejemplo |
|---|---|---|---|
| **Unitaria** | Una unidad aislada (función, método, clase) sin dependencias reales | Milisegundos | `validar_titulo("")` lanza error |
| **Integración** | Que varios componentes funcionen **juntos** (código + base de datos, API + servicio) | Segundos | Guardar una tarea en SQLite y leerla |
| **Sistema / End-to-End (E2E)** | El sistema completo como lo usaría el usuario | Minutos | Un navegador automatizado (Playwright, Selenium) abre la web, hace login y crea una tarea |
| **Aceptación (UAT)** | Que cumple los requisitos del cliente | Variable | "Como usuario quiero marcar tareas como completadas" se valida con el cliente |

### 2.2 Por propósito

| Tipo | Pregunta que responde | Herramientas típicas |
|---|---|---|
| **Funcional** | ¿Hace lo que debe? | pytest, unittest |
| **Regresión** | ¿Lo que funcionaba sigue funcionando tras el cambio? | Toda la suite automática en el CI |
| **Humo (smoke)** | ¿Arranca y responde lo básico? | `curl /health` después de desplegar |
| **Rendimiento / carga / estrés** | ¿Cuánto aguanta? ¿Qué tan rápido responde? | Locust, k6, JMeter |
| **Seguridad** | ¿Es vulnerable? | SonarQube, CodeQL, Bandit, OWASP ZAP |
| **Usabilidad** | ¿Es fácil de usar? | Pruebas con usuarios |
| **Análisis estático** | ¿El código tiene errores o malos olores sin ejecutarlo? | Linters (ruff, eslint), SonarQube |

### 2.3 Por conocimiento del código

- **Caja negra:** pruebas el comportamiento sin mirar el código (entradas → salidas esperadas).
- **Caja blanca:** diseñas las pruebas mirando el código, para recorrer todos los caminos (`if`, `else`, bucles).
- **Caja gris:** una mezcla de ambas (típico en tests de integración).

### 2.4 Manuales vs automáticas

Las **manuales** las ejecuta una persona siguiendo pasos; son útiles para explorar. Las **automáticas** son código que prueba código; son las únicas que sirven en CI/CD porque se ejecutan solas en cada cambio.

---

## 3. La pirámide de pruebas

```
              ▲  más lentas, frágiles y costosas
             ╱ ╲
            ╱E2E╲          pocas
           ╱─────╲
          ╱ Inte- ╲        algunas
         ╱ gración ╲
        ╱───────────╲
       ╱  Unitarias  ╲     muchas
      ╱───────────────╲
              ▼  más rápidas, estables y baratas
```

- **Base ancha de unitarias:** rápidas, precisas, se ejecutan en cada commit.
- **Capa media de integración:** verifican que las piezas encajan.
- **Pocas E2E:** las más realistas, pero lentas y frágiles.

**Antipatrón del "cono de helado":** muchas pruebas manuales y E2E, casi ninguna unitaria. El CI tarda horas y falla por motivos aleatorios.

---

## 4. Conceptos clave

### 4.1 Patrón AAA (Arrange, Act, Assert)

Todo test tiene tres partes:

```python
def test_validar_titulo_devuelve_titulo_limpio():
    # Arrange (preparar): los datos de entrada
    titulo = "   Comprar pan   "
    # Act (ejecutar): la acción que se prueba
    resultado = validar_titulo(titulo)
    # Assert (verificar): el resultado esperado
    assert resultado == "Comprar pan"
```

### 4.2 Principios FIRST

| Letra | Principio | Significa |
|---|---|---|
| **F** | Fast | Rápidos (si tardan, nadie los corre) |
| **I** | Independent | Independientes: no dependen del orden ni de otros tests |
| **R** | Repeatable | Repetibles: mismo resultado en cualquier máquina (sin depender de internet, hora o datos previos) |
| **S** | Self-validating | Autoverificables: pasan o fallan, sin revisar nada a mano |
| **T** | Timely | Oportunos: se escriben junto con el código (o antes, con TDD) |

### 4.3 Dobles de prueba

Para aislar una unidad se reemplazan sus dependencias por **dobles**:

| Doble | Qué hace | Ejemplo |
|---|---|---|
| **Dummy** | Se pasa pero no se usa | Un parámetro obligatorio vacío |
| **Stub** | Devuelve respuestas fijas | `repo.listar()` siempre devuelve 2 tareas |
| **Fake** | Implementación simplificada que funciona | Base de datos en memoria |
| **Mock** | Además de responder, **verifica cómo fue llamado** | "Se llamó `agregar('Estudiar', 'alta')` exactamente una vez" |
| **Spy** | Envuelve el objeto real y registra las llamadas | |

En Python: `unittest.mock.Mock`, `MagicMock`, `patch` y la fixture `monkeypatch` de pytest.

### 4.4 Cobertura de código

Porcentaje del código que se ejecuta durante los tests.

- **De líneas:** ¿qué líneas se ejecutaron?
- **De ramas (branch):** ¿se probaron el `if` y el `else`?

> ⚠️ **100 % de cobertura no significa cero errores.** Indica qué se ejecutó, no que se haya verificado bien. Una meta razonable es **≥ 80 %** en el código nuevo (es el valor por defecto del Quality Gate de SonarQube, Guía 6).

### 4.5 TDD (Test-Driven Development)

Ciclo **Rojo → Verde → Refactor**:
1. 🔴 Escribe un test que falla (la función aún no existe o no hace eso).
2. 🟢 Escribe el código mínimo para que pase.
3. 🔵 Mejora el código manteniendo los tests en verde.

Encaja perfecto con los microcommits: `test: ...` → `feat: ...` → `refactor: ...`.

---

## 5. Práctica: proyecto "gestor de tareas"

Una API web pequeña con Flask y SQLite. **Todo el código de esta guía está probado y funciona.**

### 5.1 Estructura

```
gestor-tareas/
├── src/
│   └── tareas/
│       ├── __init__.py
│       ├── logica.py          # reglas de negocio puras → tests unitarios
│       ├── repositorio.py     # acceso a SQLite       → tests de integración
│       └── app.py             # API Flask             → unitarios (mock) + integración
├── tests/
│   ├── unit/
│   │   ├── test_logica.py
│   │   └── test_api_con_mock.py
│   └── integration/
│       ├── test_repositorio.py
│       └── test_api.py
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

> **Diseño para probar:** separar la lógica pura (`logica.py`) del acceso a datos (`repositorio.py`) y de la web (`app.py`) hace que cada parte se pueda probar por separado. Además, `create_app(repositorio=...)` permite **inyectar** un repositorio falso o uno real: eso se llama **inyección de dependencias**.

### 5.2 Preparar el entorno

```bash
mkdir -p gestor-tareas/src/tareas gestor-tareas/tests/unit gestor-tareas/tests/integration
cd gestor-tareas
git init
python3 -m venv .venv
source .venv/bin/activate
touch src/tareas/__init__.py
```

`requirements.txt` (para producción):

```
flask==3.1.0
gunicorn==23.0.0
```

`requirements-dev.txt` (para desarrollo y CI):

```
-r requirements.txt
pytest==8.3.4
pytest-cov==6.0.0
ruff==0.8.4
```

```bash
pip install -r requirements-dev.txt
```

`pyproject.toml` (configuración de pytest y cobertura):

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
markers = [
    "unit: tests unitarios (rápidos, sin dependencias externas)",
    "integration: tests de integración (base de datos real, varios componentes)",
]
addopts = "-ra --strict-markers"

[tool.coverage.run]
source = ["src"]
branch = true
relative_files = true

[tool.coverage.report]
show_missing = true
```

> `relative_files = true` es necesario para que SonarQube encuentre los archivos del reporte de cobertura (Guía 6).

### 5.3 El código

`src/tareas/logica.py`:

```python
"""Reglas de negocio puras: no tocan base de datos ni red."""

PRIORIDADES = ("baja", "media", "alta")
MAX_TITULO = 100


def validar_titulo(titulo):
    """Devuelve el título limpio o lanza ValueError si no es válido."""
    if titulo is None or not str(titulo).strip():
        raise ValueError("El título es obligatorio")
    limpio = str(titulo).strip()
    if len(limpio) > MAX_TITULO:
        raise ValueError(f"El título no puede superar {MAX_TITULO} caracteres")
    return limpio


def validar_prioridad(prioridad):
    """Normaliza la prioridad. Si no se envía, se usa 'media'."""
    valor = (prioridad or "media").strip().lower()
    if valor not in PRIORIDADES:
        raise ValueError(f"Prioridad inválida. Use una de: {', '.join(PRIORIDADES)}")
    return valor


def calcular_progreso(tareas):
    """Porcentaje de tareas completadas, con dos decimales."""
    if not tareas:
        return 0.0
    completadas = sum(1 for tarea in tareas if tarea["completada"])
    return round(completadas * 100 / len(tareas), 2)
```

`src/tareas/repositorio.py`:

```python
"""Acceso a datos con SQLite."""
import sqlite3


class RepositorioTareas:
    def __init__(self, ruta_db=":memory:"):
        self.conexion = sqlite3.connect(ruta_db, check_same_thread=False)
        self.conexion.row_factory = sqlite3.Row
        self._crear_tabla()

    def _crear_tabla(self):
        self.conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                prioridad TEXT NOT NULL DEFAULT 'media',
                completada INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self.conexion.commit()

    @staticmethod
    def _a_dict(fila):
        return {
            "id": fila["id"],
            "titulo": fila["titulo"],
            "prioridad": fila["prioridad"],
            "completada": bool(fila["completada"]),
        }

    def agregar(self, titulo, prioridad="media"):
        cursor = self.conexion.execute(
            "INSERT INTO tareas (titulo, prioridad) VALUES (?, ?)", (titulo, prioridad)
        )
        self.conexion.commit()
        return self.obtener(cursor.lastrowid)

    def obtener(self, id_tarea):
        fila = self.conexion.execute(
            "SELECT * FROM tareas WHERE id = ?", (id_tarea,)
        ).fetchone()
        return self._a_dict(fila) if fila else None

    def listar(self):
        filas = self.conexion.execute("SELECT * FROM tareas ORDER BY id").fetchall()
        return [self._a_dict(f) for f in filas]

    def completar(self, id_tarea):
        cursor = self.conexion.execute(
            "UPDATE tareas SET completada = 1 WHERE id = ?", (id_tarea,)
        )
        self.conexion.commit()
        return cursor.rowcount == 1

    def eliminar(self, id_tarea):
        cursor = self.conexion.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
        self.conexion.commit()
        return cursor.rowcount == 1

    def cerrar(self):
        self.conexion.close()
```

> Fíjate en los `?` de las consultas SQL: son **consultas parametrizadas** y evitan la inyección SQL. SonarQube marcaría como vulnerabilidad una consulta armada con `f"... WHERE id = {id}"`.

`src/tareas/app.py`:

```python
"""API web con Flask."""
import os

from flask import Flask, jsonify, request

from tareas.logica import calcular_progreso, validar_prioridad, validar_titulo
from tareas.repositorio import RepositorioTareas


def create_app(repositorio=None):
    app = Flask(__name__)
    repo = repositorio or RepositorioTareas(os.getenv("DB_PATH", "tareas.db"))

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/tareas")
    def listar_tareas():
        return jsonify(repo.listar())

    @app.post("/tareas")
    def crear_tarea():
        datos = request.get_json(silent=True) or {}
        try:
            titulo = validar_titulo(datos.get("titulo"))
            prioridad = validar_prioridad(datos.get("prioridad"))
        except ValueError as error:
            return jsonify(error=str(error)), 400
        return jsonify(repo.agregar(titulo, prioridad)), 201

    @app.patch("/tareas/<int:id_tarea>/completar")
    def completar_tarea(id_tarea):
        if not repo.completar(id_tarea):
            return jsonify(error="Tarea no encontrada"), 404
        return jsonify(repo.obtener(id_tarea))

    @app.delete("/tareas/<int:id_tarea>")
    def eliminar_tarea(id_tarea):
        if not repo.eliminar(id_tarea):
            return jsonify(error="Tarea no encontrada"), 404
        return "", 204

    @app.get("/progreso")
    def progreso():
        return jsonify(progreso=calcular_progreso(repo.listar()))

    return app
```

Probar a mano (opcional):

```bash
PYTHONPATH=src flask --app "tareas.app:create_app()" run
# en otra terminal:
curl -X POST localhost:5000/tareas -H "Content-Type: application/json" -d '{"titulo":"Estudiar Docker","prioridad":"alta"}'
curl localhost:5000/tareas
curl localhost:5000/progreso
```

---

## 6. Tests unitarios

Prueban la lógica pura, sin base de datos ni red. Son los más numerosos y rápidos.

`tests/unit/test_logica.py`:

```python
import pytest

from tareas.logica import calcular_progreso, validar_prioridad, validar_titulo

pytestmark = pytest.mark.unit      # todos los tests de este archivo son "unit"


# ---------- validar_titulo ----------
def test_validar_titulo_devuelve_titulo_limpio():
    # Arrange (preparar)
    titulo = "   Comprar pan   "
    # Act (ejecutar)
    resultado = validar_titulo(titulo)
    # Assert (verificar)
    assert resultado == "Comprar pan"


@pytest.mark.parametrize("titulo_invalido", [None, "", "    "])
def test_validar_titulo_vacio_lanza_error(titulo_invalido):
    with pytest.raises(ValueError, match="obligatorio"):
        validar_titulo(titulo_invalido)


def test_validar_titulo_demasiado_largo_lanza_error():
    with pytest.raises(ValueError, match="100 caracteres"):
        validar_titulo("a" * 101)


def test_validar_titulo_en_el_limite_es_valido():
    assert len(validar_titulo("a" * 100)) == 100


# ---------- validar_prioridad ----------
@pytest.mark.parametrize(
    "entrada, esperado",
    [("alta", "alta"), ("ALTA", "alta"), (" Baja ", "baja"), (None, "media"), ("", "media")],
)
def test_validar_prioridad_normaliza(entrada, esperado):
    assert validar_prioridad(entrada) == esperado


def test_validar_prioridad_invalida_lanza_error():
    with pytest.raises(ValueError, match="Prioridad inválida"):
        validar_prioridad("urgentísima")


# ---------- calcular_progreso ----------
def test_progreso_sin_tareas_es_cero():
    assert calcular_progreso([]) == 0.0


def test_progreso_con_tareas_mixtas():
    tareas = [{"completada": True}, {"completada": False}, {"completada": True}]
    assert calcular_progreso(tareas) == 66.67


def test_progreso_todas_completadas_es_cien():
    assert calcular_progreso([{"completada": True}] * 4) == 100.0
```

**Técnicas usadas:**

- **`pytest.raises`:** verifica que se lance una excepción (y con `match`, que su mensaje contenga un texto).
- **`@pytest.mark.parametrize`:** un mismo test con varios datos. El primer test parametrizado genera 3 casos; el de prioridad, 5.
- **Valores límite:** se prueban 100 caracteres (válido) y 101 (inválido). Los errores suelen esconderse en los bordes.
- **Partición de equivalencia:** se elige un representante de cada grupo de entradas (vacío, normal, demasiado largo).

---

## 7. Tests unitarios con dobles (Mock)

¿Cómo probar `app.py` **de forma unitaria** si usa un repositorio? Reemplazándolo por un `Mock`. Así probamos solo la lógica de las rutas: validación, códigos HTTP y que se llame al repositorio correctamente.

`tests/unit/test_api_con_mock.py`:

```python
"""Tests unitarios de la API: el repositorio se reemplaza por un doble (Mock).
Así probamos SOLO la lógica de las rutas, sin base de datos."""
from unittest.mock import Mock

import pytest

from tareas.app import create_app

pytestmark = pytest.mark.unit


@pytest.fixture
def repo_falso():
    return Mock()


@pytest.fixture
def cliente(repo_falso):
    app = create_app(repositorio=repo_falso)
    app.config["TESTING"] = True
    return app.test_client()


def test_health_responde_ok(cliente):
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"status": "ok"}


def test_crear_tarea_llama_al_repositorio_con_datos_validados(cliente, repo_falso):
    repo_falso.agregar.return_value = {
        "id": 1, "titulo": "Estudiar", "prioridad": "alta", "completada": False,
    }

    respuesta = cliente.post("/tareas", json={"titulo": "  Estudiar ", "prioridad": "ALTA"})

    assert respuesta.status_code == 201
    repo_falso.agregar.assert_called_once_with("Estudiar", "alta")


def test_crear_tarea_invalida_no_toca_el_repositorio(cliente, repo_falso):
    respuesta = cliente.post("/tareas", json={"titulo": ""})

    assert respuesta.status_code == 400
    repo_falso.agregar.assert_not_called()


def test_completar_tarea_inexistente_devuelve_404(cliente, repo_falso):
    repo_falso.completar.return_value = False

    respuesta = cliente.patch("/tareas/99/completar")

    assert respuesta.status_code == 404


def test_progreso_usa_las_tareas_del_repositorio(cliente, repo_falso):
    repo_falso.listar.return_value = [{"completada": True}, {"completada": False}]

    respuesta = cliente.get("/progreso")

    assert respuesta.get_json() == {"progreso": 50.0}
```

**Conceptos nuevos:**

- **Fixture (`@pytest.fixture`):** función que prepara algo reutilizable. pytest la inyecta en cualquier test que tenga un parámetro con su nombre. Las fixtures pueden usar otras fixtures (`cliente` usa `repo_falso`).
- **`Mock().metodo.return_value`:** define qué devuelve el doble (comportamiento de stub).
- **`assert_called_once_with(...)` / `assert_not_called()`:** verifican cómo fue usado (comportamiento de mock).
- **`app.test_client()`:** cliente HTTP falso de Flask; hace peticiones sin levantar un servidor.

---

## 8. Tests de integración

Ahora **sin dobles**: el código real habla con una base de datos SQLite real (en un archivo temporal).

`tests/integration/test_repositorio.py` · integración **código ↔ base de datos**:

```python
"""Integración código <-> base de datos SQLite real (archivo temporal)."""
import pytest

from tareas.repositorio import RepositorioTareas

pytestmark = pytest.mark.integration


@pytest.fixture
def repo(tmp_path):
    repositorio = RepositorioTareas(tmp_path / "test.db")
    yield repositorio          # el test se ejecuta aquí
    repositorio.cerrar()       # limpieza al terminar


def test_agregar_y_obtener(repo):
    creada = repo.agregar("Leer libro", "baja")

    assert creada["id"] == 1
    assert repo.obtener(1) == {
        "id": 1, "titulo": "Leer libro", "prioridad": "baja", "completada": False,
    }


def test_listar_devuelve_en_orden_de_creacion(repo):
    repo.agregar("Primera")
    repo.agregar("Segunda")

    titulos = [t["titulo"] for t in repo.listar()]

    assert titulos == ["Primera", "Segunda"]


def test_completar_actualiza_la_base(repo):
    tarea = repo.agregar("Hacer ejercicio")

    assert repo.completar(tarea["id"]) is True
    assert repo.obtener(tarea["id"])["completada"] is True


def test_completar_inexistente_devuelve_false(repo):
    assert repo.completar(123) is False


def test_eliminar(repo):
    tarea = repo.agregar("Temporal")

    assert repo.eliminar(tarea["id"]) is True
    assert repo.obtener(tarea["id"]) is None


def test_los_datos_persisten_al_reabrir(tmp_path):
    ruta = tmp_path / "persistente.db"
    primero = RepositorioTareas(ruta)
    primero.agregar("No me pierdas")
    primero.cerrar()

    segundo = RepositorioTareas(ruta)
    assert len(segundo.listar()) == 1
    segundo.cerrar()
```

`tests/integration/test_api.py` · integración **completa** (HTTP → Flask → lógica → repositorio → SQLite):

```python
"""Integración completa: HTTP -> Flask -> lógica -> repositorio -> SQLite."""
import pytest

from tareas.app import create_app
from tareas.repositorio import RepositorioTareas

pytestmark = pytest.mark.integration


@pytest.fixture
def cliente(tmp_path):
    repo = RepositorioTareas(tmp_path / "api.db")
    app = create_app(repositorio=repo)
    app.config["TESTING"] = True
    yield app.test_client()
    repo.cerrar()


def test_flujo_completo_de_una_tarea(cliente):
    # 1. Crear
    r = cliente.post("/tareas", json={"titulo": "Preparar exposición", "prioridad": "alta"})
    assert r.status_code == 201
    id_tarea = r.get_json()["id"]

    # 2. Listar
    assert len(cliente.get("/tareas").get_json()) == 1

    # 3. Progreso inicial
    assert cliente.get("/progreso").get_json()["progreso"] == 0.0

    # 4. Completar
    r = cliente.patch(f"/tareas/{id_tarea}/completar")
    assert r.status_code == 200
    assert r.get_json()["completada"] is True

    # 5. Progreso final
    assert cliente.get("/progreso").get_json()["progreso"] == 100.0

    # 6. Eliminar
    assert cliente.delete(f"/tareas/{id_tarea}").status_code == 204
    assert cliente.get("/tareas").get_json() == []


def test_crear_sin_body_devuelve_400(cliente):
    r = cliente.post("/tareas", data="esto no es json", content_type="text/plain")
    assert r.status_code == 400
    assert "obligatorio" in r.get_json()["error"]


def test_eliminar_inexistente_devuelve_404(cliente):
    assert cliente.delete("/tareas/999").status_code == 404
```

**Conceptos nuevos:**

- **`tmp_path`:** fixture integrada de pytest que entrega una carpeta temporal única por test. Cada test tiene su propia base de datos limpia: así se cumple la **I** y la **R** de FIRST.
- **Fixture con `yield`:** lo que va antes de `yield` es la preparación (*setup*); lo que va después, la limpieza (*teardown*).

### Unitario vs integración: misma ruta, dos tests distintos

| | `test_crear_tarea_invalida_no_toca_el_repositorio` (unit) | `test_flujo_completo_de_una_tarea` (integración) |
|---|---|---|
| Repositorio | Mock | SQLite real |
| Verifica | Que la ruta valida y **no llama** al repo | Que los datos **realmente** se guardan y leen |
| Si falla, el error está en... | La ruta o la validación | Cualquier parte de la cadena |
| Velocidad | Más rápido | Más lento |

### ¿Y la integración con servicios reales (PostgreSQL, Redis)?

En la Guía 6 se muestra cómo levantar un PostgreSQL de verdad dentro del CI con `services:`. En local se usa Docker Compose (Guía 4). Herramienta avanzada (opcional): `testcontainers-python`, que levanta contenedores desde los propios tests.

---

## 9. Ejecutar, filtrar y medir cobertura

```bash
pytest                            # todos los tests
pytest -v                         # detallado (un renglón por test)
pytest -m unit                    # solo unitarios
pytest -m integration             # solo integración
pytest tests/unit/test_logica.py  # un archivo
pytest -k progreso                # tests cuyo nombre contiene "progreso"
pytest -x                         # se detiene al primer fallo
pytest --lf                       # repite solo los que fallaron la última vez
```

Salida esperada:

```
$ pytest -m unit -q
....................                                   [100%]
20 passed, 9 deselected in 0.22s

$ pytest -m integration -q
.........                                              [100%]
9 passed, 20 deselected in 0.13s
```

### Cobertura

```bash
pytest --cov                                  # resumen en la terminal
pytest --cov --cov-report=html                # reporte web en htmlcov/index.html
pytest --cov --cov-report=xml                 # coverage.xml (lo usa SonarQube)
pytest --cov --cov-fail-under=80              # FALLA si la cobertura es menor al 80 %
```

```
Name                        Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------
src/tareas/__init__.py          0      0      0      0   100%
src/tareas/app.py              36      0      4      0   100%
src/tareas/logica.py           19      0      8      0   100%
src/tareas/repositorio.py      32      0      0      0   100%
-----------------------------------------------------------------------
TOTAL                          87      0     12      0   100%
```

La columna **Missing** indica las líneas que ningún test ejecutó: ahí debes escribir tests.

### Linter

```bash
ruff check src tests          # busca errores y malas prácticas
ruff format src tests         # da formato al código
```

Agrega a `.gitignore`: `.venv/`, `__pycache__/`, `.pytest_cache/`, `.coverage`, `coverage.xml`, `htmlcov/`, `*.db`.

---

## 10. Referencia rápida de pytest

| Elemento | Uso |
|---|---|
| `assert x == y` | Verificación básica (pytest muestra el detalle si falla) |
| `pytest.raises(Error, match="...")` | Verificar una excepción |
| `pytest.approx(0.1 + 0.2) == 0.3` | Comparar decimales |
| `@pytest.fixture` | Preparar datos/objetos reutilizables |
| `@pytest.fixture(scope="module")` | Fixture compartida por todo el archivo |
| `conftest.py` | Archivo donde se ponen fixtures compartidas entre archivos |
| `@pytest.mark.parametrize` | Mismo test con distintos datos |
| `@pytest.mark.skip(reason="...")` | Saltar un test |
| `@pytest.mark.xfail` | Se espera que falle (bug conocido) |
| `tmp_path` | Carpeta temporal |
| `monkeypatch.setenv("VAR", "x")` | Cambiar una variable de entorno durante el test |
| `monkeypatch.setattr(modulo, "funcion", falsa)` | Reemplazar una función |
| `capsys` | Capturar lo que se imprime |
| `unittest.mock.patch("modulo.objeto")` | Reemplazar un objeto durante el test |

---

## 11. Ejercicios

1. **Nueva regla (TDD):** el título no puede contener solo números. Escribe primero el test (🔴), luego el código (🟢). Haz un microcommit para cada paso.
2. **Nuevo endpoint:** `GET /tareas?prioridad=alta` filtra por prioridad. Escribe un test unitario con mock y uno de integración.
3. **Bug intencional:** cambia `round(..., 2)` por `round(..., 1)` en `calcular_progreso` y observa qué test falla y cómo lo reporta pytest.
4. **Cobertura:** comenta un test y mira cómo aparece la línea en *Missing*. Luego ejecuta `pytest --cov --cov-fail-under=95`.
5. **monkeypatch:** escribe un test que use `monkeypatch.setenv("DB_PATH", str(tmp_path / "x.db"))` y verifique que `create_app()` sin argumentos crea ese archivo.

---

## 12. Si tu proyecto final no es en Python

Los conceptos son iguales; cambian las herramientas:

| Lenguaje | Unitarios | Mocks | Integración HTTP | Cobertura |
|---|---|---|---|---|
| JavaScript / TypeScript | Jest, Vitest | `jest.fn()`, `vi.fn()` | Supertest | `--coverage` (genera `lcov.info`) |
| Java | JUnit 5 | Mockito | Spring Boot Test, REST Assured | JaCoCo |
| C# | xUnit, NUnit | Moq | WebApplicationFactory | Coverlet |
| Go | `testing` | interfaces + gomock | `httptest` | `go test -cover` |
| PHP | PHPUnit | Mockery | Laravel HTTP tests | Xdebug / PCOV |

SonarQube acepta los reportes de cobertura de todos ellos (Guía 6).
