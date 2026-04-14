#!/bin/bash
echo "🔄 Pulling latest changes from GitHub..."

cd ~/Documents/AFD2615

git pull

if [ $? -eq 0 ]; then
    echo "✅ Successfully updated from GitHub!"
else
    echo "❌ Failed to pull changes. Check your internet or git status."
fi
