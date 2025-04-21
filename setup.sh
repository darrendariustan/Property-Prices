#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt

# Create directories for Streamlit cache
mkdir -p ~/.streamlit/

# Configure Streamlit
echo "[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = false
" > ~/.streamlit/config.toml 