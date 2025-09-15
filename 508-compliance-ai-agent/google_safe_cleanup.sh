#!/bin/bash
echo "🧹 Google-login-safe cleanup starting..."

# Step 1: Clear apt cache
echo "Clearing apt cache..."
sudo apt-get clean
sudo apt-get autoremove --purge -y

# Step 2: Clear pip cache
echo "Clearing pip cache..."
pip cache purge

# Step 3: Clear system logs (safe)
echo "Clearing /var/log..."
sudo rm -rf /var/log/*

# Step 4: Clear /tmp but keep browser temp data safe
echo "Clearing /tmp (excluding browser temp)..."
find /tmp -mindepth 1 -maxdepth 1 ! -name '.org.chromium.Chromium*' ! -name '.com.google.Chrome*' -exec sudo rm -rf {} +

# Step 5: Check free space
echo "📊 Free space after cleanup:"
df -h /

# Step 6: Ask before installing PyTorch
read -p "Do you want to install CPU-only PyTorch now? (y/n): " choice
if [[ "$choice" == "y" ]]; then
    echo "Installing CPU-only PyTorch (smaller size)..."
    pip install torch==2.8.0+cpu --index-url https://download.pytorch.org/whl/cpu --no-cache-dir
else
    echo "Skipping PyTorch installation."
fi

echo "✅ Cleanup complete. Your Google login is SAFE."
