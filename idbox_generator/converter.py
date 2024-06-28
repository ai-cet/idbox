def convert_svg_to_png(content_svg, dpi=300, scale=2) -> bytes:
    from cairosvg import svg2png

    return svg2png(
        bytestring=content_svg,
        dpi=dpi,
        scale=scale,
    )  # type: ignore
