def piece_score(state, color):
    """
    Returns piece score advantage, KING not included in scoring

    Args:
        state (Board): board state under evaluation
        color (str): player color
    Returns:
        int: score between -1 and 1
    """
    white_count = len(state.color_coords["WHITE"])
    black_count = len(state.color_coords["BLACK"])

    # NOTE: Assumption white piece score is 2 and black piece 1.
    score = 2 * white_count - black_count 

    normalized_score = score / 16

    if color == "WHITE":
        return normalized_score
    else:
        return -normalized_score


# WHITE features
def king_safety(state, color):
    """
    Returns safety score: number of black pieces missing for king capture

    Args:
        state (Board): board state under evaluation

    Returns:
        int: score between -1 and 1
    """
    king_position = state.get_king_coords()

    if king_position[0] == 4 and king_position[1] == 4:  # king oh throne
        required_for_capture = 4

    elif king_position[0] == 4 or king_position[1] == 4:  # king next to throne
        required_for_capture = 3

    else:
        required_for_capture = 2

    close_blacks = 0
    if (
        state.coords_color.get((king_position[0] - 1, king_position[1]), None)
        == "BLACK"
    ):  # Up square check
        close_blacks += 1
    if (
        state.coords_color.get((king_position[0] + 1, king_position[1]), None)
        == "BLACK"
    ):  # Down square check
        close_blacks += 1
    if (
        state.coords_color.get((king_position[0], king_position[1] - 1), None)
        == "BLACK"
    ):  # Left square check
        close_blacks += 1
    if (
        state.coords_color.get((king_position[0], king_position[1] + 1), None)
        == "BLACK"
    ):  # Right square check
        close_blacks += 1

    normalized_score = (required_for_capture - close_blacks) / 2 - 1
    if color == "BLACK":
        return -normalized_score
    return normalized_score


def capture_king(state, color):
    if state.get_king_coords() is None:
        if color == "WHITE":
            return float("-inf")
        else:
            return float("inf")
    return 0


def win_move_king(state, color):
    king_position = state.get_king_coords()
    found = False
    if king_position[1] in (0, 8) or king_position[0] in (0, 8):
        if color == "WHITE":
            print('Win White')
            return float("inf")
        else:
            return float("-inf")

    if king_position[0] not in (2, 6) and king_position[1] not in (2, 6):
        return 0

    if king_position[0] in (2, 6):
        for col in range(9):
            if state.coords_color.get((king_position[0], col), None) is not None and (
                king_position[0],
                col,
            ) != (king_position[0], king_position[1]):
                found = True
                break
    elif king_position[1] in (2, 6):
        for row in range(9):
            if state.coords_color.get((row, king_position[1]), None) is not None and (
                row,
                king_position[1],
            ) != (king_position[0], king_position[1]):
                found = True
                break

    if not found:  # not found
        if color == "WHITE":
            return float("inf")
        else:
            return float("-inf")
    return 0
