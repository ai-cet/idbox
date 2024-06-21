from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IdBoxSchemaHeader:
    value: str
    fontWeight: str = "bold"
    fontSize: int = 20
    fill: str = "#ffffff"
    color: str = "#000000"


@dataclass
class IdBoxSchemaCustomColumnDefs:
    id: str
    values: str
    defaultValue: str = ""
    fontSize: int = 15
    fontWeight: str = "normal"
    isEmbed: bool = True
    color: str = "#c2c3c3"
    fill: str = "#ffffff"
    hasDivider: bool = False
    hideCircle: bool = False


@dataclass
class IdBoxSchema:
    """Schema for id box"""

    header: IdBoxSchemaHeader
    columns: str
    columnTypes: list[IdBoxSchemaCustomColumnDefs] = field(default_factory=lambda: [])
    fills: list[str] = field(default_factory=lambda: [])
    data_matrix_text: Optional[str] = None
