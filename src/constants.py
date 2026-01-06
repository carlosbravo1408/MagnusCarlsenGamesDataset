from dataclasses import dataclass


@dataclass(frozen=True)
class __Consts:

    GAME_ID="game_id"
    DATETIME="datetime"

    WHITE_USERNAME="white_username"
    WHITE_RATING = "white_rating"
    WHITE_RESULT = "white_result"
    WHITE_ACCURACY = "white_accuracy"

    BLACK_USERNAME = "black_username"
    BLACK_RATING = "black_rating"
    BLACK_RESULT = "black_result"
    BLACK_ACCURACY = "black_accuracy"

    ECO = "eco"
    GAME_FORMAT = "game_format"
    GAME_RESULT = "game_result"
    SAN_MOVES = "san_moves"

    PGN = "pgn"

    ARCHIVES = "archives"
    GAMES = "games"
    END_TIME = "end_time"
    ACCURACIES = "accuracies"
    WHITE = "white"
    BLACK = "black"
    USERNAME = "username"
    RATING = "rating"
    RESULT = "result"
    PGN_RESULT = "Result"
    PGN_ECO = "ECO"
    TIME_CLASS = "time_class"
    URL = "url"

    CSV_COLUMNS = [
        "game_id", "datetime", "white_username", "white_rating", "white_result",
        "white_accuracy", "black_username", "black_rating", "black_result",
        "black_accuracy", "eco", "game_format", "game_result", "san_moves"
    ]

Constants = __Consts()
