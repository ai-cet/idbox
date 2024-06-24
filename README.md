# Setup

## Pre-requisites

- [python ^3.11](https://www.python.org/)
- [poetry ^1.8.3](https://python-poetry.org/docs/)

## Development

```sh
# Dependencies
poetry config virtualenvs.in-project true
poetry install
poetry shell

# Pre-commit hooks
pre-commit install
```

Default output type is in SVG. If you require JPG/PNG/PDF outputs, CarioSVG needs to be installed.
Ensure that Cario is also on your system.

```sh
brew install cairo libffi # macOS/Homebrew
sudo apt-get install libcairo2-dev # Ubuntu/Debian
```

# Usage with template files

To generate SVG:

```sh
python generate.py templates/nric.json
```

You can also specify the output file type (defaults to .svg):

```sh
python generate.py templates/nric.json -e pdf
```

You can also specify the output filename:

```sh
python generate.py templates/nric.json -o samples/out.png
```

# Usage on command-line

Instead of a json configuration, you may also supply an alternative string argument that follows the following format:
`<header-title>|<column-id><column-separator><column-id>...`

The fills flag `-f` or `--fills` takes in a string argument that follows the following format:
`<hex-code>;<hex-code>...`

For example, to generate NUS, the following command can be used:

```sh
python generate.py "STUDENT NUMBER|prefix_nus|number;number;number;number;number;number;number|postfix_nus" -f "#ffffff;#ebf3ff" -o samples/nus.png
```

# Configuring custom types

Suppose you want to create a new ID box to identify the birthday in this format `01/Jan/1970`
Where the format begins with

1. a day of the month, represented by either 0 or 1 or 2 or 3, followed by a final digit, then
2. a `/`, then
3. a month of the year, represented by Jan, Feb, Mar, etc., then
4. a `/`, then
5. the year, starting with either 19 or 20, followed by two more digits.

There are a few ways that you can create this ID box.

### 1 Include it directly in a `birthdate.json` file

```json
{
  "header": {
    "value": "BIRTHDATE"
  },
  "columns": "prefix_day;number|slash|months|slash|prefix_year;number;number",
  "columnTypes": [
    {
      "id": "prefix_year",
      "values": ";19;20"
    },
    {
      "id": "months",
      "values": "Jan;Apr;Jul;Oct|Feb;May;Aug;Nov|Mar;Jun;Sep;Dec",
      "isEmbed": false,
      "fontSize": 12,
      "color": "#000000"
    },
    {
      "id": "prefix_day",
      "values": "0;1;2;3"
    },
    {
      "id": "slash",
      "values": "",
      "defaultValue": "/"
    }
  ]
}
```

Then, using it will simply be:

```sh
python generate.py templates/birthdate.json -o samples/birthdate.jpg
```

### 2 Include new types in `default.json`

You can add the custom types in `default.json` within the `"columnTypes"` array as shown below. If you don't specify an attribute, the default value will be used (the default values are in the object with ID `"default"`). The default values are also shown below.

```json
{
  ...,
  "columnTypes": [
    {
      "id": "default",
      "values": "",
      "defaultValue": "",
      "fontSize": 15,
      "fontWeight": "normal",
      "isEmbed": true,
      "color": "#c2c3c3",
      "fill": "#ffffff",
      "hasDivider": false
    },
    ...,
    {
      "id": "prefix_day",
      "values": "0;1;2;3"
    },
    {
      "id": "months",
      "values": "Jan;Apr;Jul;Oct|Feb;May;Aug;Nov|Mar;Jun;Sep;Dec",
      "isEmbed": false,
      "fontSize": 12,
      "color": "#000000"
    },
    {
      "id": "prefix_year",
      "values": ";19;20"
    },
    {
      "id": "slash",
      "values": "",
      "defaultValue": "/"
    }
  ]
}
```

Then, you can then reference the newly added column types directly in a `birthdate-new.json` file.

```json
{
  "header": {
    "value": "BIRTHDATE"
  },
  "columns": "prefix_day;number|slash|months|slash|prefix_year;number;number"
}
```

Then, using it will simply be:

```sh
python generate.py templates/birthdate-new.json -o samples/birthdate.pdf
```

# FAQ

1. Q: How do I create a "blank" bubble?
   A: You can create a blank space in your column type, `"values": ";b;c;;e"`, will skip over the first, and fourth positions. If you still want a blank bubble circle to appear, then use `"values": " ;b;c; ;e"` instead.
2. Q: How should I name my column IDs?
   A: You're recommended to follow Python's naming convention, and keep to alphanumberic and underscore \_. This will help you avoid clashing with special reserved characters used in parsing.

# Common Errors

1. `FileNotFoundError`
   Check two important files are referenced correctly, the `default.json` at the project root, and the target template json you want to use.
2. `FileNotFoundError` or `OSError: [Errno cairo returned CAIRO_STATUS_WRITE_ERROR: b'error while writing to output stream']`
   Check that your output filepath exists.
3. `error: argument -e/--extension: invalid choice`
   When using `-e` or `--extension`, check that the output file extension is supported.
4. `KeyError:`
   Check that your column type identifiers are all specified

# Advanced concepts: Default values and Anonymous column types

You can specify an anonymous column type using the following syntax
`<column-identifier>[<values>](default-value)`
in the command-line.

You may also include an optional prefix `+` to set the `isEmbed` to `false`
`+[<values>](default-value)`

If you wish to override an existing column type, you can also use
`<column-identifier>[<values>](default-value)`

### Example usage

Using the above birthdate example again, we can create the ID box again entirely within the command-line, with the additional contraint that the birth year is set to 1970 by default.

```sh
python generate.py "BIRTHDATE|[;19;20](19);number(7);number(0)|[](/)|+[Jan;Apr;Jul;Oct|Feb;May;Aug;Nov|Mar;Jun;Sep;Dec]|[](/)|[0;1;2;3];number" -o samples/birthdate.jpg
```

# TODO

- [x] Generation of ID boxes from given configuration
- [x] Support direct json input in command line
- [ ] Detection of bounding-box of ID box(es) on scanned pages
- [ ] Detection of shaded bubbles in cropped image of ID box
- [ ] Decoding of shaded values given configuration
