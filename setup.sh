#!/bin/bash

echo "Installing SARAH dependencies..."

sudo apt update
sudo apt install -y python3 python3-pip git make arecord aplay unzip \
  adb ir-ctl libssl-dev libavahi-compat-libdnssd-dev \
  pkg-config libdbus-1-dev cmake ninja-build

echo "Setting up Python environment..."
pip install -r requirements.txt

echo "Downloading models..."
mkdir -p models
if [ ! -d "whisper.cpp" ]; then
  git clone https://github.com/ggerganov/whisper.cpp
  cd whisper.cpp && make && ./models/download-ggml-model.sh tiny.en && cd ..
fi

echo "Creating configs..."
mkdir -p configs
touch configs/platform_priority.json
touch configs/show_platform_cache.json
echo "{}" > configs/platform_priority.json
echo "{}" > configs/show_platform_cache.json

echo "Done. Run './scripts/start_service.sh' or 'sudo systemctl start sarah' after setup."
