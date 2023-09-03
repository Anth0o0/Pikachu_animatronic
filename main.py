# main avant modif septembre 


import usocket as socket                        # import de la bibliothèque usocket
import network                                  # import de la bibliothèque network pour utiliser le WiFi
from machine import Pin, PWM                    # import de la bibliothèque machine pour contrôler les broches de l'ESP32 
import time, machine
import os


# attribution des pins et PWM pour chaque servo
servo_oreilleG = machine.PWM(machine.Pin(8), freq=50)
servo_oreilleD = machine.PWM(machine.Pin(9), freq=50)
servo_brasG = machine.PWM(machine.Pin(11), freq=50)
servo_brasD = machine.PWM(machine.Pin(12), freq=50)
servo_piedG = machine.PWM(machine.Pin(13), freq=50)
servo_piedD = machine.PWM(machine.Pin(14), freq=50)
servo_queue = machine.PWM(machine.Pin(29), freq=50)
servo_teteX = machine.PWM(machine.Pin(30), freq=50)
servo_teteY = machine.PWM(machine.Pin(33), freq=50)
servo_buste = machine.PWM(machine.Pin(36), freq=50)



#initialisation des 10 servos moteurs 
angle_oreilleG, angle_oreilleD, angle_brasG, angle_brasD, angle_piedG, angle_piedD = 0 
angle_queue, angle_teteX, angle_teteY, angle_buste  = 0


# configuration de l'ESP32 en point d'accès wifi
def start_access_point():
    ap = network.WLAN(network.AP_IF)                 # configure en mode point d'accès wifi 
    ap.active(True)                                  # active l'interface en mode point d'accès 
    ap.config(essid="FoxBot", password="pikachu")    # configure le nom et mot de passe du réseau 

    
def web_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fox Bot</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(90deg, #FFFEBD, #FAF84E);
            }
            .container {
                max-width: 100%;
                margin: 0 auto;
                text-align: center;
            }

            h1 {
                font-size: 40px;
                margin-top: 20px;
                font-family: "Helvetica Neue", sans-serif;
            }
            h2 {
                font-size: 24px;
                position: fixed;
                top: 55%; /* gère la hauteur de page */
                left: 15%; /* centre horizontalement */
                transform: translate(-50%, -50%); /* Centre l'élément verticalement et horizontalement */
                font-family: "Helvetica Neue", sans-serif;
            }

            .button-group {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                position: fixed;
                top: 60%;   /*permet de placer les boutons controlant chaque servo en bas */
                transform: translateY(-1px);
            }

            .buttons-positions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 10%;
            }

            .button {
                margin: 15px 10px;
                border: none;
                background-color: black; 
                color: white;
                padding: 20px 40px;
                border-radius: 10px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
                box-shadow: 3px 3px 3px 0px rgba(0,0,0,0.5), 0px 0px 0px 1px rgba(255,255,255,0.5);
                transition: all 0.3s ease-in-out;
            }

            /* actions au survol */
            .button:hover {
                background-color: #854625; 
                color: white; 
                transform: translate(0, -5px) scale(1.1);
            }

            /* Ligne de séparation horizontale */
            .separator {
                width: 100%;
                border-top: 2px solid #000;
                height: 2px;
                background-color: #000;
                position: fixed;
                top: 50%; /* Place la ligne au milieu de la hauteur de la page */
                transform: translateY(-1px); /* Centre la ligne verticalement */
            }

            /* Styles pour la fenêtre A propose de FoxBot */
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.7);
            }
            .modal-content {
                background-color: white;
                margin: 10% auto;
                padding: 20px;
                border-radius: 5px;
                width: 60%;
            }
            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
            }

            /* placement du bouton "a propos de FoxBot" */
            #aboutBtn {
                position: fixed;
                top: 1%;
                left: 82%;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FoxBot</h1>

            <!-- Bouton "À propos de FoxBot" -->
            <button class="button" id="aboutBtn">À propos de FoxBot</button>

            <!-- Le contenu de la fenêtre modale -->
            <div id="myModal" class="modal">
                <div class="modal-content">
                    <span class="close" id="closeBtn">&times;</span>
                    <p>Société FoxBot, 2023, siège social: Bordeaux, FRANCE</p>
                </div>
            </div>
            <div class="buttons-positions">
                <button class="button" id="buttonStand" onclick="Stand()">Pikachu debout</button>
                <button class="button" id="buttonSit" onclick="Sit()">Pikachu assis</button>
                <button class="button" id="buttonSad" onclick="Sad()">Pikachu triste</button> 
                <button class="button" id="buttonHappy" onclick="Happy()">Pikachu joyeux</button> 
            </div>

            <!-- Ligne de séparation horizontale centrée -->
            <div class="separator"></div>
            <h2>Pour contrôler chaque servo : </h2>
            <!-- Boutons pour contrôler chaque servo un par un -->
            <div class="button-group">
                <button class="button" id="buttonOreilleG" onclick="OreilleG()">Oreille gauche</button>
                <button class="button" id="buttonOreilleD" onclick="OreilleD()">Oreille droite</button>
                <button class="button" id="buttonTeteX" onclick="TeteX()">Tête sur X</button> 
                <button class="button" id="buttonTeteY" onclick="TeteY()">Tête sur Y </button> 
                <button class="button" id="buttonBuste" onclick="Buste()">Buste</button>
                <button class="button" id="buttonQueue" onclick="Queue()">Queue</button>
                <button class="button" id="buttonBrasG" onclick="BrasG()">Bras gauche</button> 
                <button class="button" id="buttonBrasD" onclick="BrasD()">Bras droit</button> 
                <button class="button" id="buttonPiedG" onclick="PiedG()">Pied gauche</button>
                <button class="button"id="buttonPiedD" onclick="PiedD()">Pied droit</button>
            </div>
        </div>
        <script>
            // récupère l'élément "A propos de FoxBot"
            var aboutBtn = document.getElementById("aboutBtn");
            
            // récupère l'élément de la fenêtre du a propos 
            var modal = document.getElementById("myModal");
            
            // récupère la croix de fermeture dans la fenêtre a propos
            var closeBtn = document.getElementById("closeBtn");

            // Affiche la fenêtre modale lorsque vous cliquez sur le bouton
            aboutBtn.onclick = function() {
                modal.style.display = "block";
            }

            // Ferme la fenêtre modale lorsque vous cliquez sur la croix
            closeBtn.onclick = function() {
                modal.style.display = "none";
            }

            // Ferme la fenêtre modale si vous cliquez en dehors de celle-ci
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }

            // envoie la requête pour gérer la position debout du Pikachu
            function Stand() {
                fetch('/?Stand=on').then(() => {
                    console.log('Position debout activée');
                });
            }

            // envoie la requête pour gérer la assise debout du Pikachu
            function Sit() {
                fetch('/?Sit=on').then(() => {
                    console.log('Position assise activée');
                });
            }

            // envoie la requête pour gérer la position triste du Pikachu
            function Sad() {
                fetch('/?Sad=on').then(() => {
                    console.log('Position triste activée');
                });
            }

            // envoie la requête pour gérer la position joyeuse du Pikachu
            function Happy() {
                fetch('/?Happy=on').then(() => {
                    console.log('Position joyeuse activée');
                });
            }

            // envoie la requête pour gérer l'angle de l'oreille gauche du Pikachu
            function OreilleG() {
                fetch('/?OreilleG=on').then(() => {
                    console.log('Oreille gauche activée');
                });
            }

            function OreilleD() {
                fetch('/?OreilleD=on').then(() => {
                    console.log('Oreille droite activée');
                });
            }

            function TeteX() {
                fetch('TeteX/?=on').then(() => {
                    console.log('Tete sur X activée');
                });
            }

            function TeteY() {
                fetch('TeteY/?=on').then(() => {
                    console.log('Tete sur Y activée');
                });
            }

            function Buste() {
                fetch('Buste/?=on').then(() => {
                    console.log('Buste activé');
                });
            }

            function Queue() {
                fetch('Queue/?=on').then(() => {
                    console.log('Queue activée');
                });
            }

            function BrasG() {
                fetch('BrasG/?=on').then(() => {
                    console.log('Bras gauche activé');
                });
            }

            function BrasD() {
                fetch('BrasD/?=on').then(() => {
                    console.log('Bras droit activé');
                });
            }

            function PiedG() {
                fetch('PiedG/?=on').then(() => {
                    console.log('Pied gauche activé');
                });
            }

            function PiedD() {
                fetch('PiedD/?=on').then(() => {
                    console.log('Pied droit activé');
                });
            }
        </script>
    </body>
    </html>

    """
    return html


# positionne le Pikachu debout
def Stand(): 
    angle_piedG = 10
    duty = int(40 + angle_piedG * 100 / 180)  # Conversion de l'angle en valeur 
    servo.duty(duty)                          # Réglage de la valeur de devoir pour déplacer le servo à l'angle
    time.sleep(0.1)                           # Attente pour que le servo atteigne la position désirée
    
    angle_piedD = 170 
    duty = int(40 + angle_piedD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)                           

    angle_brasG = 10
    duty = int(40 + angle_brasG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_brasD = 170
    duty = int(40 + angle_brasD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

     angle_queue = 90
    duty = int(40 + angle_queue * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1) 

    angle_buste = 0
    duty = int(40 + angle_buste * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)     

    angle_teteX = 90
    duty = int(40 + angle_teteX * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_teteY = 0
    duty = int(40 + angle_teteY * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_oreilleG = 80
    duty = int(40 + angle_oreilleG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)  

    angle_oreilleD = 100
    duty = int(40 + angle_oreilleD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    print ("angle_piedG: , angle_piedD: , angle_brasG: , angle_brasD: , angle_queue: ", angle_piedG, angle_piedD, angle_brasG, angle_brasD, angle_queue)
    print("angle_buste: , angle_teteX: , angle_teteY: , angle_oreilleG: , angle_oreilleD: ", angle_buste, angle_teteX, angle_teteY, angle_oreilleG, angle_oreilleD)


# positionne le Pikachu assis
def Sit(): 
    angle_piedG = 10
    duty = int(40 + angle_piedG * 100 / 180)   
    servo.duty(duty)                         
    time.sleep(0.1)                           
    
    angle_piedD = 170 
    duty = int(40 + angle_piedD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)                           

    angle_brasG = 30
    duty = int(40 + angle_brasG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_brasD = 150
    duty = int(40 + angle_brasD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

     angle_queue = 160
    duty = int(40 + angle_queue * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1) 

    angle_buste = 180
    duty = int(40 + angle_buste * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)     

    angle_teteX = 90
    duty = int(40 + angle_teteX * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_teteY = 0
    duty = int(40 + angle_teteY * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_oreilleG = 50
    duty = int(40 + angle_oreilleG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)  

    angle_oreilleD = 130
    duty = int(40 + angle_oreilleD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    print ("angle_piedG: , angle_piedD: , angle_brasG: , angle_brasD: , angle_queue: ", angle_piedG, angle_piedD, angle_brasG, angle_brasD, angle_queue)
    print("angle_buste: , angle_teteX: , angle_teteY: , angle_oreilleG: , angle_oreilleD: ", angle_buste, angle_teteX, angle_teteY, angle_oreilleG, angle_oreilleD)


# position montrant le Pikachu triste
def Sad(): 
    angle_piedG = 30
    duty = int(40 + angle_piedG * 100 / 180)  # Conversion de l'angle en valeur 
    servo.duty(duty)                          # Réglage de la valeur de devoir pour déplacer le servo à l'angle
    time.sleep(0.1)                           
    
    angle_piedD = 150 
    duty = int(40 + angle_piedD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)                           

    angle_brasG = 40
    duty = int(40 + angle_brasG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_brasD = 140
    duty = int(40 + angle_brasD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

     angle_queue = 10
    duty = int(40 + angle_queue * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1) 

    angle_buste = 30
    duty = int(40 + angle_buste * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)     

    angle_teteX = 120
    duty = int(40 + angle_teteX * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_teteY = 20
    duty = int(40 + angle_teteY * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_oreilleG = 30
    duty = int(40 + angle_oreilleG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)  

    angle_oreilleD = 150
    duty = int(40 + angle_oreilleD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    print ("angle_piedG: , angle_piedD: , angle_brasG: , angle_brasD: , angle_queue: ", angle_piedG, angle_piedD, angle_brasG, angle_brasD, angle_queue)
    print("angle_buste: , angle_teteX: , angle_teteY: , angle_oreilleG: , angle_oreilleD: ", angle_buste, angle_teteX, angle_teteY, angle_oreilleG, angle_oreilleD)


# position montrant le Pikachu joyeux
def Happy(): 
    angle_piedG = 100
    duty = int(40 + angle_piedG * 100 / 180)  # Conversion de l'angle en valeur 
    servo.duty(duty)                          # Réglage de la valeur de devoir pour déplacer le servo à l'angle
    time.sleep(0.1)                           # Attente pour que le servo atteigne la position désirée
    
    angle_piedD = 80 
    duty = int(40 + angle_piedD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)                           

    angle_brasG = 70
    duty = int(40 + angle_brasG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_brasD = 110
    duty = int(40 + angle_brasD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

     angle_queue = 160
    duty = int(40 + angle_queue * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1) 

    angle_buste = 0
    duty = int(40 + angle_buste * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)     

    angle_teteX = 70
    duty = int(40 + angle_teteX * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_teteY = 0
    duty = int(40 + angle_teteY * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    angle_oreilleG = 120
    duty = int(40 + angle_oreilleG * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)  

    angle_oreilleD = 60
    duty = int(40 + angle_oreilleD * 100 / 180)  
    servo.duty(duty)                          
    time.sleep(0.1)   

    print ("angle_piedG: , angle_piedD: , angle_brasG: , angle_brasD: , angle_queue: ", angle_piedG, angle_piedD, angle_brasG, angle_brasD, angle_queue)
    print("angle_buste: , angle_teteX: , angle_teteY: , angle_oreilleG: , angle_oreilleD: ", angle_buste, angle_teteX, angle_teteY, angle_oreilleG, angle_oreilleD)

# fonctions permettant de bouger chaque servo de 1à degrés à chaque appui bouton 
def PiedG(): 
    global angle_piedG  
    angle_piedG += 10  # Incrémente l'angle de 10 degrés
    if angle_piedG > 180:
        angle_piedG = 180  # Limite l'angle à 180 degrés maximum
    duty = int(40 + angle_piedG * 100 / 180)  # Conversion de l'angle en valeur
    servo_piedG.duty(duty)  # Définit la position du servo
    time.sleep(0.1)


def PiedD(): 
    global angle_piedD  
    angle_piedD += 10  
    if angle_piedD > 180:
        angle_piedD = 180  
    duty = int(40 + angle_piedD * 100 / 180)  
    servo_piedD.duty(duty)  
    time.sleep(0.1)


def BrasG(): 
    global angle_brasG
    angle_brasG += 10
    if angle_brasG > 180:
        angle_brasG = 180
    duty = int(40 + angle_brasG * 100 / 180)
    servo_brasG.duty(duty)
    time.sleep(0.1)

def BrasD(): 
    global angle_brasD
    angle_brasD += 10
    if angle_brasD > 180:
        angle_brasD = 180
    duty = int(40 + angle_brasD * 100 / 180)
    servo_brasD.duty(duty)
    time.sleep(0.1)



def Queue(): 
    global angle_queue
    angle_queue += 10
    if angle_queue > 180:
        angle_queue = 180
    duty = int(40 + angle_queue * 100 / 180)
    servo_queue.duty(duty)
    time.sleep(0.1)

def Buste(): 
    global angle_buste
    angle_buste += 10
    if angle_buste > 180:
        angle_buste = 180
    duty = int(40 + angle_buste * 100 / 180)
    servo_buste.duty(duty)
    time.sleep(0.1)

def TeteX(): 
    global angle_teteX
    angle_teteX += 10
    if angle_teteX > 180:
        angle_teteX = 180
    duty = int(40 + angle_teteX * 100 / 180)
    servo_teteX.duty(duty)
    time.sleep(0.1)

def TeteY(): 
    global angle_teteY
    angle_teteY += 10
    if angle_teteY > 180:
        angle_teteY = 180
    duty = int(40 + angle_teteY * 100 / 180)
    servo_teteY.duty(duty)
    time.sleep(0.1)

def OreilleG(): 
    global angle_oreilleG
    angle_oreilleG += 10
    if angle_oreilleG > 180:
        angle_oreilleG = 180
    duty = int(40 + angle_oreilleG * 100 / 180)
    servo_oreilleG.duty(duty)
    time.sleep(0.1)

def OreilleD(): 
    global angle_oreilleD
    angle_oreilleD += 10
    if angle_oreilleD > 180:
        angle_oreilleD = 180
    duty = int(40 + angle_oreilleD * 100 / 180)
    servo_oreilleD.duty(duty)
    time.sleep(0.1)



# Boucle principale
while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()

        start_access_point()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("192.168.4.1", 80))
        s.listen(5)

        print("Point d'accès démarré")

        while True:
            conn, addr = s.accept()
            print("Connecté avec le client", addr)

            req = conn.recv(1024)
            req = str(req)
            print("Requête du client =", req)

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send("Connection: close\n\n")
            response = web_page()
            conn.sendall(response)  


            # suite à un appui bouton, il appelera la fonction associée 
            if '/?Stand=on' in req:
                Stand()

             if '/?Sit=on' in req:
                Sit()

            if '/?Sad=on' in req:
                Sad()

            if '/?Happy=on' in req:
                Happy()

            if '/?OreilleD=on' in req:
                OreilleD()

            if '/?TeteX=on' in req:
                TeteX()

            if '/?TeteY=on' in req:
                TeteY()

            if '/?Buste=on' in req:
                Buste()

            if '/?Queue=on' in req:
                Queue()

            if '/?BrasG=on' in req:
                BrasG()

            if '/?BrasD=on' in req:
                BrasD()

            if '/?PiedG=on' in req:
                PiedG()

            if '/?PiedD=on' in req:
                PiedD()

            else:
                print("Requête non reconnue")

            conn.close()  #arrête la connexion avec le client
            print("Connexion avec le client fermée")

    except Exception as e:
        print("Une erreur s'est produite:", e)
   



