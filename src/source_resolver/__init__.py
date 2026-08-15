"""source-resolver -- Rollenbasierte Quellenaufloesung fuer Skills.

Beantwortet fuer einen Skill die Frage "wo bekomme ich Information fuer Rolle X her?"
ueber eine feste Stufenleiter (0 User-Konfiguration .. 4 Nichts gefunden), statt dass
jeder Skill seine Quellen hart verdrahtet. Siehe README.md fuer die volle Spezifikation.
"""

from source_resolver.ladder import Stufe, ResolutionStatus, ResolutionResult, resolve, confirm
from source_resolver.pointer_check import check_pointer

__version__ = "0.1.0"

# Vertrags-Version der Ergebnisform (ResolutionResult-Felder, Stufe-Werte 0-4,
# ResolutionStatus-Vokabular). Aendert sich NUR, wenn diese Form selbst sich aendert --
# nicht bei jedem Feature. Wird von grounding-seed referenziert, dessen isolierte
# Minimalfassung dieselbe Form produzieren muss (siehe dortige ladder.py).
CONTRACT_VERSION = "1"

__all__ = [
    "Stufe",
    "ResolutionStatus",
    "ResolutionResult",
    "resolve",
    "confirm",
    "check_pointer",
    "__version__",
    "CONTRACT_VERSION",
]
