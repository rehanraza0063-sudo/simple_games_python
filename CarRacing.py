import http.server
import webbrowser

# ==========================================
# SETTINGS
# ==========================================

PORT = 8004


# ==========================================
# WEB PAGE
# ==========================================

def create_page():

    return """
<!DOCTYPE html>

<html>

<head>

    <title>Car Racing Game</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;

            font-family: Arial, sans-serif;

            background: #111;

            color: white;

            text-align: center;

            overflow: hidden;
        }

        h1 {
            margin: 15px 0 5px;

            font-size: 36px;
        }

        .info {
            font-size: 20px;

            margin-bottom: 10px;
        }

        #game {
            width: 400px;
            height: 600px;

            margin: auto;

            position: relative;

            overflow: hidden;

            background: #333;

            border-left: 8px solid white;
            border-right: 8px solid white;
        }


        /* ==============================
           ROAD
        ============================== */

        .road-line {
            position: absolute;

            width: 8px;
            height: 80px;

            background: white;

            left: 50%;

            transform: translateX(-50%);
        }


        /* ==============================
           PLAYER CAR
        ============================== */

        #player {
            position: absolute;

            width: 60px;
            height: 100px;

            background: #2196f3;

            bottom: 30px;

            left: 170px;

            border-radius: 12px;

            box-shadow:
                0 0 10px rgba(255,255,255,0.4);
        }

        #player::before {
            content: "";

            position: absolute;

            width: 38px;
            height: 35px;

            background: #bde7ff;

            left: 11px;
            top: 12px;

            border-radius: 8px;
        }

        #player::after {
            content: "";

            position: absolute;

            width: 42px;
            height: 10px;

            background: #222;

            left: 9px;
            bottom: 15px;

            border-radius: 5px;
        }


        /* ==============================
           ENEMY CAR
        ============================== */

        .enemy {
            position: absolute;

            width: 60px;
            height: 100px;

            background: red;

            border-radius: 12px;

            box-shadow:
                0 0 10px rgba(255,255,255,0.3);
        }

        .enemy::before {
            content: "";

            position: absolute;

            width: 38px;
            height: 35px;

            background: #222;

            left: 11px;
            top: 12px;

            border-radius: 8px;
        }


        /* ==============================
           START BUTTON
        ============================== */

        #startButton {

            margin-top: 15px;

            padding: 12px 30px;

            font-size: 18px;

            border: none;

            border-radius: 8px;

            cursor: pointer;
        }

        #startButton:hover {
            transform: scale(1.05);
        }


        /* ==============================
           GAME OVER
        ============================== */

        #gameOver {

            position: absolute;

            top: 50%;

            left: 50%;

            transform: translate(-50%, -50%);

            background: rgba(0,0,0,0.9);

            padding: 30px;

            border-radius: 15px;

            display: none;

            width: 300px;
        }

        #gameOver h2 {
            font-size: 32px;

            margin-top: 0;
        }

        #restartButton {

            padding: 10px 25px;

            font-size: 17px;

            border: none;

            border-radius: 8px;

            cursor: pointer;
        }


        /* ==============================
           INSTRUCTIONS
        ============================== */

        .instructions {

            margin-top: 10px;

            font-size: 16px;
        }

    </style>

</head>


<body>


<h1>🏎️ Car Racing Game</h1>

<div class="info">

    Score:
    <span id="score">0</span>

</div>


<div id="game">

    <!-- Road Lines -->

    <div class="road-line" style="top: 0px;"></div>

    <div class="road-line" style="top: 150px;"></div>

    <div class="road-line" style="top: 300px;"></div>

    <div class="road-line" style="top: 450px;"></div>


    <!-- Player -->

    <div id="player"></div>


    <!-- Game Over -->

    <div id="gameOver">

        <h2>💥 Game Over!</h2>

        <p>
            Your Score:
            <span id="finalScore">0</span>
        </p>

        <button id="restartButton"
                onclick="restartGame()">

            🔄 Restart

        </button>

    </div>

</div>


<button id="startButton"
        onclick="startGame()">

    ▶️ Start Game

</button>


<div class="instructions">

    ⬅️ Left &nbsp;&nbsp;
    ➡️ Right

    <br>

    Use Arrow Keys to control the car

</div>


<script>


// ==========================================
// GAME VARIABLES
// ==========================================

const game = document.getElementById("game");

const player = document.getElementById("player");

const scoreDisplay =
    document.getElementById("score");

const gameOverScreen =
    document.getElementById("gameOver");

const finalScore =
    document.getElementById("finalScore");

const startButton =
    document.getElementById("startButton");


let playerX = 170;

let enemies = [];

let score = 0;

let gameRunning = false;

let gameSpeed = 5;

let keys = {};


// ==========================================
// KEYBOARD CONTROLS
// ==========================================

document.addEventListener("keydown", function(event) {

    keys[event.key] = true;

});


document.addEventListener("keyup", function(event) {

    keys[event.key] = false;

});


// ==========================================
// START GAME
// ==========================================

function startGame() {

    // Reset values

    playerX = 170;

    score = 0;

    gameSpeed = 5;

    gameRunning = true;

    enemies = [];


    // Remove old enemy cars

    document
        .querySelectorAll(".enemy")
        .forEach(car => car.remove());


    // Reset player

    player.style.left =
        playerX + "px";


    scoreDisplay.innerText =
        score;


    gameOverScreen.style.display =
        "none";


    startButton.style.display =
        "none";


    // Create first enemies

    createEnemy();

    createEnemy();


    // Start game loop

    requestAnimationFrame(gameLoop);

}


// ==========================================
// CREATE ENEMY
// ==========================================

function createEnemy() {

    const enemy =
        document.createElement("div");

    enemy.classList.add("enemy");


    // Random lane

    const lanes = [
        40,
        170,
        300
    ];


    const randomLane =
        lanes[
            Math.floor(
                Math.random() * lanes.length
            )
        ];


    enemy.style.left =
        randomLane + "px";


    enemy.style.top =
        "-120px";


    game.appendChild(enemy);


    enemies.push({

        element: enemy,

        x: randomLane,

        y: -120

    });

}


// ==========================================
// MOVE PLAYER
// ==========================================

function movePlayer() {

    if (keys["ArrowLeft"]) {

        playerX -= 7;

    }


    if (keys["ArrowRight"]) {

        playerX += 7;

    }


    // Keep car inside road

    if (playerX < 10) {

        playerX = 10;

    }


    if (playerX > 330) {

        playerX = 330;

    }


    player.style.left =
        playerX + "px";

}


// ==========================================
// MOVE ENEMIES
// ==========================================

function moveEnemies() {

    for (
        let i = enemies.length - 1;
        i >= 0;
        i--
    ) {

        let enemy = enemies[i];


        enemy.y += gameSpeed;


        enemy.element.style.top =
            enemy.y + "px";


        // Collision detection

        if (checkCollision(
            player,
            enemy.element
        )) {

            endGame();

            return;

        }


        // Enemy passed player

        if (enemy.y > 620) {

            enemy.element.remove();

            enemies.splice(i, 1);

            score++;

            scoreDisplay.innerText =
                score;


            // Increase speed

            if (score % 5 === 0) {

                gameSpeed += 0.5;

            }


            createEnemy();

        }

    }

}


// ==========================================
// COLLISION DETECTION
// ==========================================

function checkCollision(
    playerCar,
    enemyCar
) {

    const p =
        playerCar.getBoundingClientRect();

    const e =
        enemyCar.getBoundingClientRect();


    return !(
        p.bottom < e.top ||
        p.top > e.bottom ||
        p.right < e.left ||
        p.left > e.right
    );

}


// ==========================================
// GAME LOOP
// ==========================================

function gameLoop() {

    if (!gameRunning) {

        return;

    }


    movePlayer();

    moveEnemies();


    requestAnimationFrame(gameLoop);

}


// ==========================================
// GAME OVER
// ==========================================

function endGame() {

    gameRunning = false;


    finalScore.innerText =
        score;


    gameOverScreen.style.display =
        "block";


    startButton.style.display =
        "inline-block";


    startButton.innerText =
        "▶️ Play Again";

}


// ==========================================
// RESTART
// ==========================================

function restartGame() {

    startGame();

}


</script>


</body>

</html>
"""


# ==========================================
# WEB SERVER
# ==========================================

class CarRacingHandler(
    http.server.BaseHTTPRequestHandler
):

    def do_GET(self):

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


# ==========================================
# START SERVER
# ==========================================

print("----------------------------------------")

print("🏎️ CAR RACING GAME")

print("----------------------------------------")

print(f"🌐 Opening http://localhost:{PORT}")

print("----------------------------------------")


server = http.server.HTTPServer(
    ("localhost", PORT),
    CarRacingHandler
)


webbrowser.open(
    f"http://localhost:{PORT}"
)


server.serve_forever()
