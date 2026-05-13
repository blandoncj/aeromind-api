from enum import StrEnum


class Role(StrEnum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    PASSENGER = "PASSENGER"

    @property
    def label(self) -> str:
        return {
            Role.ADMIN: "Administrador",
            Role.OPERATOR: "Operador",
            Role.PASSENGER: "Pasajero"
        }[self]
