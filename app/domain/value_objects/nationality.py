from dataclasses import dataclass

import pycountry


@dataclass(frozen=True)
class Nationality:
    code: str

    def __post_init__(self) -> None:
        normalized = self.code.strip().upper()
        object.__setattr__(self, "code", normalized)
        if not pycountry.countries.get(alpha_2=normalized):
            raise ValueError(
                f"Invalid country code: '{
                    self.code}'. Must be a valid ISO 3166-1 alpha-2 code."
            )

    @property
    def name(self) -> str:
        country = pycountry.countries.get(alpha_2=self.code)
        assert country is not None
        return country.name
