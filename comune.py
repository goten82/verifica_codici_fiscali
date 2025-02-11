from data import get_indexed_data
from typing import Any

_DATA: dict[str, dict[str, list[dict[str, Any]]]] = get_indexed_data()


def get_comune(codice: str) -> dict[str, Any] | None:
    comune = _DATA["municipalities"].get(
        codice,
        _DATA["countries"].get(
            codice,
            _DATA["codes"].get(
                codice,
            ),
        ),
    )
    if not comune:  
        return None  

    if isinstance(comune, dict):  
        return comune  

    return sorted(comune, key=lambda x: x.get('date_created', ''), reverse=True)[0]

    

