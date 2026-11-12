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
