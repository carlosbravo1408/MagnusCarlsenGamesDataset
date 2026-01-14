import os.path
from typing import Literal, Optional, Dict, Any

from chess.pgn import StringExporter, Game
from src.constants import Constants as C


Pseudonyms = ["MagnusCarlsen", "DrNykterstein"]
PseudonymLiteral = Literal["MagnusCarlsen", "DrNykterstein"]


class BaseAPIHelper:

    base_url = "https://api.chess.com/pub/player/{user_name}/games/archives"

    headers = {
        "User-Agent": "Python Scrapper for EDA email@student.universidadviu.com"
    }

    def get_chess_games(
            self,
            user_name: PseudonymLiteral = "MagnusCarlsen",
            output_path: str = "./dataset",
            save_pgn_games: bool = False
    ) -> Optional[str]:
        raise NotImplementedError

    @classmethod
    def _save_pgn_file(
            cls,
            output_path: str,
            game_id: str,
            pgn_game: str
    ) -> None:
        os.makedirs(os.path.join(output_path, C.PGN), exist_ok=True)
        match_game = os.path.join(output_path, C.PGN, f"{game_id}.{C.PGN}")
        with open(match_game, "w") as pgn_file_game:
            pgn_file_game.write(pgn_game)

    @classmethod
    def _get_san_moves(cls, game: Game):
        return game \
            .mainline_moves() \
            .accept(StringExporter(columns=None, comments=False))

    def _extract_chess_games(self, game_json: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
