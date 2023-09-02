import usocket as socket                        # import de la bibliothèque usocket
import network                                  # import de la bibliothèque network pour utiliser le WiFi
from machine import Pin, PWM                    # import de la bibliothèque machine pour contrôler les broches de l'ESP32 
import time, machine


wifissid = "Antho_oneplus9"                     # Nom du réseau WiFi
pwd = "aqzsedrf"                                # Mot de passe du réseau WiFi
led = Pin(2, Pin.OUT)                           # choix de la broche pour allumer une led 

# servo
servo = machine.PWM(machine.Pin(14), freq=50)
angle = 0


# fonction pour connecter l'ESP32 au WiFi
def connexion_wifi(ssid, password):             
    wlan = network.WLAN(network.STA_IF)         # initialisation de l'interface WiFi de l'ESP32
    wlan.active(True)                           # activation de l'interface WiFi
    if not wlan.isconnected():                  # si l'ESP32 n'est pas encore connectée au WiFi
        print("connexion", ssid)
        wlan.connect(ssid, password)            # connexion au WiFi
        while not wlan.isconnected():           # tant que l'ESP32 n'est pas connecté au WiFi
            pass                                # ne rien faire
    print("Adresse IP :", wlan.ifconfig()[0])      # affichage de l'adresse IP de l'ESP32
    print("Masque réseau : ", wlan.ifconfig()[1])  # affichage du masque réseau de l'ESP32
    print("Gateway :", wlan.ifconfig()[2])         # affichage de la gateway de l'ESP32
    print("Serveur DNS :", wlan.ifconfig()[3])     # affichage du serveur DNS de l'ESP32
    return wlan.ifconfig()[0]                      # renvoi de l'adresse IP de l'ESP32


AdresseIP = connexion_wifi(wifissid, pwd)              # appel de la fonction connexion_wifi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # création d'un objet socket pour écouter les requêtes HTTP
s.bind((AdresseIP, 80))                                # associe l'objet socket à l'adresse IP + port 80 (port par défaut pour les requêtes HTTP)
s.listen(1)                                            # mise en écoute de l'objet socket (1 client maximum)
socketServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création d'un socket avec le protocole AF_INET
socketServeur.bind(('', 8080))                                    #spécifie où écouter les connexions entrantes, sur le port 80
socketServeur.listen(5)                                           #nombre max de connexions en simultanées 

    
def web_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fox Bot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 100%;
                margin: 0 auto;
                text-align: center;
            }
            h1 {
                font-size: 28px;
                margin-top: 30px;
            }
            /* pour définir la taille de l'image de l'entreprise. */
            .company-image {
                width: 20%;
                margin-top: 30px;
                border: 5px solid #ccc; 
            }
            .button {
                display: inline-block;
                margin: 10px;
                border: none;
                background-color: #FAF0E6; 
                color: white;
                padding: 20px 40px; /*ajoute de l'espace entre le contenu du bouton et ses bords, créant ainsi l'effet de volume */
                border-radius: 30px; /*arrondit les bords */
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
                box-shadow: 3px 3px 3px 0px rgba(0,0,0,0.5), 0px 0px 0px 1px rgba(255,255,255,0.5); 
                border: 1px solid #FCE903; /* Ajout d'une bordure */
                transition: all 0.3s ease-in-out; /*transition lors du passage de la souris sur le bouton */
            }
            /* La classe .button img est utilisée pour définir la taille et l'espacement des images des boutons. */
            .button img {
                max-height: 50px;
                margin-right: 10px;
                vertical-align: middle;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- <h1>Fox Bot</h1> -->
            <img class="company-image" src="https://cdn.discordapp.com/attachments/1046735136328269848/1076102597599055882/image.png" alt="company logo">
            <div class="buttons">
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386900896829530/assis.png" alt="button image"></button>
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386901127503933/attaque.png" alt="button image"></button> 
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386901903458417/debout.png" alt="button image"></button>
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386901635026974/debout_disant_bonjour.png" alt="button image"></button>
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386903111422073/triste.png" alt="button image"></button>
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386901374976091/bras_leves.png" alt="button image"></button> 
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386902822010961/perplexe.png" alt="button image"></button> 
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386902239006720/enerve.png" alt="button image"></button>
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386902553567242/lover.png" alt="button image"></button> 
                <button class="button"><img src="https://cdn.discordapp.com/attachments/922061720166481980/1083386900607418419/couche.png" alt="button image"></button> 
                <p><a href="/?led=on" onclick="event.preventDefault(); fetch('/?led=on').then(() => { console.log('LED carte allumée'); });"><button class="button">Bouton Test led</button></a></p>
                <p><a href="/" onclick="event.preventDefault(); fetch('/?servo=on').then(() => { console.log('Servo moteur activé'); });"><button class="button">Bouton Test servo</button></a></p>
            </div>
        </div>     
    </body>
    </html>
    """
    return html

# # Fonction pour contrôler le servo en lui donnant un angle précis
# def control_servo(angle):
#     duty = int(40 + angle * 8 / 180)  # Conversion de l'angle en valeur de devoir
#     servo.duty(duty)                  # Réglage de la valeur de devoir pour déplacer le servo à l'angle souhaité
#     time.sleep(0.1)                   # Attente pour que le servo atteigne la position désirée
#     print("Le servo a été déplacé à l'angle", angle)


# Fonction pour contrôler le servo
def control_servo():
    global angle
    
    if angle == 90:
        angle = 45
        print ("90 donc passage à 45")
    else:
        angle = 90

    duty = int(40 + angle * 100 / 180)  # Conversion de l'angle en valeur de devoir
    servo.duty(duty)                    # Réglage de la valeur de devoir pour déplacer le servo à l'angle souhaité
    time.sleep(0.1)                     # Attente pour que le servo atteigne la position désirée
    print("Le servo a été déplacé à l'angle", angle)


# boucle principale gérant la communication avec le client et effectue des actions en fonction des requêtes HTTP
while True:
    try:
        # libération de memoire si supérieure a 102ko
        if gc.mem_free() < 102000:
            gc.collect()
            
        # attente d'une connexion client (se connecter à la page web) et acceptation avec affichage de l'adresse IP du client
        print("Attente connexion d'un client")
        connexionClient, adresse = socketServeur.accept()
        connexionClient.settimeout(0.5)
        print("Connecté avec le client", adresse)
            
        # attente de la requête du client , sera stockée dans une variable requête
        print("Attente requete du client")
        requete = connexionClient.recv(1024)     # requête du client
        requete = str(requete)
        print("Requete du client =", requete)
        connexionClient.settimeout(None)
        
        # envoi d'une réponse HTTP au client avec le code HTML de la fonction web_page()
        print("Envoi reponse du serveur : code HTML a afficher")
        connexionClient.send('HTTP/1.1 200 OK\n')
        connexionClient.send('Content-Type: text/html\n')
        connexionClient.send("Connection: close\n\n")
        reponse = web_page()
        connexionClient.sendall(reponse)
            
#         if '/?servo=on' in requete:
#             print("Servo moteur activé")
#             control_servo()  # Déplace le servo lorsque le bouton est cliqué
#             
#         if '/?led=on' in requete:
#             print("LED allumée")
#             led.value(1)
        
        
        if '/?servo=on' in requete:
            print("Servo moteur activé")
            control_servo()
            
        elif '/?led=on' in requete:
            print("LED allumée")
            led.value(1)
            
        else:
            print("Requête non reconnue")
        
        
        # Fermeture de la connexion après avoir traité la requête
        connexionClient.close()  
        print("Connexion avec le client fermée")
        
    # s'il y a eu une erreur lors du Try, on ferme la connexion avec le client en affichant l'erreur 
    except:
        connexionClient.close()  
        print("Connexion avec le client fermée, le programme a déclenché une erreur")

