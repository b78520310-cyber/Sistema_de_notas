class AsignaturaRepositorio:
    def __init__(self):
        self._asignaturas = []

    def agregar(self, asignatura):
        self._asignaturas.append(asignatura)

    def obtener_todos(self):
        return list(self._asignaturas)

    def obtener_por_uuid(self, asignatura_uuid):
        return next((a for a in self._asignaturas if a.uuid == asignatura_uuid), None)

    def actualizar(self, asignatura_uuid, nombre):
        asignatura = self.obtener_por_uuid(asignatura_uuid)
        if asignatura is None:
            return False

        asignatura.nombre = nombre
        return True

    def eliminar(self, asignatura_uuid):
        asignatura = self.obtener_por_uuid(asignatura_uuid)
        if asignatura is None:
            return False

        self._asignaturas.remove(asignatura)
        return True
