import base64
import inspect

IMAGE_NAME = "noto-inkscape"
IMAGE_TAG = "1.3"
IMAGE_IDENTIFIER = f"{IMAGE_NAME}:{IMAGE_TAG}"


def execute_local(command):
    # use local inkscape installation
    import subprocess

    try:
        output = subprocess.run(
            command,
            capture_output=True,
            shell=True,
            text=True,
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
    assert output.returncode == 0, f"Error running inkscape locally: {output.stderr}"
    return output.stdout


def execute_docker(command):
    # Fallback to docker, since cannot guarantee every user to have inkscape installed
    # Docker CLI (comes with Docker Desktop) will need to be installed: https://docs.docker.com/engine/install/
    import docker  # pip install docker

    client = docker.from_env()
    container = client.containers.run(
        IMAGE_IDENTIFIER,
        command=f'sh -c "{command}"',
        remove=True,  # Remove container after execution
        stdout=True,
        stderr=True,
    )
    return container


def convert_svg(content_svg, extension, dpi=300, use_local=True):
    """Converts SVG content to the given extension type using inkscape."""
    base64_svg = base64.b64encode(content_svg.encode()).decode()
    command = f"echo '{base64_svg}' | base64 -d | inkscape --pipe --export-dpi={dpi} --export-type={extension} --export-filename=- 2>/dev/null | base64"
    try:
        assert use_local, "Skip using local inkscape"
        base64_output = execute_local(command)
        print("Generated using local inkscape")
    except Exception as e:
        print(e)
        base64_output = execute_docker(command)
        print("Generated using docker inkscape")
    content_output = base64.b64decode(base64_output)
    return content_output


def save_to_svg(filename, content_svg, dpi=None, use_local=None):
    with open(filename, "w") as f:
        f.write(content_svg)


def save_to_png(filename, content_svg, dpi=300, use_local=True):
    content = convert_svg(content_svg, "png", dpi=dpi, use_local=use_local)
    with open(filename, "wb") as f:
        f.write(content)


def save_to_pdf(filename, content_svg, dpi=None, use_local=True):
    content = convert_svg(content_svg, "pdf", use_local=use_local)
    with open(filename, "wb") as f:
        f.write(content)


def save_to_jpg(filename, content_svg, dpi=300, use_local=True):
    from io import BytesIO

    from PIL import Image

    content = convert_svg(content_svg, "png", dpi=dpi, use_local=use_local)
    png_buffer = BytesIO(content)
    with Image.open(png_buffer) as img:
        if img.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, img)
            img = bg
        img.save(filename, "JPEG")


# functions should have the following signature:
# def save_to_<extension_type>(filename, content_svg)

FUNCTION_PREFIX = "save_to_"

SUPPORTED_EXTENSIONS = {}
for name, obj in list(globals().items()):
    if inspect.isfunction(obj) and name.startswith(FUNCTION_PREFIX):
        SUPPORTED_EXTENSIONS[name[len(FUNCTION_PREFIX) :]] = obj

if __name__ == "__main__":
    import argparse
    import pathlib

    supported_extensions = set(SUPPORTED_EXTENSIONS.keys()) - {"svg"}
    parser = argparse.ArgumentParser(
        description=f'Generates file format ({"/".join(supported_extensions)}) from given id-box.json configuration.'
    )
    parser.add_argument(
        "filename", nargs="?", default="filename", help="path to svg file"
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="svg",
        choices=supported_extensions,
        help="Output type",
    )
    parser.add_argument("-o", "--output", type=str, default="", help="Output filename")

    args = parser.parse_args()
    filename_svg = pathlib.Path(args.filename)
    filename_output = (
        f"{filename_svg.stem}.{args.ext}" if not args.output else args.output
    )
    if pathlib.Path(filename_output).suffix[1:] in supported_extensions:
        args.ext = pathlib.Path(filename_output).suffix[1:]

    with open(filename_svg) as f:
        content_svg = f.read()

    converter = SUPPORTED_EXTENSIONS[args.ext]
    converter(filename_output, content_svg)
    print(f"Generated {filename_output}")
