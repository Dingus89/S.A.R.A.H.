#!/bin/bash
cd "$(dirname "$0")/.."
python3 -m app.main



Instructions: 
# Install dependencies
chmod +x scripts/install_deps.sh
./scripts/install_deps.sh

# Launch (in a tmux session)
chmod +x scripts/start_service.sh
./scripts/start_service.sh
