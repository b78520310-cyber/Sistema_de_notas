from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Nota:
    estudiante_uuid: str
    asignatura_uuid: str
    valor: float
    uuid: str = field(default_factory=lambda: str(uuid4()))
