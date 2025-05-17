#!/bin/bash

echo "[+] Installing ALSA and audio tools..."
sudo apt update
sudo apt install -y alsa-utils pulseaudio pavucontrol sox

echo "[+] Adding user '$USER' to the audio group..."
sudo usermod -aG audio "$USER"
newgrp audio

echo "[+] Detecting available audio capture devices..."
DEVICE_LIST=$(arecord -l | grep "^card")
echo "$DEVICE_LIST"

# Try to auto-detect USB mic
USB_MIC_LINE=$(echo "$DEVICE_LIST" | grep -i 'usb\|webcam\|mic' | head -n 1)

if [ -z "$USB_MIC_LINE" ]; then
  echo "[!] No USB mic explicitly detected. Defaulting to card 1, device 0"
  CARD="1"
  DEVICE="0"
else
  echo "[+] USB mic found: $USB_MIC_LINE"
  CARD=$(echo "$USB_MIC_LINE" | sed -n 's/^card \([0-9]\+\):.*/\1/p')
  DEVICE=$(echo "$USB_MIC_LINE" | sed -n 's/.*device \([0-9]\+\):.*/\1/p')
fi

echo "[+] Setting sample rate to 44100 and default device to hw:$CARD,$DEVICE..."

sudo tee /etc/asound.conf > /dev/null <<EOL
pcm.!default {
    type plug
    slave {
        pcm "hw:$CARD,$DEVICE"
        rate 44100
    }
}
ctl.!default {
    type hw
    card $CARD
}
EOL

echo "[+] Restarting ALSA and testing the mic..."
sleep 2
arecord -f cd -d 5 test.wav
aplay test.wav

echo "[+] Done! If the audio is clean, you're ready."
echo "    If it sounds off, run 'alsamixer' to tweak levels (use F6 to pick mic)."
