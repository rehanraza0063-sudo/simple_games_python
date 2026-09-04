import http.server
import webbrowser
from urllib.parse import urlparse, parse_qs

# ==============================
# SETTINGS
# ==============================

PORT = 8002

# ==============================
# GAME VARIABLES
# ==============================

board = [""] * 9
current_player = "X"
winner = None


# ==============================
# CHECK WINNER
# ==============================

def check_winner():

    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_combinations:

        if board[a] != "":
            if board[a] == board[b] == board[c]:
                return board[a]

    # Check draw
    if all(board):
        return "Draw"

    return None


# ==============================
# CREATE WEB PAGE
# ==============================

def create_page():

    cells = ""

    for i in range(9):

        cells += f"""
        <button class="cell"
                onclick="window.location.href='/move?position={i}'">
            {board[i]}
        </button>
        """

    # Game status

    if winner == "X":
        status = "🎉 Player X Wins!"

    elif winner == "O":
        status = "🎉 Player O Wins!"

    elif winner == "Draw":
        status = "🤝 It's a Draw!"

    else:
        status = f"Player {current_player}'s Turn"

    # HTML + CSS

    page = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Tic-Tac-Toe</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(
                    135deg,
                    #141e30,
                    #243b55
                );

                color: white;
                text-align: center;
                margin: 0;
                padding-top: 50px;
            }}

            h1 {{
                font-size: 45px;
                margin-bottom: 10px;
            }}

            .subtitle {{
                font-size: 18px;
                margin-bottom: 25px;
            }}

            .status {{
                font-size: 25px;
                font-weight: bold;
                margin-bottom: 25px;
            }}

            .board {{
                width: 330px;
                height: 330px;

                margin: auto;

                display: grid;

                grid-template-columns:
                    repeat(3, 1fr);

                gap: 8px;
            }}

            .cell {{
                font-size: 55px;
                font-weight: bold;

                border: none;
                border-radius: 12px;

                background: white;
                color: #222;

                cursor: pointer;
            }}

            .cell:hover {{
                background: #eeeeee;
                transform: scale(1.03);
            }}

            .restart {{
                display: inline-block;

                margin-top: 25px;

                padding: 12px 25px;

                background: white;
                color: #222;

                text-decoration: none;

                border-radius: 8px;

                font-size: 17px;
                font-weight: bold;
            }}

            .restart:hover {{
                background: #dddddd;
            }}

        </style>

    </head>

    <body>

        <h1>⭕ Tic-Tac-Toe ❌</h1>

        <div class="subtitle">
            Python • Browser Game • Single File
        </div>

        <div class="status">
            {status}
        </div>

        <div class="board">

            {cells}

        </div>

        <a class="restart" href="/reset">
            🔄 Restart Game
        </a>

    </body>

    </html>
    """

    return page


# ==============================
# WEB SERVER
# ==============================

class GameHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        global board
        global current_player
        global winner

        url = urlparse(self.path)

        path = url.path

        # ------------------------------
        # PLAYER MAKES A MOVE
        # ------------------------------

        if path == "/move" and winner is None:

            query = parse_qs(url.query)

            if "position" in query:

                position = int(query["position"])

                # Make sure position is valid
                if 0 <= position <= 8:

                    # Make sure square is empty
                    if board[position] == "":

                        board[position] = current_player

                        # Check winner
                        result = check_winner()

                        if result:

                            winner = result

                        else:

                            # Change player
                            if current_player == "X":
                                current_player = "O"

                            else:
                                current_player = "X"

        # ------------------------------
        # RESET GAME
        # ------------------------------

        elif path == "/reset":

            board = [""] * 9

            current_player = "X"

            winner = None

        # ------------------------------
        # SEND WEB PAGE
        # ------------------------------

        page = create_page()

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            page.encode()
        )


# ==============================
# START SERVER
# ==============================

print("--------------------------------")
print("🎮 TIC-TAC-TOE GAME")
print("--------------------------------")

print(f"🌐 Opening:")
print(f"http://localhost:{PORT}")

print("--------------------------------")

server = http.server.HTTPServer(
    ("localhost", PORT),
    GameHandler
)

# Open browser automatically

webbrowser.open(
    f"http://localhost:{PORT}"
)

# Keep server running

server.serve_forever()
