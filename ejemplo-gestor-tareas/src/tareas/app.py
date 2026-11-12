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

    @app.get("/version")
    def version():
        # Render define RENDER_GIT_COMMIT; la imagen de GHCR recibe APP_COMMIT al construirse
        commit = os.getenv("RENDER_GIT_COMMIT") or os.getenv("APP_COMMIT", "dev")
        return jsonify(commit=commit[:7])

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
