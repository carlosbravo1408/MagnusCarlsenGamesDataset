import threading
from typing import Callable

from src.chesscom_api_helper import ChessComBaseAPIHelper
from src.lichess_api_helper import LichessBaseAPIHelper

from rich.progress import Progress, SpinnerColumn, TextColumn, TaskID


def get_chess_games(
        callback: Callable[[], None],
        progress_instance: Progress,
        task_id: TaskID
):
    try:
        callback()
        progress_instance.update(
            task_id, completed=1, total=1,
            description="[green]✅ Descarga: Completado"
        )
    except Exception as e:
        progress_instance.update(
            task_id,
            completed=1,
            total=1,
            description=f"[red]❌ Descarga: ({str(e)})"
        )


if __name__ == "__main__":
    chess_dot_com_api_helper = ChessComBaseAPIHelper()
    lichess_api_helper = LichessBaseAPIHelper()

    with Progress(
            SpinnerColumn(spinner_name="dots", finished_text=" "),
            TextColumn("[progress.description]{task.description}"),
            transient=False
    ) as progress:

        task1 = progress.add_task(
            "[cyan]Descargando datos @MagnusCarlsen de Chess.com...",
            total=None
        )
        t1 = threading.Thread(
            target=get_chess_games,
            kwargs={
                "callback": lambda: chess_dot_com_api_helper.get_chess_games(user_name="MagnusCarlsen"),
                "progress_instance": progress,
                "task_id": task1
            }
        )

        task2 = progress.add_task(
            "[magenta]Descargando datos @DrNykterstein de Lichess.org...",
            total=None
        )
        t2 = threading.Thread(
            target=get_chess_games,
            kwargs={
                "callback": lambda: lichess_api_helper.get_chess_games(user_name="DrNykterstein"),
                "progress_instance": progress,
                "task_id": task2
            }
        )

        t1.start()
        t2.start()
        t1.join()
        t2.join()
