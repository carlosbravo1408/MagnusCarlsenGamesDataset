from src.chesscom_api_helper import ChessComApiHelper
from src.lichess_api_helper import LichessAPIHelper

if __name__ == "__main__":
    chess_dot_com_api_helper = ChessComApiHelper()
    chess_dot_com_api_helper.get_chess_games(user_name="MagnusCarlsen")

    #lichess_api_helper = LichessAPIHelper()
    #lichess_api_helper.get_chess_games(user_name="DrNykterstein")
