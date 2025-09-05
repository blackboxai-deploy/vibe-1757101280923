#!/bin/bash

# Forensic Capture Tool Setup Script
# This script automates the installation and setup process

echo "=========================================="
echo "Forensic Capture Tool Setup"
echo "=========================================="

# Check for Python
echo "[INFO] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required but not installed."
    exit 1
fi

python3 --version
echo "[✓] Python 3 found"

# Install pip if not available
echo "[INFO] Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "[INFO] Installing pip..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-pip
    else
        echo "[ERROR] Package manager not supported. Please install pip manually."
        exit 1
    fi
fi

echo "[✓] pip found"

# Install Python dependencies
echo "[INFO] Installing Python dependencies..."
pip3 install -r requirements.txt
echo "[✓] Python dependencies installed"

# Install Playwright browser
echo "[INFO] Installing Playwright browser..."
python3 -m playwright install chromium
echo "[✓] Playwright browser installed"

# Install system dependencies based on OS
echo "[INFO] Installing system dependencies..."
if command -v dnf &> /dev/null; then
    # Amazon Linux/RHEL/CentOS
    sudo dnf install -y nss nspr dbus-libs atk at-spi2-atk cups-libs libdrm libxcb libxkbcommon at-spi2-core libX11 libXcomposite libXdamage libXext libXfixes libXrandr mesa-libgbm pango cairo alsa-lib
elif command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get install -y libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcb1 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
else
    echo "[WARNING] Unknown package manager. You may need to install system dependencies manually."
    echo "See FORENSIC_CAPTURE_README.md for details."
fi

echo "[✓] System dependencies installed"

# Create output directory if it doesn't exist
echo "[INFO] Creating output directory..."
mkdir -p output
echo "[✓] Output directory ready"

# Test the installation
echo "[INFO] Testing forensic capture tool..."
echo "Running quick test with minimal settings..."

python3 capture.py --labels TEST --out ./output --min-bytes 1000 --verbose

if [ $? -eq 0 ]; then
    echo "[✓] Installation test completed successfully"
    echo ""
    echo "=========================================="
    echo "Setup Complete!"
    echo "=========================================="
    echo ""
    echo "You can now use the forensic capture tool:"
    echo ""
    echo "Basic usage:"
    echo "  python3 capture.py --labels RHO-TECH PIPETECH --out ./output --min-bytes 1000000"
    echo ""
    echo "With verbose output:"
    echo "  python3 capture.py --labels TARGET1 TARGET2 --out ./investigation --min-bytes 500000 --verbose"
    echo ""
    echo "See FORENSIC_CAPTURE_README.md for complete documentation."
    echo ""
else
    echo "[ERROR] Installation test failed. Please check the error messages above."
    exit 1
fi