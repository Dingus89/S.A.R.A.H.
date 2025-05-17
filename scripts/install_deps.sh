#!/bin/bash
# Install dependencies
sudo apt update
sudo apt install -y \
  python3 python3-pip \
  git curl unzip \
  make gcc g++ \
  arecord aplay               # Audio capture/playback
  adb                         # Android TV control
  ir-ctl                      # Infrared (LIRC) CLI
  libssl-dev                  # Required for chip-tool build
  libavahi-compat-libdnssd-dev \
  pkg-config libdbus-1-dev \
  cmake ninja-build           # For Matter CLI (chip-tool)pip install -r requirements.txt

# Setup whisper.cpp
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp && make
./models/download-ggml-model.sh tiny.en
