#!/usr/bin/env python3
"""
Simple test script to verify ControlNet setup locally
"""

import os
import sys
from PIL import Image
import numpy as np

def test_setup():
    """Test if all dependencies are available"""
    print("🧪 Testing ControlNet Setup...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        
        import diffusers
        print(f"✅ Diffusers: {diffusers.__version__}")
        
        import controlnet_aux
        print("✅ ControlNet Aux")
        
        from controlnet_aux import CannyDetector, DepthDetector, NormalDetector
        print("✅ ControlNet Detectors")
        
        # Test CUDA availability
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name()}")
        else:
            print("⚠️  CUDA not available (will use CPU)")
        
        print("\n🎉 All dependencies are ready!")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    # Create a simple room-like image
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Add some room elements
    img[100:400, 100:400] = [200, 200, 200]  # Floor
    img[0:100, :] = [150, 150, 200]  # Wall
    img[:, 0:100] = [150, 150, 200]  # Wall
    
    # Add a rectangle for furniture
    img[300:350, 200:300] = [100, 100, 100]
    
    return Image.fromarray(img)

if __name__ == "__main__":
    if test_setup():
        print("\n📸 Creating test image...")
        test_img = create_test_image()
        test_img.save("test_room.png")
        print("✅ Test image saved as 'test_room.png'")
        print("\n🚀 Ready for deployment!")
    else:
        print("\n❌ Setup incomplete. Please install missing dependencies.")
        sys.exit(1)