from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IdBoxSchemaHeader:
    value: str
    height: float = 40
    fontWeight: str = "bold"
    fontSize: int = 20
    fill: str = "#000000"
    color: str = "#ffffff"


@dataclass
class IdBoxSchemaCustomFieldDefs:
    values: str
    bubbles_per_column: int = 13
    defaultValue: str = ""
    fontSize: int = 15
    fontWeight: str = "normal"
    isEmbed: bool = True
    color: str = "#c2c3c3"
    fill: Optional[str] = None
    hasDivider: bool = True
    hideCircle: bool = False


@dataclass
class IdBoxSchema:
    """Schema for id box"""

    header: IdBoxSchemaHeader
    fields: list[IdBoxSchemaCustomFieldDefs] = field(default_factory=lambda: [])
    fills: list[str] = field(default_factory=lambda: ["#ffffff", "#d8e0f2"])
    data_matrix_text: str = ""
    aruco_stub_id: int = 0


@dataclass
class SvgHeaderParam:
    value: str
    height: float
    fontWeight: str
    fontSize: int
    fill: str
    color: str


@dataclass
class SvgBubbleParam:
    value: str
    center_x: float
    center_y: float
    radius_x: float
    radius_y: float
    isHidden: bool
    isShaded: bool
    isLabel: bool


@dataclass
class SvgColumnParam:
    fieldIndex: int
    values: list[SvgBubbleParam]
    fontSize: int
    fontWeight: str
    isEmbed: bool
    color: str
    fill: str
    hasDivider: bool
    hideCircle: bool


@dataclass
class SvgDatamatrixParam:
    tiles: list[list[bool]]
    left: float
    top: float
    width: float
    height: float
    margin: float


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
    footer_height: float
    data_matrices: list[SvgDatamatrixParam]

    default_value_position_size_triplets: list[tuple[str, float, int]]
