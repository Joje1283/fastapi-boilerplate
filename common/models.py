from dataclasses import dataclass

from common.constants import Role


@dataclass
class CurrentUser:
    id: str
    role: Role

    def __str__(self):
        return f"{self.id}({self.role})"
