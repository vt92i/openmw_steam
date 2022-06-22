#!/usr/bin/env python

import os
import sys
from ctypes import CDLL
from subprocess import call

# Steam path
steam_path = os.path.join(os.getenv("HOME"), ".local/share/Steam/")
if not os.path.exists(steam_path):
    print("Steam path not found.")
    sys.exit(1)

# Find gameoverlayrenderer.so
game_overlay_path = os.path.join(steam_path, "ubuntu12_64/gameoverlayrenderer.so")
if not os.path.exists(game_overlay_path):
    print("gameoverlayrenderer.so not found")
    sys.exit(1)

# Find libsteam_api.so
libsteam_api_path = None
for root, dirs, files in os.walk(steam_path):
    if libsteam_api_path is None:
        for file in files:
            if file.endswith("libsteam_api.so"):
                libsteam_api_path = os.path.join(root, file)

if libsteam_api_path == None:
    print("libsteam_api.so not found")
    sys.exit(1)

# Morrowind
os.environ["SteamAppId"] = "22320"

# Enable Steam Overlay
os.environ["LD_PRELOAD"] = game_overlay_path

# Load libsteam_api.so
steam_api = CDLL(libsteam_api_path)

# Check if Steam is running
if steam_api.SteamAPI_IsSteamRunning() != 0:
    # Initialize Steam API
    if steam_api.SteamAPI_Init() != 0:
        # Launch Morrowind
        call(["openmw"])
    else:
        print("Failed to initialize Steam API")
else:
    print("Steam is not running")
