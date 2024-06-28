from pylibdmtx.pylibdmtx import encode

# The below constants are only for 10x10 datamatrix
DATAMATRIX_SIZE = 10
ENCODING_SIZE_NAMES = f"{DATAMATRIX_SIZE}x{DATAMATRIX_SIZE}"
EDGE_SIZE = 14
PADDING_SIZE = 2
BYTES_PER_PIXEL = 3
BYTES_PER_SQUARE_EDGE = BYTES_PER_PIXEL * 5
BYTES_PER_DATAMATRIX_EDGE = BYTES_PER_SQUARE_EDGE * 70


def str_to_datamatrix(text: str) -> list[list[bool]]:
    if len(text) > 3:
        raise ValueError("Input text should be less than 3 chars")
    encoded = encode(text.encode("ascii"), size=ENCODING_SIZE_NAMES)
    tiles = [[False for _ in range(DATAMATRIX_SIZE)] for _ in range(DATAMATRIX_SIZE)]
    for r in range(PADDING_SIZE, EDGE_SIZE - PADDING_SIZE):
        for c in range(PADDING_SIZE, EDGE_SIZE - PADDING_SIZE):
            iloc = r * BYTES_PER_DATAMATRIX_EDGE + c * BYTES_PER_SQUARE_EDGE
            tiles[r - PADDING_SIZE][c - PADDING_SIZE] = encoded.pixels[iloc] == 255
    return tiles
