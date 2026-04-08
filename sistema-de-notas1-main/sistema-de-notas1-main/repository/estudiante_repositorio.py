class EstudianteRepositorio:
    def __init__(self):
        self._estudiantes = []

    def agregar(self, estudiante):
        self._estudiantes.append(estudiante)

    def obtener_todos(self):
        return list(self._estudiantes)

    def obtener_por_uuid(self, estudiante_uuid):
        return next((e for e in self._estudiantes if e.uuid == estudiante_uuid), None)

    def actualizar(self, estudiante_uuid, nombre):
        estudiante = self.obtener_por_uuid(estudiante_uuid)
        if estudiante is None:
            return False

        estudiante.nombre = nombre
        return True

    def eliminar(self, estudiante_uuid):
        estudiante = self.obtener_por_uuid(estudiante_uuid)
        if estudiante is None:
            return False

        self._estudiantes.remove(estudiante)
        return True
