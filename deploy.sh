#!/bin/bash

echo "🚀 ControlNet-v1-1-nightly Deployment Script"
echo "============================================="

# Check if cog is installed
if ! command -v cog &> /dev/null; then
    echo "📥 Installing Cog..."
    curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)
    chmod +x /usr/local/bin/cog
    echo "✅ Cog installed successfully!"
else
    echo "✅ Cog is already installed"
fi

# Check if logged in to Replicate
echo "🔐 Checking Replicate login..."
if ! cog whoami &> /dev/null; then
    echo "⚠️  Not logged in to Replicate"
    echo "Please run: cog login"
    echo "Then run this script again"
    exit 1
fi

echo "✅ Logged in to Replicate as: $(cog whoami)"

# Build and push
echo "🔨 Building model..."
cog build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    echo "📤 Pushing to Replicate..."
    cog push
    
    if [ $? -eq 0 ]; then
        echo "🎉 Deployment successful!"
        echo "Your model is now available on Replicate!"
        echo "Update your .env file with the new model URL"
    else
        echo "❌ Push failed"
        exit 1
    fi
else
    echo "❌ Build failed"
    exit 1
fi