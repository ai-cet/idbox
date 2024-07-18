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


def id_to_aruco_tiles(id: int) -> list[list[bool]]:
    import cv2.aruco as aruco

    if id < 0 or id > 586:
        raise ValueError("aruco id should be between 0 and 586")
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h11)
    img = aruco.generateImageMarker(aruco_dict, id, 8)
    return [[bool(tile == 255) for tile in row] for row in img]
