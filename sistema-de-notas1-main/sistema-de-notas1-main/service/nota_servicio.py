class NotaServicio:
    def __init__(self, nota_repositorio):
        self._nota_repositorio = nota_repositorio

    def calcular_promedio(self, estudiante_uuid):
        notas = self._nota_repositorio.obtener_por_estudiante(estudiante_uuid)
        if not notas:
            return 0.0

        total = sum(nota.valor for nota in notas)
        return total / len(notas)
