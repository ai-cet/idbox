import argparse
import dataclasses
import json
import os
import re
from pathlib import Path
from typing import Optional

from jinja2 import Template

from idbox_generator.schema import IdBoxSchema, SvgParams

from .data_matrix import str_to_datamatrix
from .json_parser import parse_json, parse_schema
from .save_to import SUPPORTED_EXTENSIONS

# pip install Jinja2


_CURRENT_DIR = Path(__file__).parent.absolute()
_ASSET_DIR = _CURRENT_DIR / "assets"
_DATA_DIR = _CURRENT_DIR / "data"

FILENAME_DEFAULT_JSON = _DATA_DIR / "default.json"
WIDTH_DEFAULT = 30
HEIGHT_DEFAULT = 30
HEIGHT_TITLE = 40
HEIGHT_WRITING = 40
BUBBLE_RATIO = 0.8
HEIGHT_TEXT_OFFSET = 1.5  # to ensure text is aligned vertically middle


def generate_svg_params_by_schema(schema: IdBoxSchema):
    return parse_schema(schema)


def generate_svg_params(template_data, data_matrix_text: Optional[str] = None):
    with open(FILENAME_DEFAULT_JSON) as f:
        data = json.load(f)

    data = parse_json(data, template_data)
    columns = data["columns"]

    data["num_columns"] = len(columns)
    max_rows = max(len(column["values"]) for column in columns)
    # if the first column is too long, add a row for the bot-left marker
    data["num_rows"] = max_rows
    if len(columns[0]["values"]) == max_rows:
        data["num_rows"] += 1

    data["height_max"] = (
        HEIGHT_TITLE + HEIGHT_WRITING + data["num_rows"] * HEIGHT_DEFAULT
    )
    data["width_max"] = WIDTH_DEFAULT * data["num_columns"]
    data["width_box"] = WIDTH_DEFAULT
    data["height_box"] = HEIGHT_DEFAULT
    data["height_title"] = HEIGHT_TITLE
    data["height_writing"] = HEIGHT_WRITING
    data["width_bubble"] = WIDTH_DEFAULT * BUBBLE_RATIO
    data["height_bubble"] = HEIGHT_DEFAULT * BUBBLE_RATIO
    data["height_text_offset"] = HEIGHT_TEXT_OFFSET

    data["data_matrix"] = []
    if data_matrix_text is not None:
        data["data_matrix"] = str_to_datamatrix(data_matrix_text)
        data["data_matrix_offset_x"] = (HEIGHT_TITLE - HEIGHT_DEFAULT) / 2
        data["data_matrix_offset_y"] = (HEIGHT_TITLE - HEIGHT_DEFAULT) / 2
    return data


def create_svg_from_params(params: SvgParams):
    svg_template_filepath = _ASSET_DIR / "template.svg"
    with open(svg_template_filepath) as f:
        svg_template = Template(f.read())

    return svg_template.render(**dataclasses.asdict(params))


def create_svg(params):
    svg_template_filepath = _ASSET_DIR / "template.svg"
    with open(svg_template_filepath) as f:
        svg_template = Template(f.read())

    return svg_template.render(**params)


def save_svg_to_file(content_svg, filename_output, extension=None, use_local=True):
    extension = extension or Path(filename_output).suffix[1:]
    converter = SUPPORTED_EXTENSIONS[extension]
    converter(filename_output, content_svg, use_local=use_local)


def convert_svg_to_png(content_svg, dpi=300, scale=2) -> bytes:
    from cairosvg import svg2png

    return svg2png(
        bytestring=content_svg,
        dpi=dpi,
        scale=scale,
    )  # type: ignore


def slugify(text, separator="_"):
    text = text.lower()
    text = re.sub(r"\s+", separator, text)  # Replace spaces with separator
    text = re.sub(
        r"[^\w\s-]", "", text
    )  # Remove all non-word characters except hyphens
    text = re.sub(f"{separator}+", separator, text).strip(separator)
    return text


def is_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description=f'Generates file format ({"/".join(SUPPORTED_EXTENSIONS.keys())}) from given id-box.json configuration.'
    )
    parser.add_argument(
        "configuration",
        help='path/to/config.json or "{json: string}" or "command-line-pattern"',
    )
    parser.add_argument(
        "-f",
        "--fills",
        type=str,
        default="",
        help="Fill values to be used in command-line usage",
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default="svg",
        choices=SUPPORTED_EXTENSIONS.keys(),
        help="Output extension type",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="",
        help="Output filename, extension here will override --extension flag if specified",
    )
    parser.add_argument(
        "-d",
        "--docker",
        action="store_true",
        help="Flag to use docker image for conversion",
    )

    args = parser.parse_args()
    args.fills = (
        [hexcode or "none" for hexcode in args.fills.rstrip(";").split(";")]
        if args.fills
        else []
    )
    configuration = args.configuration
    if os.path.exists(configuration):
        filename_json = Path(configuration)
        with open(filename_json) as f:
            template_data = json.load(f)
        filestem_output = filename_json.stem
    elif is_json(configuration):
        template_data = json.loads(configuration)
        filestem_output = slugify(
            template_data.get("header", {}).get("value", "output")
        )
    else:
        header_value, columns = args.configuration.split("|", maxsplit=1)
        template_data = {
            "header": {
                "value": header_value,
            },
            "columns": columns,
        }
        filestem_output = slugify(header_value)
    if args.fills:
        template_data["fills"] = args.fills

    filename_output = args.output or f"{filestem_output}.{args.extension}"
    if Path(filename_output).suffix[1:] in SUPPORTED_EXTENSIONS:
        args.extension = Path(filename_output).suffix[1:]

    svg_params = generate_svg_params(template_data)
    content_svg = create_svg(svg_params)
    save_svg_to_file(
        content_svg,
        filename_output,
        extension=args.extension,
        use_local=not args.docker,
    )
    print(f"Generated {filename_output}")


if __name__ == "__main__":
    main()
