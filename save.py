import usocket as socket                        # import de la bibliothèque usocket, une implémentation de socket optimisée pour les microcontrôleurs
import network                                  # import de la bibliothèque network pour utiliser le WiFi
from machine import Pin                         # import de la bibliothèque machine pour contrôler les broches de l'ESP32

wifissid = "..."                     # Nom du réseau WiFi
pwd = "..."                                # Mot de passe du réseau WiFi
led_1 = Pin(33, Pin.OUT)                        # choix de la broche pour allumer une led 

def connexion_wifi(ssid, password):             # fonction pour connecter l'ESP32 au WiFi
    wlan = network.WLAN(network.STA_IF)         # initialisation de l'interface WiFi de l'ESP32
    wlan.active(True)                           # activation de l'interface WiFi
    if not wlan.isconnected():                  # si l'ESP32 n'est pas encore connecté au WiFi
        print("connexion", ssid)
        wlan.connect(ssid, password)            # connexion au WiFi avec les identifiants spécifiés
        while not wlan.isconnected():           # tant que l'ESP32 n'est pas connecté au WiFi
            pass                                # ne rien faire
    print("Adresse IP :", wlan.ifconfig()[0])      # affichage de l'adresse IP de l'ESP32
    print("Masque réseau : ", wlan.ifconfig()[1])  # affichage du masque réseau de l'ESP32
    print("Gateway :", wlan.ifconfig()[2])         # affichage de la gateway de l'ESP32
    print("Serveur DNS :", wlan.ifconfig()[3])     # affichage du serveur DNS de l'ESP32
    return wlan.ifconfig()[0]                      # renvoi de l'adresse IP de l'ESP32

AdresseIP = connexion_wifi(wifissid, pwd)              # appel de la fonction connexion_wifi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # création d'un objet socket pour écouter les requêtes HTTP

s.bind((AdresseIP, 80))  # association de l'objet socket à l'adresse IP de l'ESP32 et au port 80 (port par défaut pour les requêtes HTTP)
s.listen(1)              # mise en écoute de l'objet socket (1 client maximum)


def web_page():

    html = """
    <!DOCTYPE html>
    <html>
       <head>
               <title>ESP</title>
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <style>
                       html
                       {
                               font-family: Helvetica;
                               margin: 0px auto;
                               text-align: center;
                       }
                       h1
                       {
                               color: #0F3376;
                               padding: 2vh;
                       }
                       p
                       {
                               font-size: 24px;
                       }
                       .button
                       {
                               background-color: #4CAF50;   /* Vert */
                               border: none;
                               border-radius: 6px;   /* Angle arrondi */
                               color: white;
                               padding: 15px 32px;
                               text-align: center;
                               text-decoration: none;
                               font-size: 30px;
                       }
                       .button2
                       {
                               background-color: #f44336; /* Rouge */
                       }
               </style>
       </head>
       <body>
               <h1>ESP Serveur Web</h1>
               <p><a href="/?led=on"><button class="button">ON</button></a></p>
               <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
       </body>
    </html>
    """
    return html

socketServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServeur.bind(('', 8080))
socketServeur.listen(5)

#boucle principale gérant la communication avec le client et effectue des actions en fonction des requêtes HTTP
while True:
    try:
        
        #libération de memoire si supérieure a 102ko
        if gc.mem_free() < 102000:
            gc.collect()
         
        # attente d'une connexion client (se connecter à la page web) et acceptation avec affichage de IP du client
        print("Attente connexion d'un client")
        connexionClient, adresse = socketServeur.accept()
        connexionClient.settimeout(4.0)
        print("Connecté avec le client", adresse)

        # attente de la requête du client , sera stockée dans une variable requête
        print("Attente requete du client")
        requete = connexionClient.recv(1024)     #requête du client
        requete = str(requete)
        print("Requete du client = ", requete)
        connexionClient.settimeout(None)
        
        #analyse de la requête, recherche de led=on ou led=off
        if "GET /?led=on" in requete:
            print("LED ON")
            led_1.value(1)
        if "GET /?led=off" in requete:
            print("LED OFF")
            led_1.value(0)
         
        #envoi d'une réponse HTTP au client avec le code HTML de la fonction web_page()
        print("Envoi reponse du serveur : code HTML a afficher")
        connexionClient.send('HTTP/1.1 200 OK\n')
        connexionClient.send('Content-Type: text/html\n')
        connexionClient.send("Connection: close\n\n")
        reponse = web_page()
        connexionClient.sendall(reponse)
        connexionClient.close()  
        print("Connexion avec le client fermee")
        
    #s'il y a eu une erreur lors du Try, on ferme la connexion avec le client en affichant l'erreur 
    except:
        connexionClient.close()  
        print("Connexion avec le client fermee, le programme a declenché une erreur")
