#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "xxxxxx";
const char* password = "xxxxx";

WebServer server(80);

int gpLb = 12; // Left 1
int gpLf = 13; // Left 2
int gpRb = 14; // Right 1
int gpRf = 27; // Right 2

void setup() {
  Serial.begin(115200);
  
  pinMode(gpLf, OUTPUT);
  pinMode(gpLb, OUTPUT);
  pinMode(gpRf, OUTPUT);
  pinMode(gpRb, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  server.on("/right", HTTP_GET, []() {
    if (server.hasArg("time")) {
        int time = server.arg("time").toFloat() * 1000;
        digitalWrite(gpLf, HIGH);
        digitalWrite(gpLb, LOW);
        digitalWrite(gpRf, HIGH);
        digitalWrite(gpRb, LOW);
        delay(time);
        stop();
        server.send(200, "text/plain", "Going Forward for " + server.arg("time") + " seconds");
    } else {
        server.send(400, "text/plain", "Time parameter is missing");
    }
  });

  server.on("/left", HTTP_GET, []() {
    if (server.hasArg("time")) {
        int time = server.arg("time").toFloat() * 1000;
        digitalWrite(gpLf, LOW);
        digitalWrite(gpLb, HIGH);
        digitalWrite(gpRf, LOW);
        digitalWrite(gpRb, HIGH);
        delay(time);
        stop();
        server.send(200, "text/plain", "Going Backward for " + server.arg("time") + " seconds");
    } else {
        server.send(400, "text/plain", "Time parameter is missing");
    }
  });

  server.on("/back", HTTP_GET, []() {
    if (server.hasArg("time")) {
        int time = server.arg("time").toFloat() * 1000;
        digitalWrite(gpLf, HIGH);
        digitalWrite(gpLb, LOW);
        digitalWrite(gpRf, LOW);
        digitalWrite(gpRb, HIGH);
        delay(time);
        stop();
        server.send(200, "text/plain", "Turning Left for " + server.arg("time") + " seconds");
    } else {
        server.send(400, "text/plain", "Time parameter is missing");
    }
  });

  server.on("/go", HTTP_GET, []() {
    if (server.hasArg("time")) {
        int time = server.arg("time").toFloat() * 1000;
        digitalWrite(gpLf, LOW);
        digitalWrite(gpLb, HIGH);
        digitalWrite(gpRf, HIGH);
        digitalWrite(gpRb, LOW);
        delay(time);
        stop();
        server.send(200, "text/plain", "Turning Right for " + server.arg("time") + " seconds");
    } else {
        server.send(400, "text/plain", "Time parameter is missing");
    }
  });

  server.on("/stop", HTTP_GET, []() {
    stop();
    server.send(200, "text/plain", "Stopping");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}

void stop() {
  digitalWrite(gpLf, LOW);
  digitalWrite(gpLb, LOW);
  digitalWrite(gpRf, LOW);
  digitalWrite(gpRb, LOW);
}
