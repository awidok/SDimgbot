from telegram.ext import Updater
import logging
import os
from importlib import import_module


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Log an error
def process_error(update, context):
    logger.warning('Update "%s" caused error "%s"' % (update, context.error))


def add_handlers(dp):
    for module in os.listdir(os.path.join(os.path.dirname(__file__), "handlers")):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        module_name = "handlers." + module[:-3]
        module = import_module(module_name)
        getattr(module, 'add_handler')(dp)

    dp.add_error_handler(process_error)

def add_common_data(dp):
    for module in os.listdir(os.path.join(os.path.dirname(__file__), "common_data")):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        module_name = "common_data." + module[:-3]
        module = import_module(module_name)
        getattr(module, 'add_data')(dp)


def main():
    TOKEN = os.environ['TELEGRAM_TOKEN']
    updater = Updater(TOKEN)
    add_handlers(updater.dispatcher)
    add_common_data(updater.dispatcher)

    if "USE_WEBHOOK" in os.environ:
        PORT = int(os.environ.get('PORT', '5000'))
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN
        )
        url = os.environ['URL']

        updater.bot.set_webhook(url + TOKEN)

        updater.idle()
    else:
        updater.start_polling()


if __name__ == '__main__':
    main()
