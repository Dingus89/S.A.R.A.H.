import sys
import serial

# Adjust port to your ESP32-S2 Mini
PORT = "/dev/ttyUSB0"
BAUD = 115200

if len(sys.argv) < 2:
    print("Usage: esp_send.py <code>")
    sys.exit(1)

command = sys.argv[1]

try:
    with serial.Serial(PORT, BAUD, timeout=2) as ser:
        ser.write((command + "\n").encode())
        print(f"Sent: {command}")
except Exception as e:
    print(f"Serial error: {e}")
