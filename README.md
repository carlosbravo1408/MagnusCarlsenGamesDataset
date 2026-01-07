# Dataset de partidas de Magnus Carlsen en [chess.com](www.chess.com)

El siguiente repositorio contiene una colección de juegos de Magnus Carlsen en [Chess,com](www.chess.com), con datos estructurados a nivel de juegos con metadatos necesarios y movimientos normalizados bajo el formato SAN (Standard Algebraic Notation).

# Dataset Overview:

* **Origen**: API publica de [Chess.com](https://www.chess.com/news/view/published-data-api)
* **Alcance**: Todas las partidas disponibles en Chess.com hasta 05/01/2025
* **Formatos de juego**: Classical, Rapid, Blitz, Bullet
* **Notación de movimientos**: SAN normalizado.

# Chess.com API Overview

En este apartado se documenta brevemente el cómo consumir la API pública de Chess.com. Esta API es de acceso gratuito, de solo lectura y no requiere claves de autenticación, pero exige el cumplimiento de normas de etiqueta en las cabeceras.

Todas las peticiones se realizan a:

```http
https://api.chess.com/pub/
```

## Headers requeridos (User-Agent)

Es pertinente y obligatorio el identificar el script mediante el header `User-Agent`. De no hacerlo, se recibirá un error `403 Forbidden` o `429 Too Many Requests`

Formato sugerido (Usado en el script principal):

```python
headers = {
    'User-Agent': 'Python Scrapper for EDA email@institute.com'
}
```

## Endpoints usados:

### 1. Obtener los archivos por meses

* **Método**: `Get`
* **Endpoint**: `/player/{username}/games/archives`

#### Respuesta (JSON)

```json
{
    "archives": [
        "https://api.chess.com/pub/player/magnuscarlsen/games/2014/01",
        "https://api.chess.com/pub/player/magnuscarlsen/games/2014/02",
        "..."
    ]
}
```

### 2. Obtener las partidas de un mes:

* **Método**: `Get`
* **Endpoint**: `/player/{username}/games/{YYYY}/{MM}`

#### Respuesta (JSON)

```json
{
  "games": [
    {
      "url": "https://www.chess.com/game/live/123456789",
      "pgn": "[Event \"Live Chess\"]...",  // El PGN completo en texto plano
      "time_control": "180",
      "end_time": 1704067200,           
      "rated": true,
      "tcn": "mC0KmC0K...",              
      "uuid": "a1b2c3d4-...",
      "white": {
        "rating": 2882,
        "result": "win",
        "username": "MagnusCarlsen",
        "uuid": "..."
      },
      "black": {
        "rating": 2800,
        "result": "checkmated",
        "username": "Hikaru",
        "uuid": "..."
      },
      "time_class": "blitz",             // bullet, blitz, rapid, daily
      "rules": "chess",
      "accuracies": {                    // Solo disponible si hubo revisión de partida
        "white": 98.5,
        "black": 85.2
      }
    }
  ]
}
```

Si se desea un análisis exhaustivo partida por partida, se sugiere ejecutar el script `main.py` para que este descargue todos los juegos completos en formato `pgn` para su posterior tratamiento.

# Lichess API Overview

A diferencia de Chess.com, la API de Lichess está diseñada para el streaming de datos en lugar de la paginación por meses. Esto permite descargar historiales masivos en una sola conexión HTTP.

Todas las peticiones se realizan a:

```http
https://lichess.org/api/
```

## Headers requeridos

Es pertinente y obligatorio incluir la cabecera `Accept`.

```python
headers = {
    'Accept': 'application/x-ndjson'
}
```

## Endpoint usado:

Obtiene el historial completo (o parcial) de un usuario mediante streaming.

* **Método**: `GET`
* **Endpoint**: `/games/user/{username}`

### Parámetros Útiles (Query Params):

* `max`: Número máximo de partidas (ej. 50). Si se omite, descarga todas.
* `since` / `until`: Timestamps (en milisegundos) para filtrar por fecha.
* `pgnInJson`: true (Incluye el PGN dentro del objeto JSON).
* `clocks`: true (Incluye los tiempos de reloj por jugada).
* `evals`: true (Incluye evaluaciones de Stockfish si existen).
* `opening`: true (Incluye el código ECO y nombre de la apertura).

### Respuesta (NDJSON)

```json
{"id":"game1", "players":{...}, "moves":"e4 e5..."}
{"id":"game2", "players":{...}, "moves":"d4 d5..."}
{"id":"game3", "players":{...}, "moves":"Nf3 d5..."}
```

# Columnas:

* game_id: Identificador unico del juego, se puede usar también como parte de la url para visualizar la partida en Chess.com de la forma `https://www.chess.com/game/live/{game_id}`.
* datetime: fecha del encuentro en formato `YYYY-MM-DD HH:mm:SS`.
* white_username: Nombre de usuario jugando con blancas.
* white_result: win, resigned, insufficient, checkmated, timeout.
* white_rating: ELO rating para el jugador de blancas.
* white_accuracy: si la partida tuvo revisión, porcentaje de precisión en movimientos para blancas (Chess.com).
* black_username: Nombre de usuario jugando con negras.
* black_result: win, resigned, insufficient, checkmated, timeout.
* black_rating: ELO rating para el jugador de negras.
* black_accuracy: si la partida tuvo revisión, porcentaje de precisión en movimientos para negras (Chess.com).
* eco: Encyclopaedia of Chess Openings. tipo de apertura.
* game_format: Formato de juego: rapid, blitz, classical, bullet, etc.
* game_result: resultado en notación estándar: (1-0, 0-1, 1/2-1/2).
* san_moves: movimientos de la partida en formato SAN normalizado.

# Observaciones:

* Este dataset incluye juegos de Chess.com, incluye también de manera experimental juegos provenientes de lichess.com, no se incluyen partidas reales.
* Los movimientos fueron extraídos y convertidos con la librería `chess` para `python` de las partidas de formato `pgn` a un formato normalizado SAN.
* Los ratings ELO corresponden a los instantes en los que los participantes tenían en el instante del encuentro.