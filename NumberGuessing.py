import random
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

secret_number = random.randint(1, 100)
attempts = 0
message = "I'm thinking of a number between 1 and 100."


class GameHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global secret_number, attempts, message

        if self.path == "/":
            self.show_page()
            return

        if self.path.startswith("/guess"):
            query = self.path.split("?", 1)

            if len(query) > 1:
                data = parse_qs(query[1])

                try:
                    guess = int(data.get("number", [""])[0])
                    attempts += 1

                    if guess < 1 or guess > 100:
                        message = "⚠️ Enter a number between 1 and 100."

                    elif guess < secret_number:
                        message = "📈 Too low! Try a bigger number."

                    elif guess > secret_number:
                        message = "📉 Too high! Try a smaller number."

                    else:
                        message = (
                            f"🎉 Correct! The number was {secret_number}. "
                            f"You guessed it in {attempts} attempts!"
                        )

                except ValueError:
                    message = "⚠️ Please enter a valid number."

            self.show_page()

    def show_page(self):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Number Guessing Game</title>

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}

                .game {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    width: 400px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}

                h1 {{
                    color: #333;
                }}

                p {{
                    color: #555;
                    font-size: 18px;
                }}

                input {{
                    padding: 12px;
                    width: 180px;
                    font-size: 18px;
                    border: 2px solid #667eea;
                    border-radius: 8px;
                    text-align: center;
                }}

                button {{
                    margin-top: 15px;
                    padding: 12px 25px;
                    font-size: 17px;
                    border: none;
                    border-radius: 8px;
                    background: #667eea;
                    color: white;
                    cursor: pointer;
                }}

                button:hover {{
                    background: #4c63c7;
                }}

                .message {{
                    margin-top: 25px;
                    font-weight: bold;
                    color: #333;
                }}

                .attempts {{
                    margin-top: 15px;
                    color: #777;
                }}
            </style>
        </head>

        <body>

            <div class="game">

                <h1>🎯 Number Guessing Game</h1>

                <p>
                    Guess a number between <b>1 and 100</b>
                </p>

                <form action="/guess" method="get">

                    <input
                        type="number"
                        name="number"
                        min="1"
                        max="100"
                        placeholder="Enter number"
                        required
                    >

                    <br>

                    <button type="submit">
                        Guess
                    </button>

                </form>

                <div class="message">
                    {message}
                </div>

                <div class="attempts">
                    Attempts: {attempts}
                </div>

            </div>

        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass


# Start the local web server
server = HTTPServer(("localhost", 8000), GameHandler)

print("🎮 Number Guessing Game Started!")
print("🌐 Opening http://localhost:8000")
print("Press CTRL+C to stop the game.")

webbrowser.open("http://localhost:8000")

server.serve_forever()
