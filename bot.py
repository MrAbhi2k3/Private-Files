import json
import os
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN1 = "BOT_TOKEN_1"
TOKEN2 = "BOT_TOKEN_2"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Please send me a file to download.")

def get_file_content(bot_token, file_id):
    """Retrieves the file content for a given file ID using the bot API."""
    file_url = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(bot_token, file_id)
    response = requests.get(file_url)
    file_data = json.loads(response.content.decode('utf-8'))
    file_path = file_data['result']['file_path']
    file_url = 'https://api.telegram.org/file/bot{}/{}'.format(bot_token, file_path)
    file_content = requests.get(file_url).content
    return file_content

def download(update, context):
    """Downloads the file with the specified file ID."""
    file_id = update.message.document.file_id
    file_content = get_file_content(TOKEN1, file_id)
    context.bot.send_document(chat_id=update.effective_chat.id, document=file_content)
    # Transfer file ID to second bot
    transferred_file = context.bot.send_document(chat_id='CHAT_ID_OF_SECOND_BOT', document=file_id)
    transferred_file_id = transferred_file.document.file_id
    # Download file from second bot
    transferred_file_content = get_file_content(TOKEN2, transferred_file_id)
    # Save file to local disk or process it as required
    # For example, you could save the file as follows:
    with open('downloaded_file.jpg', 'wb') as f:
        f.write(transferred_file_content)

def main():
    updater = Updater(TOKEN1, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, download))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
