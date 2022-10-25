from telegram.ext import CommandHandler
import random
import torch
from lib.text_utils import extract_parameter, split_prompts
from lib.image_utils import image_to_bytes

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
    num_inference_steps = min(num_inference_steps, 300)
    num_inference_steps = max(num_inference_steps, 1)
    as_file, text = extract_parameter(text, "as_file", bool, False)
    prompt, negative_prompt = split_prompts(text)

    image = context.bot_data["pipe"].text2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        generator=generator,
        guidance_scale=guidance_scale).images[0]
    if as_file:
        update.message.reply_document(image_to_bytes(image), "image.png")
    else:
        update.message.reply_photo(image_to_bytes(image), "{} (Seed: {})".format(text, seed))


def add_handler(dp):
    dp.add_handler(CommandHandler("txt2img", txt2img_command))