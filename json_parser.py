import re
import uuid

COLUMN_DIVIDER = "|"
COLUMN_SEPARATOR = ";"
regex_column = re.compile(rf"(?<!\[)([{COLUMN_DIVIDER}{COLUMN_SEPARATOR}])(?![^\[]*\])")

VALUE_DIVIDER = "|"
VALUE_SEPARATOR = ";"
regex_value = re.compile(rf"([{VALUE_SEPARATOR}{VALUE_DIVIDER}])")

regex_anonymous = re.compile(
    r"(?!$)(?P<non_embed>\+)?(?P<column_identifier>.*?)(?P<values>\[.*?\])?(?P<default_value>\(.*?\))?$"
)

WIDTH_DEFAULT = 30
HEIGHT_DEFAULT = 30
HEIGHT_HEADER = 40

DEFAULT_COLUMN_TYPE = {
    "values": "",
    "defaultValue": "",
    "fontSize": 18,
    "fontWeight": "normal",
    "isEmbed": False,
    "color": "#c2c3c3",
    "fill": "#ffffff",
    "hasDivider": False,
    "hideCircle": False,
}


def parse_json(data, template_data):
    data["header"] = data.get("header", {})
    data["fills"] = data.get("fills", [])
    data["columns"] = data.get("columns", "")
    data["columnTypes"] = {d["id"]: d for d in data.get("columnTypes", [])}

    # update with supplied template
    data["header"].update(template_data.get("header", {}))
    data["fills"] = template_data.get("fills", data["fills"])
    data["columns"] = template_data.get("columns", data["columns"])
    for d in template_data.get("columnTypes", []):
        data["columnTypes"][d["id"]] = data["columnTypes"].get(d["id"], {})
        data["columnTypes"][d["id"]].update(d)

    columns_split, default_value_position_size_triplets = parse_columns(data)
    data["columns"] = columns_split
    data["default_value_position_size_triplets"] = default_value_position_size_triplets

    return data


def parse_columns(data):
    column_string = data["columns"]
    column_fills = data["fills"]
    column_types = data["columnTypes"]

    # set overrides
    default_column_type = column_types.get("default", {})
    column_identifiers = regex_column.split(column_string)
    column_identifiers = [
        column_identifier
        for column_identifier in column_identifiers
        if column_identifier != COLUMN_SEPARATOR
    ]

    for i, column_identifier in enumerate(column_identifiers):
        if column_identifier == COLUMN_DIVIDER:
            continue
        groups = regex_anonymous.search(column_identifier)
        if not groups:
            continue

        column_identifier = groups.group("column_identifier")
        uid = get_uid(column_types.keys())
        column_identifiers[i] = uid
        column_types[uid] = column_types.get(
            column_identifier, column_types["default"]
        ).copy()

        values = groups.group("values")
        if values:
            column_types[uid]["values"] = values[1:-1]

        default_value = groups.group("default_value")
        if default_value:
            column_types[uid]["defaultValue"] = default_value[1:-1]

        non_embed = groups.group("non_embed")
        if non_embed:
            column_types[uid]["isEmbed"] = False
            column_types[uid]["color"] = "#000000"

    columns = []
    for i, column_identifier in enumerate(column_identifiers):
        if column_identifier == COLUMN_DIVIDER and i > 0:
            columns[-1]["hasDivider"] = True
        else:
            column = column_types[column_identifier].copy()
            columns.append(column)

    if len(column_fills) > 0:  # apply fill pattern if available
        for i, column in enumerate(columns):
            column["fill"] = column.get("fill", column_fills[i % len(column_fills)])

    columns_split = []
    for column in columns:
        # set defaults for values not yet set
        for key, value in default_column_type.items():
            column[key] = column.get(key, value)

        # convert values to list of lists
        column["values"] = parse_values(column["values"])
        for i, values in enumerate(column["values"]):
            if not column["isEmbed"]:
                labels = column.copy()
                labels["values"] = [
                    {
                        "value": value,
                        "isShaded": False,
                        "isHidden": True,
                        "isLabel": True,
                    }
                    for value in values
                ]
                labels["hideCircle"] = True
                labels["hasDivider"] = False
                bubbles = column.copy()
                bubbles["values"] = [
                    {
                        "value": "",
                        "isShaded": value == column["defaultValue"],
                        "isHidden": value == "",
                    }
                    for value in values
                ]
                bubbles["hasDivider"] = (
                    column["hasDivider"] if i == len(column["values"]) - 1 else False
                )
                columns_split.extend([labels, bubbles])
            else:
                bubbles = column.copy()
                bubbles["values"] = [
                    {
                        "value": value,
                        "isShaded": value == column["defaultValue"],
                        "isHidden": value == "",
                    }
                    for value in values
                ]
                bubbles["hasDivider"] = (
                    column["hasDivider"] if i == len(column["values"]) - 1 else False
                )
                columns_split.append(bubbles)

    default_value_position_size_triplets = []
    i = 0
    for column in columns:
        offset = len(column["values"])
        if not column["isEmbed"]:
            offset *= 2
        if column["defaultValue"] != "":
            value = column["defaultValue"]
            position = i + offset / 2
            fontSize = column["fontSize"]
            triplet = (value, position, fontSize)
            default_value_position_size_triplets.append(triplet)
        i += offset

    return columns_split, default_value_position_size_triplets


def parse_values(value_string):
    return [
        col.split(VALUE_SEPARATOR) if col else []
        for col in value_string.split(VALUE_DIVIDER)
    ]


def get_uid(reserved_keys=set()):
    uid = uuid.uuid4().hex
    while uid in reserved_keys:
        uid = uuid.uuid4().hex
    return uid
