from pylibdmtx.pylibdmtx import encode

# The below constants are only for 10x10 datamatrix
ENCODING_SIZE_NAMES = "10x10"
EDGE_SIZE = 10 + 4  # 10 for tiles, 4 for paddings
BYTES_PER_PIXEL = 3
BYTES_PER_SQUARE_EDGE = BYTES_PER_PIXEL * 5
BYTES_PER_DATAMATRIX_EDGE = BYTES_PER_SQUARE_EDGE * 70


def str_to_datamatrix(text: str) -> list[list[bool]]:
    if len(text) > 3:
        raise ValueError("Input text should be less than 3 chars")
    encoded = encode(text.encode("ascii"), size=ENCODING_SIZE_NAMES)
    tiles = [[False for _ in range(EDGE_SIZE)] for _ in range(EDGE_SIZE)]
    for r in range(EDGE_SIZE):
        for c in range(EDGE_SIZE):
            iloc = r * BYTES_PER_DATAMATRIX_EDGE + c * BYTES_PER_SQUARE_EDGE
            # print(encoded.pixels[iloc] == 255)
            tiles[r][c] = encoded.pixels[iloc] == 255
    return tiles
