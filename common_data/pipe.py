from diffusers import DiffusionPipeline
import os
import torch


def init_pipe():
    HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN", None)
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", custom_pipeline="stable_diffusion_mega", torch_dtype=torch.float16, revision="fp16", use_auth_token=HUGGINGFACE_TOKEN)
    pipe.to("cuda")
    pipe.enable_attention_slicing()

    def dummy_checker(images, **kwargs): return images, False
    pipe.safety_checker = dummy_checker

    return pipe


def add_data(dp):
    dp.bot_data["pipe"] = init_pipe()