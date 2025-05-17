#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

// Replace with your Wi-Fi credentials
const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

#define RELAY_LIGHT 2
#define RELAY_LOW   3
#define RELAY_MED   4
#define RELAY_HIGH  5
#define RELAY_OFF   6

void activateRelay(int pin) {
  digitalWrite(pin, HIGH);
  delay(500);
  digitalWrite(pin, LOW);
}

void handleCommand(String cmd) {
  if (cmd == "L") activateRelay(RELAY_LIGHT);
  else if (cmd == "1") activateRelay(RELAY_LOW);
  else if (cmd == "2") activateRelay(RELAY_MED);
  else if (cmd == "3") activateRelay(RELAY_HIGH);
  else if (cmd == "0") activateRelay(RELAY_OFF);
}

void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client,
               AwsEventType type, void * arg, uint8_t *data, size_t len) {
  if (type == WS_EVT_DATA) {
    String msg = "";
    for (size_t i = 0; i < len; i++) {
      msg += (char) data[i];
    }
    handleCommand(msg);
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(RELAY_LIGHT, OUTPUT);
  pinMode(RELAY_LOW, OUTPUT);
  pinMode(RELAY_MED, OUTPUT);
  pinMode(RELAY_HIGH, OUTPUT);
  pinMode(RELAY_OFF, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);
  server.begin();

  Serial.println("WebSocket server started.");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Nothing needed here
}
