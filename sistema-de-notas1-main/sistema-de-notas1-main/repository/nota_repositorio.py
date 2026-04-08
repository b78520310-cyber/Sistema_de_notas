class NotaRepositorio:
    def __init__(self):
        self._notas = []

    def agregar(self, nota):
        self._notas.append(nota)

    def obtener_todos(self):
        return list(self._notas)

    def obtener_por_uuid(self, nota_uuid):
        return next((n for n in self._notas if n.uuid == nota_uuid), None)

    def obtener_por_estudiante(self, estudiante_uuid):
        return [nota for nota in self._notas if nota.estudiante_uuid == estudiante_uuid]

    def actualizar(self, nota_uuid, estudiante_uuid, asignatura_uuid, valor):
        nota = self.obtener_por_uuid(nota_uuid)
        if nota is None:
            return False

        nota.estudiante_uuid = estudiante_uuid
        nota.asignatura_uuid = asignatura_uuid
        nota.valor = valor
        return True

    def eliminar(self, nota_uuid):
        nota = self.obtener_por_uuid(nota_uuid)
        if nota is None:
            return False

        self._notas.remove(nota)
        return True

    def eliminar_por_estudiante(self, estudiante_uuid):
        self._notas = [nota for nota in self._notas if nota.estudiante_uuid != estudiante_uuid]

    def eliminar_por_asignatura(self, asignatura_uuid):
        self._notas = [nota for nota in self._notas if nota.asignatura_uuid != asignatura_uuid]
