import dataclasses
from .datamatrix import str_to_datamatrix
from .types import (
    IdBoxSchema,
    SvgBubbleParam,
    SvgColumnParam,
    SvgHeaderParam,
    SvgParams,
)

VALUE_SEPARATOR = ";"
WIDTH_BUBBLE_BOX_DEFAULT = 30
HEIGHT_BUBBLE_BOX_DEFAULT = 30
HEIGHT_HEADER = 40
HEIGHT_WRITING = 40
BUBBLE_RATIO = 0.8
HEIGHT_TEXT_OFFSET = 1.5  # to ensure text is aligned vertically middle


def parse_schema_to_svg_params(schema: IdBoxSchema) -> SvgParams:
    header = SvgHeaderParam(**dataclasses.asdict(schema.header))
    columns = _parse_schema_fields(schema)

    num_rows = max(fieldDef.bubbles_per_column for fieldDef in schema.fields)
    num_columns = len(columns)

    data_matrix = []
    if schema.data_matrix_text is not None:
        data_matrix = str_to_datamatrix(schema.data_matrix_text)

    return SvgParams(
        width_max=WIDTH_BUBBLE_BOX_DEFAULT * num_columns,
        height_max=2 * header.height
        + HEIGHT_WRITING
        + num_rows * HEIGHT_BUBBLE_BOX_DEFAULT,
        width_box=WIDTH_BUBBLE_BOX_DEFAULT,
        height_box=HEIGHT_BUBBLE_BOX_DEFAULT,
        width_bubble=WIDTH_BUBBLE_BOX_DEFAULT * BUBBLE_RATIO,
        height_bubble=HEIGHT_BUBBLE_BOX_DEFAULT * BUBBLE_RATIO,
        height_writing=HEIGHT_WRITING,
        height_text_offset=HEIGHT_TEXT_OFFSET,
        columns=columns,
        header=header,
        footer_height=HEIGHT_HEADER,
        data_matrix=data_matrix,
        default_value_position_size_triplets=[],
    )


def _parse_schema_fields(schema: IdBoxSchema) -> list[SvgColumnParam]:
    columns: list[SvgColumnParam] = []
    column_count = 0
    for index, field_def in enumerate(schema.fields):
        col_values = _parse_schema_field_values(
            field_def.values,
            column_count,
        )
        column_count += len(col_values)
        for values in col_values:
            fill_offset = index if len(schema.fields) % 2 == 1 else index + 1
            default_fill = schema.fills[fill_offset % len(schema.fills)]
            columns.append(
                SvgColumnParam(
                    fieldIndex=index,
                    values=values,
                    fontSize=field_def.fontSize,
                    fontWeight=field_def.fontWeight,
                    isEmbed=field_def.isEmbed,
                    color=field_def.color,
                    fill=field_def.fill if field_def.fill is not None else default_fill,
                    hasDivider=False,
                    hideCircle=field_def.hideCircle,
                )
            )
        columns[-1].hasDivider = field_def.hasDivider
    columns[-1].hasDivider = False
    return columns


def _parse_schema_field_values(
    values: str,
    column_index: int,
    column_width: float = WIDTH_BUBBLE_BOX_DEFAULT,
    row_height: float = HEIGHT_BUBBLE_BOX_DEFAULT,
    bubble_ratio: float = BUBBLE_RATIO,
    dheight: float = HEIGHT_HEADER + HEIGHT_WRITING,
    bubbles_per_column: int = 13,
) -> list[list[SvgBubbleParam]]:
    valuesLst = values.split(VALUE_SEPARATOR)
    columns: list[list[SvgBubbleParam]] = []
    for s in range(0, len(valuesLst), bubbles_per_column):
        row_values = valuesLst[s : s + bubbles_per_column]
        bubbles: list[SvgBubbleParam] = []
        for i in range(len(row_values)):
            bubbles.append(
                SvgBubbleParam(
                    value=row_values[i],
                    isHidden=False,
                    isShaded=False,
                    isLabel=False,
                    center_x=(column_index + s // bubbles_per_column + 0.5)
                    * column_width,
                    center_y=(i + 0.5) * row_height + dheight,
                    radius_x=0.5 * column_width * bubble_ratio,
                    radius_y=0.5 * row_height * bubble_ratio,
                )
            )
        columns.append(bubbles)
    return columns
