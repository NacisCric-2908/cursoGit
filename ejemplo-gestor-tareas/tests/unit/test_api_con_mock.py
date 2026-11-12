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


def test_version_lee_el_commit_del_entorno(cliente, monkeypatch):
    monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)
    monkeypatch.setenv("APP_COMMIT", "abcdef1234567")

    assert cliente.get("/version").get_json() == {"commit": "abcdef1"}


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
