#!/bin/bash
# Start script for KickCheck

echo "Starting KickCheck API server..."
cd "$(dirname "$0")/api"
python3 app.py

