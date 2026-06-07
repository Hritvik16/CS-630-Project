#!/bin/bash

DIR=$(pwd)

echo "🎬 Launching Dual Distributed Visualization..."

# Launch Warehouse in a new terminal window
osascript -e "tell application \"Terminal\" to do script \"cd '$DIR' && python3 visual_demo.py --sim warehouse\""

# Launch Forest Fire in a new terminal window
osascript -e "tell application \"Terminal\" to do script \"cd '$DIR' && python3 visual_demo.py --sim forest_fire\""

echo "✅ Demos launched in separate windows! Arrange them side-by-side for your screen recording."