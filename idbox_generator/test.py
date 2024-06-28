from idbox_generator.generate import (
    create_svg_from_params,
    save_svg_to_file,
)
from .schema_handler import parse_schema_to_svg_params
from .types import (
    IdBoxSchema,
    IdBoxSchemaCustomFieldDefs,
    IdBoxSchemaHeader,
)


def test():
    schema = IdBoxSchema(
        header=IdBoxSchemaHeader(
            value="STUDENT ID",
            fontWeight="bold",
            fontSize=20,
            fill="#000000",
            color="#ffffff",
        ),
        data_matrix_text="nus",
        fields=[
            IdBoxSchemaCustomFieldDefs(
                values="0;1;2;3;4;5;6;7;8;9",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z"
            ),
            IdBoxSchemaCustomFieldDefs(
                values="X;Y;Z",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="0;1;2;3;4;5;6;7;8;9",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="0;1;2;3;4;5;6;7;8;9",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="0;1;2;3;4;5;6;7;8;9",
            ),
        ],
    )
    svg_params = parse_schema_to_svg_params(schema)
    svg_content = create_svg_from_params(svg_params)
    save_svg_to_file(svg_content, "test.png", "png")
