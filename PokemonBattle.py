import http.server
import webbrowser
import random

# ==========================================
# SETTINGS
# ==========================================

PORT = 8007


# ==========================================
# GAME VARIABLES
# ==========================================

player_hp = 100
player_max_hp = 100

enemy_hp = 100
enemy_max_hp = 100

player_level = 1
player_xp = 0

battle_message = "A wild Flamecub appeared!"

game_over = False


# ==========================================
# RESET GAME
# ==========================================

def reset_game():

    global player_hp
    global enemy_hp
    global player_level
    global player_xp
    global battle_message
    global game_over

    player_hp = player_max_hp
    enemy_hp = enemy_max_hp

    player_level = 1
    player_xp = 0

    battle_message = "A wild Flamecub appeared!"

    game_over = False


# ==========================================
# PLAYER ATTACK
# ==========================================

def player_attack():

    global player_hp
    global enemy_hp
    global player_xp
    global player_level
    global battle_message
    global game_over

    if game_over:
        return

    damage = random.randint(15, 25)

    enemy_hp -= damage

    if enemy_hp < 0:
        enemy_hp = 0

    battle_message = (
        f"Sparkpaw used Thunder Claw! "
        f"It dealt {damage} damage."
    )

    # Check enemy defeat

    if enemy_hp <= 0:

        player_xp += 50

        if player_xp >= 100:

            player_level += 1
            player_xp = 0

            battle_message += (
                " 🎉 Enemy defeated! "
                f"Sparkpaw reached Level {player_level}!"
            )

        else:

            battle_message += (
                f" 🎉 Enemy defeated! "
                f"+50 XP"
            )

        game_over = True

        return

    enemy_attack()


# ==========================================
# SPECIAL ATTACK
# ==========================================

def special_attack():

    global player_hp
    global enemy_hp
    global player_xp
    global player_level
    global battle_message
    global game_over

    if game_over:
        return

    damage = random.randint(25, 40)

    enemy_hp -= damage

    if enemy_hp < 0:
        enemy_hp = 0

    battle_message = (
        f"Sparkpaw used Lightning Burst! "
        f"It dealt {damage} damage."
    )

    # Check enemy defeat

    if enemy_hp <= 0:

        player_xp += 75

        if player_xp >= 100:

            player_level += 1
            player_xp -= 100

        battle_message += (
            " ⚡ Critical attack! "
            "Enemy defeated!"
        )

        game_over = True

        return

    enemy_attack()


# ==========================================
# HEAL
# ==========================================

def heal():

    global player_hp
    global battle_message

    if game_over:
        return

    if player_hp >= player_max_hp:

        battle_message = (
            "Sparkpaw's HP is already full!"
        )

        return

    heal_amount = random.randint(15, 25)

    player_hp += heal_amount

    if player_hp > player_max_hp:
        player_hp = player_max_hp

    battle_message = (
        f"Sparkpaw recovered "
        f"{heal_amount} HP! 💚"
    )

    enemy_attack()


# ==========================================
# ENEMY ATTACK
# ==========================================

def enemy_attack():

    global player_hp
    global battle_message
    global game_over

    damage = random.randint(10, 20)

    player_hp -= damage

    if player_hp < 0:
        player_hp = 0

    battle_message += (
        f" Flamecub attacked back "
        f"and dealt {damage} damage."
    )

    if player_hp <= 0:

        battle_message = (
            "💥 Sparkpaw fainted! "
            "You lost the battle."
        )

        game_over = True


# ==========================================
# CREATE WEB PAGE
# ==========================================

def create_page():

    player_hp_percent = (
        player_hp / player_max_hp
    ) * 100

    enemy_hp_percent = (
        enemy_hp / enemy_max_hp
    ) * 100

    if game_over:

        if enemy_hp <= 0:

            result = "🏆 VICTORY!"

        else:

            result = "💀 DEFEAT!"

    else:

        result = "⚔️ BATTLE"


    page = f"""
<!DOCTYPE html>

<html>

<head>

<title>Monster Battle</title>

<style>

* {{
    box-sizing: border-box;
}}


body {{

    margin: 0;

    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            135deg,
            #1b2735,
            #090a0f
        );

    color: white;

    text-align: center;

}}


h1 {{

    margin-top: 20px;

    font-size: 40px;

}}


#battle {{

    width: 800px;

    max-width: 95%;

    height: 600px;

    margin: auto;

    position: relative;

    overflow: hidden;

    border-radius: 20px;

    background:
        linear-gradient(
            #6dd5ed,
            #2193b0
        );

    border: 5px solid white;

    box-shadow:
        0 0 30px
        rgba(255,255,255,0.3);

}}


/* =================================
   BATTLE FIELD
================================= */

.ground {{

    position: absolute;

    bottom: 0;

    width: 100%;

    height: 170px;

    background:
        linear-gradient(
            #6dbb45,
            #3c8128
        );

}}


/* =================================
   ENEMY AREA
================================= */

.enemy-area {{

    position: absolute;

    top: 60px;

    right: 70px;

}}


.enemy-monster {{

    width: 150px;

    height: 150px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #ff7043,
            #c62828
        );

    border: 6px solid #8e1c1c;

    font-size: 80px;

    display: flex;

    align-items: center;

    justify-content: center;

    box-shadow:
        0 10px 15px
        rgba(0,0,0,0.4);

}}


/* =================================
   PLAYER AREA
================================= */

.player-area {{

    position: absolute;

    bottom: 180px;

    left: 70px;

}}


.player-monster {{

    width: 170px;

    height: 170px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #42a5f5,
            #1565c0
        );

    border: 6px solid #0d47a1;

    font-size: 90px;

    display: flex;

    align-items: center;

    justify-content: center;

    box-shadow:
        0 10px 15px
        rgba(0,0,0,0.4);

}}


/* =================================
   HEALTH BOX
================================= */

.health-box {{

    background: white;

    color: #222;

    padding: 12px;

    border-radius: 12px;

    width: 230px;

    text-align: left;

    box-shadow:
        0 5px 10px
        rgba(0,0,0,0.3);

}}


.name {{

    font-size: 20px;

    font-weight: bold;

}}


.level {{

    float: right;

}}


.hp-label {{

    margin-top: 8px;

    font-weight: bold;

}}


.hp-bar {{

    width: 100%;

    height: 18px;

    background: #ddd;

    border-radius: 10px;

    overflow: hidden;

}}


.hp-fill {{

    height: 100%;

    width: {player_hp_percent}%;

    background: #32cd32;

    transition: width 0.3s;

}}


.enemy-hp-fill {{

    height: 100%;

    width: {enemy_hp_percent}%;

    background: #ff9800;

    transition: width 0.3s;

}}


/* =================================
   BATTLE MESSAGE
================================= */

.message-box {{

    position: absolute;

    bottom: 20px;

    left: 20px;

    width: 400px;

    min-height: 100px;

    background: rgba(255,255,255,0.95);

    color: #222;

    border: 4px solid #333;

    border-radius: 15px;

    padding: 15px;

    font-size: 17px;

    text-align: left;

}}


/* =================================
   ACTIONS
================================= */

.actions {{

    position: absolute;

    bottom: 20px;

    right: 20px;

    width: 300px;

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 10px;

}}


button {{

    padding: 15px;

    font-size: 16px;

    font-weight: bold;

    border: none;

    border-radius: 10px;

    cursor: pointer;

    background: white;

}}


button:hover {{

    transform: scale(1.04);

    background: #eeeeee;

}}


/* =================================
   RESULT
================================= */

.result {{

    position: absolute;

    top: 50%;

    left: 50%;

    transform:
        translate(-50%, -50%);

    background:
        rgba(0,0,0,0.9);

    padding: 30px 50px;

    border-radius: 20px;

    display: {"block" if game_over else "none"};

    z-index: 20;

}}


.result h2 {{

    font-size: 40px;

}}


.restart {{

    padding: 12px 25px;

    font-size: 18px;

}}


</style>

</head>


<body>


<h1>⚔️ Monster Battle</h1>


<div id="battle">


    <!-- GROUND -->

    <div class="ground"></div>


    <!-- ENEMY -->

    <div class="enemy-area">

        <div class="health-box">

            <span class="name">
                Flamecub
            </span>

            <span class="level">
                Lv. 5
            </span>

            <div class="hp-label">
                HP
            </div>

            <div class="hp-bar">

                <div
                    class="enemy-hp-fill">
                </div>

            </div>

            <div>
                {enemy_hp} / {enemy_max_hp}
            </div>

        </div>


        <div class="enemy-monster">
            🔥
        </div>

    </div>


    <!-- PLAYER -->

    <div class="player-area">

        <div class="player-monster">
            ⚡
        </div>


        <div class="health-box">

            <span class="name">
                Sparkpaw
            </span>

            <span class="level">
                Lv. {player_level}
            </span>

            <div class="hp-label">
                HP
            </div>

            <div class="hp-bar">

                <div
                    class="hp-fill">
                </div>

            </div>

            <div>
                {player_hp} / {player_max_hp}
            </div>

            <div style="margin-top:5px;">
                XP: {player_xp} / 100
            </div>

        </div>

    </div>


    <!-- MESSAGE -->

    <div class="message-box">

        {battle_message}

    </div>


    <!-- ACTIONS -->

    <div class="actions">

        <form method="GET">

            <input
                type="hidden"
                name="action"
                value="attack">

            <button type="submit">
                ⚔️ Attack
            </button>

        </form>


        <form method="GET">

            <input
                type="hidden"
                name="action"
                value="special">

            <button type="submit">
                ⚡ Special
            </button>

        </form>


        <form method="GET">

            <input
                type="hidden"
                name="action"
                value="heal">

            <button type="submit">
                💚 Heal
            </button>

        </form>


        <button onclick="location.reload()">
            🔄 Reset
        </button>

    </div>


    <!-- RESULT -->

    <div class="result">

        <h2>
            {result}
        </h2>

        <p>
            Final Score: {player_xp} XP
        </p>

        <button
            class="restart"
            onclick="location.reload()">

            🔄 Play Again

        </button>

    </div>


</div>


</body>

</html>
"""

    return page


# ==========================================
# WEB SERVER
# ==========================================

class BattleHandler(
    http.server.BaseHTTPRequestHandler
):

    def do_GET(self):

        global battle_message

        path = self.path

        # ------------------------------
        # ATTACK
        # ------------------------------

        if "action=attack" in path:

            player_attack()


        # ------------------------------
        # SPECIAL ATTACK
        # ------------------------------

        elif "action=special" in path:

            special_attack()


        # ------------------------------
        # HEAL
        # ------------------------------

        elif "action=heal" in path:

            heal()


        # ------------------------------
        # RESET
        # ------------------------------

        elif "reset" in path:

            reset_game()


        # ------------------------------
        # SEND PAGE
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


# ==========================================
# START SERVER
# ==========================================

reset_game()


print("----------------------------------------")
print("⚔️ MONSTER BATTLE GAME")
print("----------------------------------------")

print(
    f"🌐 Opening http://localhost:{PORT}"
)

print("----------------------------------------")


server = http.server.HTTPServer(
    ("localhost", PORT),
    BattleHandler
)


webbrowser.open(
    f"http://localhost:{PORT}"
)


server.serve_forever()
