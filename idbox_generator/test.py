from idbox_generator.generate import (
    create_svg_from_params,
    generate_svg_params_by_schema,
    save_svg_to_file,
)
from idbox_generator.schema import (
    IdBoxSchema,
    IdBoxSchemaCustomFieldDefs,
    IdBoxSchemaHeader,
)


def test():
    schema = IdBoxSchema(
        header=IdBoxSchemaHeader(
            value="Student ID",
            fontWeight="bold",
            fontSize=20,
            fill="#ffffff",
            color="#000000",
        ),
        data_matrix_text="nus",
        fields=[
            IdBoxSchemaCustomFieldDefs(
                values="1;2;3;4;5;6;7;8",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r;s;t;u;v;w;x;y;z",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="x;y;z",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="1;2;3;4;5;6;7;8",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="1;2;3;4;5;6;7;8",
            ),
            IdBoxSchemaCustomFieldDefs(
                values="1;2;3;4;5;6;7;8",
            ),
        ],
    )
    svg_params = generate_svg_params_by_schema(schema)
    svg_content = create_svg_from_params(svg_params)
    save_svg_to_file(svg_content, "test.png", "png")
