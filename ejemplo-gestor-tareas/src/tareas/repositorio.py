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
