#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* ssid = "MIWIFI_dUAY";
const char* password = "fPYc4YYs";

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


WebServer server(80);
bool isSpeaking = false;

int gpLb = 12; // Left 1
int gpLf = 13; // Left 2
int gpRb = 14; // Right 1
int gpRf = 27; // Right 2

#define TRIGGER_PIN  33  // Pin de Trigger del HC-SR04
#define ECHO_PIN     32   // Pin de Echo del HC-SR04

void setup() {
  Serial.begin(115200);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); //  OLED
  display.clearDisplay();

  pinMode(gpLf, OUTPUT);
  pinMode(gpLb, OUTPUT);
  pinMode(gpRf, OUTPUT);
  pinMode(gpRb, OUTPUT);

  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  server.on("/distance", HTTP_GET, []() {
    int distance = measureDistance(); // Obtiene la distancia
    if (distance >= 0) { // Verifica si la distancia es válida
      server.send(200, "text/plain", String(distance) + " cm");
    } else {
      server.send(200, "text/plain", "Out of range");
    }
  });
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

  server.on("/speak", HTTP_GET, []() {
    isSpeaking = true;
    server.send(200, "text/plain", "Speaking");
  });


  server.on("/silence", HTTP_GET, []() {
    isSpeaking = false;
    server.send(200, "text/plain", "Silence");
  });

  server.begin();
}

void speakingMouth() {
  display.clearDisplay();
  float amplitude = random(10, 30);
  float frequencyVariation = random(10, 30) / 10.0;
  static float xOffset = 0;
  xOffset += PI / 4;

  for (int x = 0; x < SCREEN_WIDTH; x++) {
    int y = (int)(amplitude * sin((1.0 + frequencyVariation) * ((float)x * 2 * PI / SCREEN_WIDTH) + xOffset)) + (SCREEN_HEIGHT / 2);
    for (int extraY = -2; extraY <= 2; extraY++) {
      display.drawPixel(x, y + extraY, SSD1306_WHITE);
    }
  }
  display.display();
  delay(5);
}

void closedMouth() {
  display.clearDisplay();
  float amplitude = random(1, 3); // Amplitud baja

  for (int x = 0; x < SCREEN_WIDTH; x++) {
    int y = (int)(amplitude * sin(1.0 * ((float)x * 2 * PI / SCREEN_WIDTH)) + (SCREEN_HEIGHT / 2));
    display.drawPixel(x, y, SSD1306_WHITE);
  }
  display.display();
  delay(5);
}

void loop() {
  server.handleClient();
  server.handleClient();
  display.clearDisplay(); // Limpia el display

  if (isSpeaking) {
    speakingMouth();
  } else {
    closedMouth();
  }

  display.display(); // Muestra los cambios en el display
  delay(5); // Retraso breve para reducir parpadeo
}


int measureDistance() {
  // Asegura que el pin de trigger esté en LOW.
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  // Emite un pulso ultrasónico.
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  // Mide la duración del eco
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Calcula la distancia
  int distance = duration * 0.034 / 2;

  // Verifica si la distancia está fuera de rango
  if (distance > 0 && distance <= 400) { // Asume que el rango máximo es 400 cm
    return distance;
  } else {
    return -1; // Retorna -1 si está fuera de rango
  }
}

void stop() {
  digitalWrite(gpLf, LOW);
  digitalWrite(gpLb, LOW);
  digitalWrite(gpRf, LOW);
  digitalWrite(gpRb, LOW);
}