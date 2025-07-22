import os
import cv2
import torch
import numpy as np
from PIL import Image
import tempfile
from typing import Optional
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from controlnet_aux import CannyDetector, DepthDetector, NormalDetector
import sys
import subprocess
import cog

class Predictor:
    def setup(self):
        """Download and setup ControlNet models"""
        print("Setting up ControlNet models...")
        
        # Create models directory
        os.makedirs("models", exist_ok=True)
        
        # Download ControlNet models from ControlNet-v1-1-nightly
        models_to_download = {
            "canny": {
                "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth",
                "config": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.yaml"
            },
            "depth": {
                "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth",
                "config": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.yaml"
            },
            "normal": {
                "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normal.pth",
                "config": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normal.yaml"
            }
        }
        
        # Download models
        for model_type, urls in models_to_download.items():
            model_path = f"models/control_v11p_sd15_{model_type}.pth"
            config_path = f"models/control_v11p_sd15_{model_type}.yaml"
            
            if not os.path.exists(model_path):
                print(f"Downloading {model_type} model...")
                subprocess.run(["wget", "-O", model_path, urls["url"]], check=True)
            
            if not os.path.exists(config_path):
                print(f"Downloading {model_type} config...")
                subprocess.run(["wget", "-O", config_path, urls["config"]], check=True)
        
        # Load base Stable Diffusion model
        print("Loading Stable Diffusion model...")
        self.base_model = "runwayml/stable-diffusion-v1-5"
        
        # Initialize detectors
        self.canny_detector = CannyDetector()
        self.depth_detector = DepthDetector.from_pretrained("lllyasviel/Annotators")
        self.normal_detector = NormalDetector.from_pretrained("lllyasviel/Annotators")
        
        # Load ControlNet models
        self.controlnet_models = {}
        for model_type in ["canny", "depth", "normal"]:
            model_path = f"models/control_v11p_sd15_{model_type}.pth"
            config_path = f"models/control_v11p_sd15_{model_type}.yaml"
            
            if os.path.exists(model_path) and os.path.exists(config_path):
                print(f"Loading {model_type} ControlNet...")
                self.controlnet_models[model_type] = ControlNetModel.from_pretrained(
                    model_path,
                    config_file=config_path,
                    torch_dtype=torch.float16
                )
        
        # Create pipelines for each model type
        self.pipelines = {}
        for model_type, controlnet in self.controlnet_models.items():
            print(f"Creating pipeline for {model_type}...")
            pipeline = StableDiffusionControlNetPipeline.from_pretrained(
                self.base_model,
                controlnet=controlnet,
                torch_dtype=torch.float16
            )
            
            if torch.cuda.is_available():
                pipeline = pipeline.to("cuda")
            
            pipeline.enable_xformers_memory_efficient_attention()
            self.pipelines[model_type] = pipeline
        
        print("Setup complete!")
    
    def predict(
        self,
        image: cog.File,
        prompt: str,
        control_type: str = "canny",
        negative_prompt: str = "",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        low_threshold: int = 100,
        high_threshold: int = 200,
        seed: Optional[int] = None
    ) -> cog.File:
        """
        Generate image using ControlNet
        
        Args:
            image: Input image (PIL Image or path)
            prompt: Text prompt for generation
            control_type: Type of control (canny, depth, normal)
            negative_prompt: Negative prompt
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale
            low_threshold: Low threshold for Canny
            high_threshold: High threshold for Canny
            seed: Random seed
        """
        
        # Validate control type
        if control_type not in self.pipelines:
            raise ValueError(f"Control type '{control_type}' not available. Use: {list(self.pipelines.keys())}")
        
        # Load image
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        else:
            # Handle cog.File type
            image = Image.open(image.path).convert("RGB")
        
        # Convert to numpy for processing
        image_np = np.array(image)
        
        # Apply control based on type
        if control_type == "canny":
            control_image = self.canny_detector(image_np, low_threshold, high_threshold)
        elif control_type == "depth":
            control_image = self.depth_detector(image_np)
        elif control_type == "normal":
            control_image = self.normal_detector(image_np)
        else:
            raise ValueError(f"Unknown control type: {control_type}")
        
        # Convert back to PIL
        control_image = Image.fromarray(control_image)
        
        # Set seed for reproducibility
        if seed is not None:
            torch.manual_seed(seed)
            generator = torch.Generator().manual_seed(seed)
        else:
            generator = None
        
        # Generate image
        print(f"Generating with {control_type} control...")
        result = self.pipelines[control_type](
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=control_image,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        ).images[0]
        
        # Save result
        output_path = tempfile.mktemp(suffix=".png")
        result.save(output_path)
        
        return cog.File(output_path)