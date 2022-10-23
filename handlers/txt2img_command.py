from telegram.ext import CommandHandler
import random
import torch
from io import BytesIO


def image_to_bytes(image):
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'png')
    bio.seek(0)
    return bio


def txt2img_command(update, context):
    text = update.message.text
    if ' ' in text:
        text = text[text.find(' ') + 1:]
    if text == "/txt2img":
        return

        
    seed = random.randint(1, 10000)
    generator = torch.cuda.manual_seed_all(seed)
    image = context.bot_data["pipe"].text2img(
        prompt=text,
        num_inference_steps=100,
        generator=generator).images[0]

    update.message.reply_photo(image_to_bytes(image), "{} (Seed: {})".format(text, seed))


def add_handler(dp):
    dp.add_handler(CommandHandler("txt2img", txt2img_command))