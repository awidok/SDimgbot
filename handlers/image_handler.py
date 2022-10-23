from telegram.ext import MessageHandler, Filters
from io import BytesIO
from PIL import Image

def img2img(update, context, file_):
    bytes_io = BytesIO()

    file_.download(out=bytes_io)

    image = Image.open(bytes_io)
    image.thumbnail((512, 512))

    if image.size[0] < 512:
        new_image = Image.new('RGBA', (512, image.size[1]), color=(255,255,255,0))
        new_image.paste(image, (0, 0, image.size[0], image.size[1]))
        image = new_image

    stream = BytesIO()
    image.save(stream, format='WEBP')
    out_stream = BytesIO(stream.getvalue())
    bot.send_document(update.message.chat.id, out_stream, timeout=30)

    stream = BytesIO()
    image.save(stream, format='PNG')
    out_stream = BytesIO(stream.getvalue())
    bot.send_document(update.message.chat.id, out_stream, timeout=30)

def img2img_command(update, context):
    text = update.message.text
    if ' ' in text:
        text = text[text.find(' ') + 1:]
    if text == "/txt2img":
        return
    update.message.reply("pong")


# reply to an image
def image_document_handler(update, context):
    img2img(update, context, update.message.document.get_file())
    
# reply to an image
def photo_handler(update, context):
    img2img(update, context, context.bot.getFile(update.message.photo[-1].file_id))

def add_handler(dp):
    dp.add_handler(MessageHandler(Filters.document.category("image"), image_document_handler))
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))
