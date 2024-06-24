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
class IdBoxSchemaCustomFieldDefs:
    id: str
    values: str
    bubbles_per_column: int = 13
    defaultValue: str = ""
    fontSize: int = 15
    fontWeight: str = "normal"
    isEmbed: bool = True
    color: str = "#c2c3c3"
    fill: str = "#ffffff"
    hasDivider: bool = True
    hideCircle: bool = False


@dataclass
class IdBoxSchema:
    """Schema for id box"""

    header: IdBoxSchemaHeader
    fields: dict[str, IdBoxSchemaCustomFieldDefs] = field(default_factory=lambda: {})
    fills: list[str] = field(default_factory=lambda: [])
    data_matrix_text: Optional[str] = None


@dataclass
class SvgHeaderParam:
    value: str
    fontWeight: str
    fontSize: int
    fill: str
    color: str


@dataclass
class SvgBubbleParam:
    value: str
    offset_x: float
    offset_y: float
    radius_x: float
    radius_y: float
    isHidden: bool
    isShaded: bool
    isLabel: bool


@dataclass
class SvgColumnParam:
    fieldId: str
    values: list[SvgBubbleParam]
    fontSize: int
    fontWeight: str
    isEmbed: bool
    color: str
    fill: str
    hasDivider: bool
    hideCircle: bool


@dataclass
class SvgParams:
    width_max: float
    height_max: float
    width_box: float
    height_box: float
    width_bubble: float
    height_bubble: float

    height_writing: float
    height_text_offset: float

    columns: list[SvgColumnParam]
    header: SvgHeaderParam
    data_matrix: list[list[bool]]

    default_value_position_size_triplets: list[tuple[str, float, int]]
