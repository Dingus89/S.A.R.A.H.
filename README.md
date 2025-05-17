# S.A.R.A.H.
Home automation 

Full Install Instructions (Ubuntu 22.04+)

1. Clone SARAH Repo
git clone https://github.com/your-username/sarah.git
cd sarah

2. Install System Dependencies
sudo apt update
sudo apt install -y python3 python3-pip git curl unzip make gcc g++ arecord aplay adb ir-ctl libssl-dev libavahi-compat-libdnssd-dev pkg-config libdbus-1-dev cmake ninja-build
        
3. Install Python Dependencies
pip install -r requirements.txt

4. Setup Whisper for STT
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp && make
./models/download-ggml-model.sh tiny.en
cd ..

5. Install Matter CLI (Optional Fallback)
git clone https://github.com/project-chip/connectedhomeip.git
cd connectedhomeip
source scripts/activate.sh
gn gen out/debug
ninja -C out/debug
chip-tool is now at connectedhomeip/out/debug/chip-tool

You can:
•	Add it to your $PATH, or
•	Update lights_fan.py to call it by full path
 
Start SARAH
chmod +x scripts/install_deps.sh
chmod +x scripts/start_service.sh

# In a tmux or screen session:
./scripts/start_service.sh

 
Final requirements.txt

Here’s the complete content:
websockets
requests==2.31.0
python-dotenv==1.0.1
flask==3.0.2
paho-mqtt==1.6.1
