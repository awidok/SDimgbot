from telegram.ext import CommandHandler


# Start message
def start_command(update, context):
    update.message.reply_text('Greetings, here you can generate stickers with Stable Diffusion')


def add_handler(dp):
    dp.add_handler(CommandHandler("start", start_command))