#!/usr/bin/python

import telegram
import subprocess
import time
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from subprocess import check_output, STDOUT, CalledProcessError

token = open("token.txt", "r").read().strip()
print ("\n\n\n{}\n\n".format(token))
updater = Updater(token=token)
bot = telegram.Bot(token=token)

GOD = 185198389
sudoerfile = open("sudoers.txt", "r")
logger = open("bot.log", "w")

#sudoers = [int(x.strip()) for x in sudoerfile.read().split("\n")[:-1]]

sudoers = []
for x in sudoerfile.read().split("\n"):
	x = x.strip()
	if x == "":
		continue
	if x.startswith("#"):
		continue
	sudoers.append(int(x))

#### TODO : se l'output di un comando e' null messaggio relativo al problema "null"

def logup(usr,txt,info):

	#now = time.strftime("%Y-%m-%d %H:%M")
	print (f"{usr} :: {txt} {info}")
	logger.write(f" {usr} :: {txt} {info} \n")
	logger.flush()

def execute(words):
	try:
		answer = check_output([words], shell=True, stderr=STDOUT)
		a = answer.decode()
		logup("tried ", words, "DONE")
		return a
	except CalledProcessError as exc :
		e = exc.output.decode()
		logup("tried ", words, "ERROR")
		return e
	else :
		assert 0

def start(bot, update):

	logup(update.message.chat_id, "triggered", "START")
	bot.sendMessage(chat_id=update.message.chat_id, text="You just pressed start. This is indeed pretty useless")
	bot.sendMessage(chat_id=update.message.chat_id, text="Anyways, I can give you a list of commands if you type /help.")

def createap(bot, update):

	logup(update.message.chat_id, "triggered", "CREATEAP")
	bot.sendMessage(chat_id=update.message.chat_id, text="Ok, I see you're pimped for this command,\n i am too indeed...")
	bot.sendMessage(chat_id=update.message.chat_id, text="But still this is not ready yet...")

def help(bot, update):

	logup(update.message.chat_id, "triggered", "HELP")
	bot.sendMessage(chat_id=update.message.chat_id, text="This bot is not the most featurefull bot ever.")
	bot.sendMessage(chat_id=update.message.chat_id, text="you can use the command /cmd [command] to execute something in the server")
	bot.sendMessage(chat_id=update.message.chat_id, text="you can use the command /createap to close this bot.")
	bot.sendMessage(chat_id=update.message.chat_id, text="you can try the command /kill to close this bot.")
	bot.sendMessage(chat_id=update.message.chat_id, text="you can try the command /logs to watch the log table.")

def cmd(bot, update):

	if update.message.chat_id in sudoers:
		msg = update.message.text
		sudochat = update.message.chat_id
		if msg == "/cmd" :
			bot.sendMessage(chat_id=update.message.chat_id, text="command is empty, use : /cmd [command] to make it work.")
			logup(sudochat, "triggered", "CMD")
		else :
			words = msg.strip("/cmd")
			if words.find("reboot") > -1 or words.find("shutdown") > -1 or words.find("suspend") > -1 or words.find("hybernate") > -1 :
				bot.sendMessage(chat_id=sudochat, text="Asking for permission \n Please wait... ")
				if update.message.chat_id == GOD :
					bot.sendMessage(chat_id=GOD, text=" You're IN.")
					for sudoer in sudoers:
						bot.sendMessage(chat_id=sudoer, text= " Sorry to tell you, but the bot got terminated from chat. \n Also, the computer has been knocked down")
					logup(sudochat," is ", "executing ::")
					answer = execute(words)
				else :
					bot.sendMessage(chat_id=sudochat, text=" Permission denied, sorry.")
			else :
				answer = execute(words)
				bot.sendMessage(chat_id=sudochat, text="executing command : {}".format(words))
				if answer == "":
					bot.sendMessage(chat_id=sudochat, text="output is apparently empty. No errors occourred.")
				else :
					bot.sendMessage(chat_id=sudochat, text="output:\n{}".format(answer))
	else :
		bot.sendMessage(chat_id=update.message.chat_id, text="Come on, I'm not this retarded.\n you're not going to send a command to my pc, sorry. ...")

def logs(bot, update):

	if update.message.chat_id in sudoers:
		msg = update.message.text
		thischat = update.message.chat_id
		logup(thischat, "triggered", "LOGGER")
		bot.sendMessage(chat_id=thischat, text="The logfile currently is :")
		answer = execute("cat bot.log")
		if answer == "" :
			bot.sendMessage(chat_id=thischat, text="... Apparently empty" )
		else :
			bot.sendMessage(chat_id=thischat, text=answer)
	else :
		bot.sendMessage(chat_id=update.message.chat_id, text="Sorry to tell you, but you're not allowed to execute this command, you can ask @xornand for the permission tho.")

def echo(bot, update):

	answer = ("I can't do any '{}', sorry".format(update.message.text))
	bot.sendMessage(chat_id=update.message.chat_id, text=answer)
	bot.sendMessage(chat_id=update.message.chat_id, text="You could try the /help function.")

#### loopcode down here #####

for sudoer in sudoers:
	bot.sendMessage(chat_id=sudoer, text=" HELLO FUCKIN' WORLD! The Nor Xand bot just started. type /help to get a list of possible commands. Have fun fucker.")
	if os.geteuid() == 0:
		bot.sendMessage(chat_id=sudoer, text=" and please BE AWARE YOU ARE NOW IN CONSTANT SUDO")

updater.start_polling()
logup("polling started","sending welcome message", "(SYS)")

dispatcher = updater.dispatcher

### handlers ###

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

cmd_handler = CommandHandler('cmd', cmd)
dispatcher.add_handler(cmd_handler)

createap_handler = CommandHandler('createap', createap)
dispatcher.add_handler(createap_handler)

logs_handler = CommandHandler('logs', logs)
dispatcher.add_handler(logs_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.idle()
logger.close()
print("ctrl-c was pressed, stopping")

for sudoer in sudoers:
	bot.sendMessage(chat_id=sudoer, text="Sorry to tell you, but the bot got terminated from server.")

#update.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")
