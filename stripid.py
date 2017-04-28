#usr/bin/python
import telegram
import subprocess
import time

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from subprocess import check_output, STDOUT, CalledProcessError

updater = Updater(token='286104748:AAFsANChmNRXLFM0l5b06f6BKOyagaM2Fq0')
bot = telegram.Bot(token='286104748:AAFsANChmNRXLFM0l5b06f6BKOyagaM2Fq0')

def echo(bot, update):

	bot.sendMessage(chat_id=update.message.chat_id, text="ma va?")
	bot.sendMessage(chat_id=update.message.chat_id, text="grazie")
	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.chat_id)
	print (update.message.chat_id)

updater.start_polling()

dispatcher = updater.dispatcher
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(echo_handler)
