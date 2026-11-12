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
