import csv
import io
import json
import os
from datetime import datetime
from typing import Literal, Optional, Dict, Any

import requests

from src.base_api_helper import APIHelper
from chess.pgn import read_game
from src.constants import Constants as C


Pseudonyms = [
    "MagnusCarlsen", "DrNykterstein", "DrDrunkenstein", "STL_Carlsen",
    "DannytheDonkey", "manwithavan", "damnsaltythatsport", "DrGrekenstein"
]
PseudonymLiteral = Literal[
    "MagnusCarlsen", "DrNykterstein", "DrDrunkenstein", "STL_Carlsen",
    "DannytheDonkey", "manwithavan", "damnsaltythatsport", "DrGrekenstein"
]


class LichessAPIHelper(APIHelper):
    base_url = "https://lichess.org/api/games/user/{user_name}"
    params = {
        "pgnInJson": True,
        #"evals": True,
        "opening": True
    }
    headers = {
        "Accept": "application/x-ndjson"
    }

    def get_chess_games(
            self,
            user_name: PseudonymLiteral = "DrNykterstein",
            output_path: str = "./dataset",
            save_pgn_games: bool = False
    ) -> Optional[str]:
        with requests.get(
                url=self.base_url.format(user_name=user_name),
                params=self.params,
                headers=self.headers,
                stream=True
        ) as response:
            try:
                response.raise_for_status()
                file_path = os.path.join(output_path, f"{user_name}_lichess.csv")
                os.makedirs(output_path, exist_ok=True)
                with open(file_path, "w", newline='',
                          encoding='utf-8') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=C.CSV_COLUMNS)
                    writer.writeheader()
                    for line in response.iter_lines():
                        if line:
                            game_json = json.loads(line)
                            row = self._extract_chess_games(game_json)
                            if save_pgn_games:
                                self._save_pgn_file(
                                    output_path,
                                    row[C.GAME_ID],
                                    row.pop(C.PGN)
                                )
                            else:
                                row.pop(C.PGN)
                            writer.writerow(row)
                        csv_file.flush()
            except Exception as e:
                print(f"Error: {e}")

    def _extract_chess_games(self, game_json: Dict[str, Any]) -> Dict[str, Any]:
        created_at = game_json.get("createdAt", 0) / 1000
        dt_object = datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S')
        white_p = game_json["players"]["white"]
        black_p = game_json["players"]["black"]
        game = read_game(io.StringIO(game_json.get("pgn")))
        return {
            C.GAME_ID: game_json["id"],
            C.DATETIME: dt_object,
            C.WHITE_USERNAME: white_p.get("user", {}).get("name", "Anon"),
            C.WHITE_RATING: white_p.get("rating"),
            C.WHITE_RESULT: "win" if game_json.get("winner") == "white" else "loss",
            C.WHITE_ACCURACY: None,
            C.BLACK_USERNAME: black_p.get("user", {}).get("name", "Anon"),
            C.BLACK_RATING: black_p.get("rating"),
            C.BLACK_RESULT: "win" if game_json.get("winner") == "black" else "loss",
            C.BLACK_ACCURACY: None,
            C.ECO: game_json.get("opening", {}).get("eco"),
            C.GAME_FORMAT: game_json.get("speed"), # bullet, blitz
            C.GAME_RESULT: game.headers.get(C.PGN_RESULT),
            C.PGN: game_json.get("pgn"),
            C.SAN_MOVES: APIHelper._get_san_moves(game),
        }
