import http.server
import webbrowser

# ==========================================
# SETTINGS
# ==========================================

PORT = 8006


# ==========================================
# CREATE WEB PAGE
# ==========================================

def create_page():

    return """
<!DOCTYPE html>

<html>

<head>

    <title>Space Shooter</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: #050510;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            overflow: hidden;
        }

        h1 {
            margin: 15px 0 5px;
            font-size: 38px;
        }

        .info {
            font-size: 20px;
            margin-bottom: 10px;
        }

        #game {

            width: 500px;
            height: 650px;

            margin: auto;

            position: relative;

            overflow: hidden;

            background:
                radial-gradient(circle at 20% 20%, white 1px, transparent 2px),
                radial-gradient(circle at 70% 40%, white 1px, transparent 2px),
                radial-gradient(circle at 40% 80%, white 1px, transparent 2px),
                radial-gradient(circle at 90% 15%, white 1px, transparent 2px),
                #080820;

            background-size:
                150px 150px,
                200px 200px,
                180px 180px,
                220px 220px;

            border: 4px solid white;

            box-shadow:
                0 0 25px rgba(255,255,255,0.3);
        }


        /* =================================
           PLAYER
        ================================= */

        #player {

            position: absolute;

            width: 50px;
            height: 60px;

            left: 225px;
            bottom: 25px;

            background: #28a9ff;

            clip-path: polygon(
                50% 0%,
                100% 100%,
                50% 75%,
                0% 100%
            );

            z-index: 10;
        }


        /* =================================
           BULLET
        ================================= */

        .bullet {

            position: absolute;

            width: 6px;
            height: 18px;

            background: yellow;

            border-radius: 5px;

            box-shadow:
                0 0 8px yellow;
        }


        /* =================================
           ENEMY
        ================================= */

        .enemy {

            position: absolute;

            width: 50px;
            height: 45px;

            background: #ff304f;

            border-radius: 50% 50% 20% 20%;

            box-shadow:
                0 0 10px rgba(255,0,0,0.5);
        }

        .enemy::before {

            content: "";

            position: absolute;

            width: 10px;
            height: 10px;

            background: yellow;

            border-radius: 50%;

            left: 10px;
            top: 15px;

            box-shadow:
                20px 0 yellow;
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

            background: rgba(0,0,0,0.75);

            z-index: 30;

            display: flex;

            flex-direction: column;

            justify-content: center;

            align-items: center;
        }

        #startScreen h2 {

            font-size: 35px;

            margin: 10px;
        }

        #startButton {

            padding: 12px 30px;

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

            height: 100%;

            top: 0;
            left: 0;

            background: rgba(0,0,0,0.8);

            z-index: 40;

            display: none;

            flex-direction: column;

            justify-content: center;

            align-items: center;
        }

        #gameOver h2 {

            font-size: 38px;

            margin: 10px;
        }

        #restartButton {

            padding: 12px 25px;

            font-size: 18px;

            border: none;

            border-radius: 8px;

            cursor: pointer;
        }


        /* =================================
           INSTRUCTIONS
        ================================= */

        .instructions {

            margin-top: 10px;

            font-size: 16px;

        }

    </style>

</head>


<body>


<h1>🚀 Space Shooter</h1>


<div class="info">

    Score:
    <span id="score">0</span>

    &nbsp;&nbsp;|&nbsp;&nbsp;

    Lives:
    <span id="lives">3</span>

</div>


<div id="game">


    <!-- PLAYER -->

    <div id="player"></div>


    <!-- START SCREEN -->

    <div id="startScreen">

        <h2>🚀 Space Shooter</h2>

        <p>Defeat the enemy ships!</p>

        <button id="startButton"
                onclick="startGame()">

            ▶️ Start Game

        </button>

    </div>


    <!-- GAME OVER -->

    <div id="gameOver">

        <h2>💥 GAME OVER</h2>

        <p>

            Final Score:
            <span id="finalScore">0</span>

        </p>

        <button id="restartButton"
                onclick="restartGame()">

            🔄 Restart

        </button>

    </div>


</div>


<div class="instructions">

    ⬅️ ➡️ Move &nbsp;&nbsp; | &nbsp;&nbsp;
    SPACE = Shoot

</div>


<script>


// ==========================================
// GAME ELEMENTS
// ==========================================

const game =
    document.getElementById("game");

const player =
    document.getElementById("player");

const scoreDisplay =
    document.getElementById("score");

const livesDisplay =
    document.getElementById("lives");

const startScreen =
    document.getElementById("startScreen");

const gameOverScreen =
    document.getElementById("gameOver");

const finalScore =
    document.getElementById("finalScore");


// ==========================================
// GAME VARIABLES
// ==========================================

let playerX = 225;

let score = 0;

let lives = 3;

let gameRunning = false;

let bullets = [];

let enemies = [];

let keys = {};

let enemyTimer = 0;

let enemySpeed = 2;


// ==========================================
// KEYBOARD CONTROLS
// ==========================================

document.addEventListener(
    "keydown",
    function(event) {

        keys[event.code] = true;

        // Prevent page scrolling

        if (
            event.code === "ArrowLeft" ||
            event.code === "ArrowRight" ||
            event.code === "Space"
        ) {

            event.preventDefault();

        }

        // Shoot

        if (
            event.code === "Space" &&
            gameRunning
        ) {

            shoot();

        }

    }
);


document.addEventListener(
    "keyup",
    function(event) {

        keys[event.code] = false;

    }
);


// ==========================================
// START GAME
// ==========================================

function startGame() {

    playerX = 225;

    score = 0;

    lives = 3;

    bullets = [];

    enemies = [];

    enemyTimer = 0;

    enemySpeed = 2;

    gameRunning = true;


    player.style.left =
        playerX + "px";


    scoreDisplay.innerText =
        score;

    livesDisplay.innerText =
        lives;


    startScreen.style.display =
        "none";

    gameOverScreen.style.display =
        "none";


    // Remove old objects

    document
        .querySelectorAll(".bullet")
        .forEach(
            bullet => bullet.remove()
        );

    document
        .querySelectorAll(".enemy")
        .forEach(
            enemy => enemy.remove()
        );


    gameLoop();

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


    // Keep player inside game

    if (playerX < 5) {

        playerX = 5;

    }


    if (playerX > 445) {

        playerX = 445;

    }


    player.style.left =
        playerX + "px";

}


// ==========================================
// SHOOT BULLET
// ==========================================

function shoot() {

    const bullet =
        document.createElement("div");

    bullet.className =
        "bullet";


    const bulletX =
        playerX + 22;


    const bulletY =
        570;


    bullet.style.left =
        bulletX + "px";

    bullet.style.top =
        bulletY + "px";


    game.appendChild(bullet);


    bullets.push({

        element: bullet,

        x: bulletX,

        y: bulletY

    });

}


// ==========================================
// MOVE BULLETS
// ==========================================

function moveBullets() {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

        let bullet =
            bullets[i];


        bullet.y -= 10;


        bullet.element.style.top =
            bullet.y + "px";


        // Remove bullet

        if (bullet.y < -20) {

            bullet.element.remove();

            bullets.splice(i, 1);

        }

    }

}


// ==========================================
// CREATE ENEMY
// ==========================================

function createEnemy() {

    const enemy =
        document.createElement("div");

    enemy.className =
        "enemy";


    const x =
        Math.floor(
            Math.random() * 440
        );


    enemy.style.left =
        x + "px";

    enemy.style.top =
        "-60px";


    game.appendChild(enemy);


    enemies.push({

        element: enemy,

        x: x,

        y: -60

    });

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

        let enemy =
            enemies[i];


        enemy.y += enemySpeed;


        enemy.element.style.top =
            enemy.y + "px";


        // Enemy reaches player area

        if (enemy.y > 650) {

            enemy.element.remove();

            enemies.splice(i, 1);

            loseLife();

            continue;

        }


        // Enemy hits player

        if (
            checkCollision(
                player,
                enemy.element
            )
        ) {

            enemy.element.remove();

            enemies.splice(i, 1);

            loseLife();

        }

    }

}


// ==========================================
// BULLET VS ENEMY
// ==========================================

function checkBulletCollisions() {

    for (
        let i = bullets.length - 1;
        i >= 0;
        i--
    ) {

        let bullet =
            bullets[i];


        for (
            let j = enemies.length - 1;
            j >= 0;
            j--
        ) {

            let enemy =
                enemies[j];


            if (
                checkCollision(
                    bullet.element,
                    enemy.element
                )
            ) {

                // Remove bullet

                bullet.element.remove();

                bullets.splice(i, 1);


                // Remove enemy

                enemy.element.remove();

                enemies.splice(j, 1);


                // Increase score

                score++;

                scoreDisplay.innerText =
                    score;


                // Increase difficulty

                if (score % 5 === 0) {

                    enemySpeed += 0.3;

                }


                break;

            }

        }

    }

}


// ==========================================
// COLLISION DETECTION
// ==========================================

function checkCollision(
    object1,
    object2
) {

    const a =
        object1.getBoundingClientRect();

    const b =
        object2.getBoundingClientRect();


    return !(
        a.bottom < b.top ||
        a.top > b.bottom ||
        a.right < b.left ||
        a.left > b.right
    );

}


// ==========================================
// LOSE LIFE
// ==========================================

function loseLife() {

    if (!gameRunning) {

        return;

    }


    lives--;


    livesDisplay.innerText =
        lives;


    if (lives <= 0) {

        endGame();

    }

}


// ==========================================
// GAME LOOP
// ==========================================

function gameLoop() {

    if (!gameRunning) {

        return;

    }


    movePlayer();

    moveBullets();

    moveEnemies();

    checkBulletCollisions();


    // Create enemies

    enemyTimer++;


    if (enemyTimer > 70) {

        createEnemy();

        enemyTimer = 0;

    }


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
        "flex";

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

class SpaceShooterHandler(
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
print("🚀 SPACE SHOOTER")
print("----------------------------------------")

print(f"🌐 Opening http://localhost:{PORT}")

print("----------------------------------------")


server = http.server.HTTPServer(
    ("localhost", PORT),
    SpaceShooterHandler
)


webbrowser.open(
    f"http://localhost:{PORT}"
)


server.serve_forever()
