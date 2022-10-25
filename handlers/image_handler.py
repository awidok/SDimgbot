from telegram.ext import MessageHandler, Filters
from io import BytesIO
from PIL import Image
import numpy as np
from lib.text_utils import extract_parameter, split_prompts
from lib.image_utils import image_to_bytes
import random
import torch

def get_img(file):
    bytes_io = BytesIO()
    file.download(out=bytes_io)
    image = Image.open(bytes_io)
    return image


def img2img(update, context, file):
    text = update.message.caption
    if not text.startswith("/img2img"):
        return
    if ' ' in text:
        text = text[text.find(' ') + 1:]
    if text == "/img2img":
        text = ""

    seed, text = extract_parameter(text, "seed", int, random.randint(1, 10000))
    generator = torch.cuda.manual_seed_all(seed)

    strength, text = extract_parameter(text, "strength", float, 0.8)
    as_file, text = extract_parameter(text, "as_file", bool, False)
    steps, text = extract_parameter(text, "steps", int, 50)
    steps = min(steps, 300)
    steps = max(steps, 1)

    prompt, negative_prompt = split_prompts(text)

    image = context.bot_data["pipe"].img2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        init_image=get_img(file),
        num_inference_steps=steps,
        generator=generator,
        strength=strength).images[0]
    if as_file:
        update.message.reply_document(image_to_bytes(image), "image.png")
    else:
        update.message.reply_photo(image_to_bytes(image), "{} (Seed: {})".format(text, seed))


# reply to an image
def image_document_handler(update, context):
    img2img(update, context, update.message.document.get_file())
    
# reply to an image
def photo_handler(update, context):
    img2img(update, context, context.bot.getFile(update.message.photo[-1].file_id))

def add_handler(dp):
    dp.add_handler(MessageHandler(Filters.document.category("image"), image_document_handler))
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))
