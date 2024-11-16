import torch
from diffusers import StableDiffusionUpscalePipeline
from PIL import Image
import os

class UpscalerService:
    def __init__(self, device='cuda'):
        self.model_id = "stabilityai/stable-diffusion-x4-upscaler"
        self.device = device
        
        print(f"Initializing upscaler service on device: {device}")
        if device == 'cuda':
            # Load model with mixed precision for better GPU memory usage
            self.pipeline = StableDiffusionUpscalePipeline.from_pretrained(
                self.model_id,
                revision="fp16",
                torch_dtype=torch.float16
            )
        else:
            self.pipeline = StableDiffusionUpscalePipeline.from_pretrained(
                self.model_id,
                revision="main",
                torch_dtype=torch.float32
            )
        
        self.pipeline = self.pipeline.to(device)
        
        if device == 'cuda':
            # Enable memory efficient attention
            self.pipeline.enable_attention_slicing()
            # Enable sequential CPU offload if needed
            if torch.cuda.get_device_properties(0).total_memory < 8 * 1024 * 1024 * 1024:  # less than 8GB
                self.pipeline.enable_sequential_cpu_offload()

    def upscale_image(self, input_path, prompt=""):
        try:
            # Load and process image
            image = Image.open(input_path).convert("RGB")
            
            # Ensure image is not too large for initial processing
            max_size = 512
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Generate upscaled image
            upscaled_image = self.pipeline(
                prompt=prompt if prompt else "high quality, detailed image",
                image=image,
                num_inference_steps=20,
                guidance_scale=7.5
            ).images[0]

            # Save result
            output_path = os.path.join('results', f'upscaled_{os.path.basename(input_path)}')
            upscaled_image.save(output_path)
            
            return output_path
        except Exception as e:
            print(f"Error in upscale_image: {str(e)}")
            raise
