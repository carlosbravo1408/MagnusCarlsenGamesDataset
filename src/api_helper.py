import csv
import io
import os.path
import time
from datetime import datetime
from typing import Literal

import requests

from chess.pgn import StringExporter, read_game, Game
from src.constants import Constants as C

Pseudonyms = ["MagnusCarlsen", "DrNykterstein"]
PseudonymLiteral = Literal["MagnusCarlsen", "DrNykterstein"]


class APIHelper:

    base_url = "https://api.chess.com/pub/player/{user_name}/games/archives"

    headers = {
        "User-Agent": "Python Scrapper for EDA email@student.universidadviu.com"
    }

    def get_chess_games(
            self,
            user_name: PseudonymLiteral = "MagnusCarlsen",
            output_path: str = "./dataset"
    ):
        try:
            response = requests.get(
                url=self.base_url.format(user_name=user_name),
                headers=self.headers
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return None
        archives = response.json().get(C.ARCHIVES, [])
        if not archives:
            return None
        file_path = os.path.join(output_path, f"{user_name}.csv")
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(os.path.join(output_path, C.PGN), exist_ok=True)
        with open(file_path, "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=C.CSV_COLUMNS)
            writer.writeheader()
            for month in archives:
                month_response = requests.get(url=month, headers=self.headers)
                month_response.raise_for_status()
                data_games = month_response.json().get(C.GAMES, [])
                for data_game in data_games:
                    game_data = self._extract_game_data(data_game)
                    self._save_pgn_file(
                        output_path, game_data[C.GAME_ID], game_data.pop(C.PGN))
                    if game_data:
                        writer.writerow(game_data)
                csv_file.flush()
                time.sleep(0.025)
        return file_path


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

    def _extract_game_data(self, game_json: dict):
        pgn_game = game_json.get(C.PGN)
        if not pgn_game:
            return None
        game = read_game(io.StringIO(pgn_game))
        dt_object = datetime\
            .fromtimestamp(game_json.get(C.END_TIME,0)) \
            .strftime('%Y-%m-%d %H:%M:%S')
        return {
            C.DATETIME: dt_object,
            C.WHITE_USERNAME: game_json[C.WHITE][C.USERNAME],
            C.WHITE_RATING: game_json[C.WHITE][C.RATING],
            C.WHITE_RESULT: game_json[C.WHITE][C.RESULT],
            C.WHITE_ACCURACY: game_json \
                .get(C.ACCURACIES, {}) \
                .get(C.WHITE, None),
            C.BLACK_USERNAME: game_json[C.BLACK][C.USERNAME],
            C.BLACK_RATING: game_json[C.BLACK][C.RATING],
            C.BLACK_RESULT: game_json[C.BLACK][C.RESULT],
            C.BLACK_ACCURACY: game_json \
                .get(C.ACCURACIES, {}) \
                .get(C.BLACK, None),
            C.ECO: game.headers.get(C.PGN_ECO),
            C.GAME_FORMAT: game_json[C.TIME_CLASS],
            C.GAME_RESULT: game.headers.get(C.PGN_RESULT),
            C.PGN: pgn_game,
            C.SAN_MOVES: self._get_san_moves(game),
            C.GAME_ID: game_json[C.URL].split("/")[-1],
        }
