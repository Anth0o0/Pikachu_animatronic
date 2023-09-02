// (No copyright)  SLG Robotics V09/20

#include <WiFi.h>
  const char* ssid = "Antho_oneplus9"; 
  const char* mot_de_passe = "aqzsedrf"; 
String entete; 
String etat_LEDV = "eteint"; 
String etat_LEDR = "eteint";
const int LEDV= 32;
const int LEDR = 33;
WiFiServer server(80); 

void setup() {
Serial.begin(115200);
Serial.println("Tentative de rejoindre le réseau...");
WiFi.begin(ssid,mot_de_passe);
while (WiFi.status()!=WL_CONNECTED){delay(500);
Serial.print(".");
}

Serial.println("connexion au réseau réussie...!");
Serial.println(WiFi.localIP());
server.begin();
pinMode(LEDV,OUTPUT);pinMode(LEDR,OUTPUT);
}

void loop() {
  
WiFiClient client = server.available(); 
  if (client) { Serial.println("nouveau client");
    String ligne = ""; 
   
   while (client.connected())
   {Serial.println("client connecté !");
     if (client.available())
     {char c = client.read(); 
      Serial.write(c);entete += c;
        if (c == '\n') 
        {if (ligne.length() == 0) {
client.println("HTTP/1.1 200 OK"); 
client.println("Content-type:text/html");
client.println("Connection: close");
client.println();

if (entete.indexOf("GET /2/allume") >= 0) {
Serial.println("LED verte allumée");etat_LEDV = "allume"; 
digitalWrite(LEDV, HIGH);
} else if (entete.indexOf("GET /2/eteint") >= 0) {
Serial.println("LED verte éteinte");etat_LEDV = "eteint";
digitalWrite(LEDV, LOW);
} else if (entete.indexOf("GET /1/allume") >= 0) {
Serial.println("LED rouge allumée");etat_LEDR = "allume";
digitalWrite(LEDR, HIGH);
} else if (entete.indexOf("GET /1/eteint") >= 0) {
Serial.println("LED rouge éteinte");etat_LEDR = "eteint";
digitalWrite(LEDR, LOW);
            }
            
client.println("<!DOCTYPE html><html>");
client.print("<head><meta name=\"viewport\" content=\"width=device-width, ");
client.println("initial-scale=1\">");

client.println("<link rel=\"icon\" href=\"data:,\">");

client.print("<style>html { font-family: Helvetica; display: inline-block; ");
client.println("margin: 0px auto; text-align: center;}");

client.print(".button { background-color: #299886; border: none; ");
client.println("color: white; padding: 16px 40px;");
client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");

client.print(".button1 { background-color: #d35845; border: none; color: white; ");
client.println("padding: 16px 40px;");

client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
client.println(".button3 {background-color: #f2b2a8;}");
client.println(".button2 {background-color: #82d9cb;}</style></head>");
            
client.println("<body><h1>Server web ESP32 </h1>");
client.println("<p>LED verte - Etat " + etat_LEDV + "</p>");
if (etat_LEDV=="eteint") {
client.println("<p><a href=\"/2/allume\"><button class=\"button\">Allumer</button></a></p>");
} else {
client.print("<p><a href=\"/2/eteint\"><button class=\"button button2\">Eteindre");
client.println("</button></a></p>");} 
client.println("<p>LED rouge - Etat " + etat_LEDR + "</p>");

if (etat_LEDR=="eteint") {
client.print("<p><a href=\"/1/allume\"><button class=\"button button1\">Allumer");
client.println("</button></a></p>");

} else {
client.print("<p><a href=\"/1/eteint\"><button class=\"button button3\">Eteindre");
client.println("</button></a></p>");

}client.println("</body></html>");
            

client.println();break;
} else { ligne = "";
}} else if (c != '\r') {  
 ligne += c;}}}
entete = "";
client.stop(); 
Serial.println("Client déconnecté !");
Serial.println("");
}}
