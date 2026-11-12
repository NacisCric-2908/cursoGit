import pytest

from tareas.logica import calcular_progreso, validar_prioridad, validar_titulo

pytestmark = pytest.mark.unit


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
