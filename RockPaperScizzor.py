import random
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

player_score = 0
computer_score = 0
draws = 0

choices = ["Rock", "Paper", "Scissors"]

result = "Choose your move!"


class GameHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global player_score, computer_score, draws, result

        parsed_url = urlparse(self.path)

        if parsed_url.path == "/":
            self.show_page()
            return

        if parsed_url.path == "/play":

            data = parse_qs(parsed_url.query)
            player_choice = data.get("choice", [""])[0]

            if player_choice in choices:

                computer_choice = random.choice(choices)

                if player_choice == computer_choice:
                    result = (
                        f"🤝 Draw! Both chose {computer_choice}."
                    )
                    draws += 1

                elif (
                    (player_choice == "Rock" and computer_choice == "Scissors")
                    or
                    (player_choice == "Paper" and computer_choice == "Rock")
                    or
                    (player_choice == "Scissors" and computer_choice == "Paper")
                ):
                    result = (
                        f"🎉 You Win!<br>"
                        f"You: {player_choice}<br>"
                        f"Computer: {computer_choice}"
                    )
                    player_score += 1

                else:
                    result = (
                        f"😢 Computer Wins!<br>"
                        f"You: {player_choice}<br>"
                        f"Computer: {computer_choice}"
                    )
                    computer_score += 1

            self.show_page()
            return

        if parsed_url.path == "/reset":

            player_score = 0
            computer_score = 0
            draws = 0

            result = "🔄 Game reset! Choose your move."

            self.show_page()
            return

        self.send_error(404)

    def show_page(self):

        html = f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Rock Paper Scissors</title>

            <style>

                body {{
                    margin: 0;
                    height: 100vh;

                    display: flex;
                    justify-content: center;
                    align-items: center;

                    font-family: Arial, sans-serif;

                    background:
                    linear-gradient(
                        135deg,
                        #667eea,
                        #764ba2
                    );
                }}

                .game {{
                    background: white;

                    width: 430px;

                    padding: 35px;

                    border-radius: 20px;

                    text-align: center;

                    box-shadow:
                    0 10px 30px
                    rgba(0,0,0,0.3);
                }}

                h1 {{
                    color: #333;
                    margin-bottom: 10px;
                }}

                .subtitle {{
                    color: #666;
                    font-size: 17px;
                }}

                .buttons {{
                    display: flex;
                    justify-content: center;
                    gap: 12px;

                    margin-top: 25px;
                }}

                .choice {{
                    text-decoration: none;

                    padding: 15px 18px;

                    border-radius: 10px;

                    color: white;

                    background: #667eea;

                    font-size: 16px;

                    font-weight: bold;
                }}

                .choice:hover {{
                    background: #4f63c4;
                }}

                .result {{
                    margin-top: 30px;

                    padding: 20px;

                    border-radius: 12px;

                    background: #f1f3ff;

                    font-size: 18px;

                    line-height: 1.8;

                    color: #333;
                }}

                .score {{
                    margin-top: 25px;

                    display: flex;
                    justify-content: space-around;

                    font-weight: bold;

                    font-size: 16px;
                }}

                .reset {{
                    display: inline-block;

                    margin-top: 25px;

                    padding: 10px 20px;

                    border-radius: 8px;

                    background: #333;

                    color: white;

                    text-decoration: none;
                }}

                .reset:hover {{
                    background: #555;
                }}

            </style>

        </head>

        <body>

            <div class="game">

                <h1>✊ Rock Paper Scissors ✋</h1>

                <div class="subtitle">
                    Choose your move!
                </div>

                <div class="buttons">

                    <a class="choice"
                       href="/play?choice=Rock">
                       🪨 Rock
                    </a>

                    <a class="choice"
                       href="/play?choice=Paper">
                       📄 Paper
                    </a>

                    <a class="choice"
                       href="/play?choice=Scissors">
                       ✂️ Scissors
                    </a>

                </div>

                <div class="result">
                    {result}
                </div>

                <div class="score">

                    <div>
                        🧑 You<br>
                        {player_score}
                    </div>

                    <div>
                        🤝 Draws<br>
                        {draws}
                    </div>

                    <div>
                        🤖 Computer<br>
                        {computer_score}
                    </div>

                </div>

                <a class="reset" href="/reset">
                    🔄 Reset Game
                </a>

            </div>

        </body>

        </html>
        """

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            html.encode()
        )

    def log_message(self, format, *args):
        pass


# Start server

server = HTTPServer(
    ("localhost", 8001),
    GameHandler
)

print("🎮 Rock Paper Scissors started!")

print(
    "🌐 Opening http://localhost:8001"
)

print(
    "Press CTRL+C to stop the game."
)

webbrowser.open(
    "http://localhost:8001"
)

server.serve_forever()
