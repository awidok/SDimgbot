from telegram.ext import CommandHandler


def del_command(update, context):
    replied_message = update.message.reply_to_message
    context.bot.delete_message(replied_message.chat_id, replied_message.message_id)


def add_handler(dp):
    dp.add_handler(CommandHandler("del", del_command))