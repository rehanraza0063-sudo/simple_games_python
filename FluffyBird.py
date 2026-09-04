import http.server
import webbrowser

# ==========================================
# SETTINGS
# ==========================================

PORT = 8005


# ==========================================
# CREATE WEB PAGE
# ==========================================

def create_page():

    return """
<!DOCTYPE html>

<html>

<head>

    <title>Flappy Bird Style Game</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;

            font-family: Arial, sans-serif;

            background: #222;

            color: white;

            text-align: center;
        }

        h1 {
            margin: 20px 0 5px;

            font-size: 40px;
        }

        .score {
            font-size: 25px;

            margin: 10px;
        }

        #game {

            width: 400px;
            height: 600px;

            margin: auto;

            position: relative;

            overflow: hidden;

            background: linear-gradient(
                #70c5ce,
                #dff6f8
            );

            border: 5px solid white;
        }


        /* =================================
           BIRD
        ================================= */

        #bird {

            position: absolute;

            width: 40px;
            height: 30px;

            background: yellow;

            border-radius: 50%;

            left: 80px;
            top: 250px;

            z-index: 10;
        }

        #bird::before {

            content: "";

            position: absolute;

            width: 10px;
            height: 10px;

            background: black;

            border-radius: 50%;

            right: 7px;
            top: 6px;
        }

        #bird::after {

            content: "";

            position: absolute;

            width: 14px;
            height: 8px;

            background: orange;

            right: -10px;
            top: 13px;

            border-radius: 3px;
        }


        /* =================================
           PIPES
        ================================= */

        .pipe {

            position: absolute;

            width: 60px;

            background: #28a745;

            border: 3px solid #146c2e;
        }

        .top-pipe {

            top: 0;
        }

        .bottom-pipe {

            bottom: 0;
        }


        /* =================================
           GROUND
        ================================= */

        #ground {

            position: absolute;

            bottom: 0;
            left: 0;

            width: 100%;
            height: 25px;

            background: #d2b45f;

            border-top: 4px solid #8b7a3c;

            z-index: 20;
        }


        /* =================================
           START SCREEN
        ================================= */

        #startScreen {

            position: absolute;

            width: 100%;
            height: 100%;

            top: 0;
            left: 0;

            background: rgba(0, 0, 0, 0.35);

            z-index: 30;

            display: flex;

            flex-direction: column;

            justify-content: center;

            align-items: center;
        }

        #startScreen h2 {

            font-size: 32px;

            margin: 10px;
        }

        #startButton {

            padding: 12px 25px;

            font-size: 18px;

            border: none;

            border-radius: 8px;

            cursor: pointer;
        }


        /* =================================
           GAME OVER
        ================================= */

        #gameOver {

            position: absolute;

            width: 100%;

            top: 40%;

            text-align: center;

            z-index: 40;

            display: none;
        }

        #gameOverBox {

            display: inline-block;

            background: rgba(0, 0, 0, 0.85);

            padding: 25px;

            border-radius: 15px;
        }

        #gameOver h2 {

            font-size: 32px;

            margin: 5px;
        }

        #restartButton {

            padding: 10px 22px;

            font-size: 17px;

            border: none;

            border-radius: 8px;

            cursor: pointer;
        }


        /* =================================
           INSTRUCTIONS
        ================================= */

        .instructions {

            margin-top: 15px;

            font-size: 17px;
        }

    </style>

</head>


<body>


<h1>🐦 Flappy Bird Style</h1>


<div class="score">

    Score:
    <span id="score">0</span>

</div>


<div id="game">


    <!-- BIRD -->

    <div id="bird"></div>


    <!-- START SCREEN -->

    <div id="startScreen">

        <h2>🐦 Ready?</h2>

        <button id="startButton"
                onclick="startGame()">

            ▶️ Start Game

        </button>

    </div>


    <!-- GAME OVER -->

    <div id="gameOver">

        <div id="gameOverBox">

            <h2>💥 Game Over!</h2>

            <p>
                Score:
                <span id="finalScore">0</span>
            </p>

            <button id="restartButton"
                    onclick="restartGame()">

                🔄 Restart

            </button>

        </div>

    </div>


    <!-- GROUND -->

    <div id="ground"></div>


</div>


<div class="instructions">

    🖱️ Click or press SPACE to fly

    <br>

    Avoid the pipes!

</div>


<script>


// ==========================================
// GAME ELEMENTS
// ==========================================

const game =
    document.getElementById("game");

const bird =
    document.getElementById("bird");

const scoreDisplay =
    document.getElementById("score");

const startScreen =
    document.getElementById("startScreen");

const gameOverScreen =
    document.getElementById("gameOver");

const finalScore =
    document.getElementById("finalScore");


// ==========================================
// GAME VARIABLES
// ==========================================

let birdX = 80;

let birdY = 250;

let velocity = 0;

let gravity = 0.45;

let jumpStrength = -8;

let score = 0;

let gameRunning = false;

let pipes = [];

let pipeSpeed = 3;

let pipeTimer = 0;


// ==========================================
// START GAME
// ==========================================

function startGame() {

    birdY = 250;

    velocity = 0;

    score = 0;

    pipeSpeed = 3;

    pipeTimer = 0;

    pipes = [];

    gameRunning = true;


    scoreDisplay.innerText = score;


    startScreen.style.display =
        "none";

    gameOverScreen.style.display =
        "none";


    // Remove old pipes

    document
        .querySelectorAll(".pipe")
        .forEach(pipe => pipe.remove());


    gameLoop();

}


// ==========================================
// BIRD JUMP
// ==========================================

function jump() {

    if (!gameRunning) {

        return;

    }

    velocity = jumpStrength;

}


// ==========================================
// KEYBOARD CONTROL
// ==========================================

document.addEventListener(
    "keydown",
    function(event) {

        if (event.code === "Space") {

            event.preventDefault();

            jump();

        }

    }
);


// ==========================================
// MOUSE CONTROL
// ==========================================

game.addEventListener(
    "click",
    function(event) {

        // Don't jump when clicking buttons

        if (
            event.target.tagName !== "BUTTON"
        ) {

            jump();

        }

    }
);


// ==========================================
// CREATE PIPE
// ==========================================

function createPipe() {

    const gap = 160;

    const minTop = 80;

    const maxTop = 330;

    const topHeight =
        Math.floor(
            Math.random() *
            (maxTop - minTop)
        ) + minTop;


    const bottomHeight =
        600 -
        topHeight -
        gap;


    // Top pipe

    const topPipe =
        document.createElement("div");

    topPipe.className =
        "pipe top-pipe";

    topPipe.style.height =
        topHeight + "px";

    topPipe.style.left =
        "400px";


    // Bottom pipe

    const bottomPipe =
        document.createElement("div");

    bottomPipe.className =
        "pipe bottom-pipe";

    bottomPipe.style.height =
        bottomHeight + "px";

    bottomPipe.style.left =
        "400px";


    game.appendChild(topPipe);

    game.appendChild(bottomPipe);


    pipes.push({

        x: 400,

        topHeight: topHeight,

        bottomHeight: bottomHeight,

        topElement: topPipe,

        bottomElement: bottomPipe,

        passed: false

    });

}


// ==========================================
// MOVE PIPES
// ==========================================

function movePipes() {

    for (
        let i = pipes.length - 1;
        i >= 0;
        i--
    ) {

        let pipe = pipes[i];


        pipe.x -= pipeSpeed;


        pipe.topElement.style.left =
            pipe.x + "px";

        pipe.bottomElement.style.left =
            pipe.x + "px";


        // Score

        if (
            !pipe.passed &&
            pipe.x + 60 < birdX
        ) {

            pipe.passed = true;

            score++;

            scoreDisplay.innerText =
                score;


            // Increase difficulty

            if (score % 5 === 0) {

                pipeSpeed += 0.3;

            }

        }


        // Remove pipe

        if (pipe.x < -70) {

            pipe.topElement.remove();

            pipe.bottomElement.remove();

            pipes.splice(i, 1);

        }

    }

}


// ==========================================
// COLLISION DETECTION
// ==========================================

function checkCollision() {

    // Bird boundaries

    const birdLeft = birdX;

    const birdRight =
        birdX + 40;

    const birdTop = birdY;

    const birdBottom =
        birdY + 30;


    // Ground collision

    if (birdBottom >= 575) {

        return true;

    }


    // Ceiling collision

    if (birdTop <= 0) {

        return true;

    }


    // Pipe collision

    for (let pipe of pipes) {

        const pipeLeft =
            pipe.x;

        const pipeRight =
            pipe.x + 60;


        // Is bird horizontally touching pipe?

        if (
            birdRight > pipeLeft &&
            birdLeft < pipeRight
        ) {

            // Top pipe collision

            if (
                birdTop < pipe.topHeight
            ) {

                return true;

            }


            // Bottom pipe collision

            const bottomPipeTop =
                600 -
                pipe.bottomHeight;

            if (
                birdBottom >
                bottomPipeTop
            ) {

                return true;

            }

        }

    }


    return false;

}


// ==========================================
// GAME LOOP
// ==========================================

function gameLoop() {

    if (!gameRunning) {

        return;

    }


    // Gravity

    velocity += gravity;

    birdY += velocity;


    // Move bird

    bird.style.top =
        birdY + "px";


    // Create pipes

    pipeTimer++;

    if (pipeTimer > 100) {

        createPipe();

        pipeTimer = 0;

    }


    // Move pipes

    movePipes();


    // Collision

    if (checkCollision()) {

        endGame();

        return;

    }


    // Continue

    requestAnimationFrame(
        gameLoop
    );

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

class FlappyHandler(
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

print("🐦 FLAPPY BIRD STYLE GAME")

print("----------------------------------------")

print(f"🌐 Opening http://localhost:{PORT}")

print("----------------------------------------")


server = http.server.HTTPServer(
    ("localhost", PORT),
    FlappyHandler
)


webbrowser.open(
    f"http://localhost:{PORT}"
)


server.serve_forever()
