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
