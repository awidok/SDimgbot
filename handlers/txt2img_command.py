from telegram.ext import CommandHandler
import random
import torch
from io import BytesIO
from lib.text_utils import extract_parameter


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


    seed, text = extract_parameter(text, "seed", int, random.randint(1, 10000))
    generator = torch.cuda.manual_seed_all(seed)

    guidance_scale, text = extract_parameter(text, "scale", float, 7.5)
    num_inference_steps, text = extract_parameter(text, "steps", int, 100)
    as_file, text = extract_parameter(text, "as_file", bool, False)


    image = context.bot_data["pipe"].text2img(
        prompt=text,
        num_inference_steps=num_inference_steps,
        generator=generator,
        guidance_scale=guidance_scale).images[0]
    if as_file:
        update.message.reply_document(image_to_bytes(image), "{} (Seed: {})".format(text, seed))
    else:
        update.message.reply_photo(image_to_bytes(image), "{} (Seed: {})".format(text, seed))


def add_handler(dp):
    dp.add_handler(CommandHandler("txt2img", txt2img_command))