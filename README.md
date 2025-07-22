# ControlNet-v1-1-nightly for Replicate

This repository contains a Replicate deployment of ControlNet-v1-1-nightly for image-to-image generation with multiple control types.

## Features

- **Canny Edge Detection**: Perfect for room transformation and structure preservation
- **Depth Control**: Excellent for 3D room understanding and complex layouts
- **Normal Control**: Great for surface details and material understanding
- **Multiple Control Types**: Choose the best control for your use case

## Models Included

- `control_v11p_sd15_canny.pth` - Edge detection control
- `control_v11f1p_sd15_depth.pth` - Depth map control  
- `control_v11p_sd15_normal.pth` - Surface normal control

## Usage

### Parameters

- `image`: Input image (PIL Image or file path)
- `prompt`: Text description of desired output
- `control_type`: Type of control ("canny", "depth", "normal")
- `negative_prompt`: What to avoid in generation
- `num_inference_steps`: Number of generation steps (default: 20)
- `guidance_scale`: How closely to follow prompt (default: 7.5)
- `low_threshold`: Canny edge detection low threshold (default: 100)
- `high_threshold`: Canny edge detection high threshold (default: 200)
- `seed`: Random seed for reproducibility

### Example Usage

```python
import replicate

# Generate with Canny control
output = replicate.run(
    "yourusername/controlnet-v1-1-nightly",
    input={
        "image": "path/to/room.jpg",
        "prompt": "a modern living room with minimalist furniture",
        "control_type": "canny",
        "negative_prompt": "blurry, low quality",
        "num_inference_steps": 20,
        "guidance_scale": 7.5
    }
)
```

## Deployment

1. Install Cog: `curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m) && chmod +x /usr/local/bin/cog`
2. Login to Replicate: `cog login`
3. Deploy: `cog push`

## Cost Optimization

- Use 15-20 inference steps for good quality/cost balance
- Canny control is fastest and cheapest
- Depth control provides best 3D understanding
- Normal control is best for surface details

## Credits

Based on [ControlNet-v1-1-nightly](https://github.com/lllyasviel/ControlNet-v1-1-nightly) by lllyasviel.