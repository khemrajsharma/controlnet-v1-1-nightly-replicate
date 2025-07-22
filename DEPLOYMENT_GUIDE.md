# 🚀 ControlNet-v1-1-nightly Deployment Guide

## Quick Start (3 Steps)

### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `controlnet-v1-1-nightly-replicate`
3. Make it public
4. Don't initialize with README (we already have one)

### Step 2: Upload Files
1. Upload all files from this directory to your GitHub repository:
   - `cog.yaml`
   - `predict.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `deploy.sh`
   - `test_local.py`

### Step 3: Deploy to Replicate
1. Clone your repository locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/controlnet-v1-1-nightly-replicate.git
   cd controlnet-v1-1-nightly-replicate
   ```

2. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

3. Follow the prompts to log in to Replicate

## Manual Deployment (Alternative)

If the script doesn't work, do it manually:

### Install Cog
```bash
curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)
chmod +x /usr/local/bin/cog
```

### Login to Replicate
```bash
cog login
```

### Deploy
```bash
cog build
cog push
```

## After Deployment

1. **Get your model URL**: After successful deployment, you'll get a URL like:
   ```
   https://replicate.com/YOUR_USERNAME/controlnet-v1-1-nightly
   ```

2. **Update your RoomCraft AI app**: Change your `.env` file:
   ```bash
   REPLICATE_MODEL=YOUR_USERNAME/controlnet-v1-1-nightly
   ```

3. **Test the model**: Use the test script:
   ```bash
   python test_local.py
   ```

## Model Features

Your deployed model will support:

- **Canny Control**: Best for room transformation
- **Depth Control**: Best for 3D room understanding  
- **Normal Control**: Best for surface details

## Cost Savings

- **Public model**: $0.01-0.02 per image
- **Your own model**: $0.005-0.01 per image (50% cheaper!)

## Troubleshooting

### Build Fails
- Check your internet connection
- Make sure you have enough disk space
- Try running `cog build --debug` for more info

### Push Fails
- Make sure you're logged in: `cog whoami`
- Check your Replicate account has credits
- Try `cog push --debug` for more info

### Model Doesn't Work
- Check the model URL is correct
- Verify all files were uploaded to GitHub
- Check the Replicate logs for errors

## Support

If you encounter issues:
1. Check the [Cog documentation](https://github.com/replicate/cog)
2. Check the [Replicate documentation](https://replicate.com/docs)
3. Look at the [ControlNet-v1-1-nightly repository](https://github.com/lllyasviel/ControlNet-v1-1-nightly)

## Credits

This deployment is based on [ControlNet-v1-1-nightly](https://github.com/lllyasviel/ControlNet-v1-1-nightly) by lllyasviel.