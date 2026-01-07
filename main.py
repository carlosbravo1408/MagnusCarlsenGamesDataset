from src.api_helper import APIHelper


if __name__ == "__main__":
    api = APIHelper()
    api.get_chess_games(user_name="MagnusCarlsen")
