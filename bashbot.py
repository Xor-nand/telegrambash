# this is the beta for the new complete telegram bashbot
import telegram
import subprocess
import time
import os

from pathlib import Path
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from subprocess import check_output, STDOUT, CalledProcessError

token = open("configs/token.txt", "r").read().strip()
admin = open("configs/admin_chat_id.txt", "r").read().strip()
print (" admin : {}".format(admin))

sudoerfile = open("configs/superusers_chat_id.txt", "r")
forbiddencmds = open("configs/forbiddencmds.txt", "r")
logger = open("bot.log", "w")

sudoers = []
for y in sudoerfile.read().split("\n"):
	y = y.strip()
	if y == "":
		continue
	if y.startswith("#"):
		continue
	sudoers.append(int(y))

forbid = []
for x in forbiddencmds.read().split("\n"):
	x = x.strip()
	if x == "":
		continue
	if x.startswith("#"):
		continue
	forbid.append(x)

updater = Updater(token=token)
bot = telegram.Bot(token=token)

print ("\n\n !SYS :: Starting bot with token:\n {}\n\n".format(token))

def logup(usr,txt,info):

	#now = time.strftime("%Y-%m-%d %H:%M")
	print (f" {usr} :: {txt} {info}")
	logger.write(f" {usr} :: {txt} {info} \n")
	logger.flush()

logup("!SYS", "started", "logger")

def execute(words):
	try:
		answer = check_output([words], shell=True, stderr=STDOUT)
		a = answer.decode()
		logup( "\t> {}".format(words), "executed", "DONE")
		return a
	except CalledProcessError as exc :
		e = exc.output.decode()
		logup( "\t> {}".format(words), "executed", "ERROR")
		return e
	else :
		assert 0

def cmd(bot, update):
	logup(update.message.chat_id, "triggered", "cmd")
	msg = update.message.text
	if update.message.chat_id in sudoers:
		logup(update.message.chat_id, "triggered", "cmd as sudoer:")
		sudochat = update.message.chat_id
		if msg == "/cmd" :
			logup(" > ", " empty command","")
			bot.sendMessage(chat_id=sudochat, text="command is empty, use : /cmd [command] to make it work.")
		else :
			words = msg.strip("/cmd")
			passcode = True
			for forbidden in forbid:
				if words.find(forbidden) > -1 :
					logup(sudochat, " > illegal word : ", words)
					passcode = False
				else :
					pass
			if passcode == False:
				bot.sendMessage(chat_id=sudochat, text="Asking for permission \n Please wait... ")
				if "{}".format(update.message.chat_id) == admin :
					bot.sendMessage(chat_id=admin, text="You're IN.")
					bot.sendMessage(chat_id=admin, text="Command executed.")
					for sudoer in sudoers:
						bot.sendMessage(chat_id=sudoer, text= " Sorry to tell you, but the bot got terminated from chat. \n Also, the computer has been knocked down")
					logup(sudochat,"executing", "shutdown")
					answer = execute(words)
				else :
					bot.sendMessage(chat_id=sudochat, text=" Permission denied, sorry bro.")
			else :
				#bot.sendMessage(chat_id=sudochat, text="executing command : `{}`".format(words), parse_mode=telegram.ParseMode.MARKDOWN)
				update.message.reply_text("Executing command: `{}`".format(words), parse_mode=telegram.ParseMode.MARKDOWN)
				answer = execute(words)
				if answer == "":
					bot.sendMessage(chat_id=sudochat, text="output is apparently empty. No errors occourred tho.")
				else :
					bot.sendMessage(chat_id=sudochat, text="output:\n\n`{}`".format(answer), parse_mode=telegram.ParseMode.MARKDOWN)
	else :
		bot.sendMessage(chat_id=update.message.chat_id, text="Come on, I'm not this retarded.\n you're not going to send a command to my pc, sorry. ...")

def start(bot, update):

	logup(update.message.chat_id, "triggered", "START")
	bot.sendMessage(chat_id=update.message.chat_id, text="You just pressed start. This is indeed pretty useless")
	bot.sendMessage(chat_id=update.message.chat_id, text="Anyways, I can give you a list of commands if you type /help.")

def createap(bot, update):

	if os.geteuid() == 0:
		logup(update.message.chat_id, "triggered", "CREATEAP")
		bot.sendMessage(chat_id=update.message.chat_id, text="Ok, I see you're pimped for this command,\n i am too indeed...")
		bot.sendMessage(chat_id=update.message.chat_id, text="But still this is not ready yet...")
	else:
		logup(update.message.chat_id, "triggered", "CREATEAP-nosudo")
		bot.sendMessage(chat_id=update.message.chat_id, text="You are not in sudo, sorry but I can't execute this command")

def help(bot, update):

	logup(update.message.chat_id, "triggered", "HELP")
	bot.sendMessage(chat_id=update.message.chat_id, text="This bot is not the most featurefull bot ever.", parse_mode=telegram.ParseMode.MARKDOWN)
	bot.sendMessage(chat_id=update.message.chat_id, text="you can use the command /cmd [command] to execute something in the server", parse_mode=telegram.ParseMode.MARKDOWN)
	bot.sendMessage(chat_id=update.message.chat_id, text="you can use the command /createap to close this bot.", parse_mode=telegram.ParseMode.MARKDOWN)
	bot.sendMessage(chat_id=update.message.chat_id, text="you can try the command /kill to close this bot.", parse_mode=telegram.ParseMode.MARKDOWN)
	bot.sendMessage(chat_id=update.message.chat_id, text="you can try the command /logs to watch the log table.", parse_mode=telegram.ParseMode.MARKDOWN)

def logs(bot, update):

	if update.message.chat_id in sudoers:
		msg = update.message.text
		thischat = update.message.chat_id
		logup(thischat, "triggered", "LOGGER :")
		bot.sendMessage(chat_id=thischat, text="The logfile currently is :")
		answer = execute("cat bot.log")
		if answer == "" :
			bot.sendMessage(chat_id=thischat, text="... Apparently empty" )
		else :
			bot.sendMessage(chat_id=thischat, text="`{}`".format(answer), parse_mode=telegram.ParseMode.MARKDOWN )
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
logup("polling started","sending welcome message", "")

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
print("ctrl-c was pressed, stopping\n\n")

for sudoer in sudoers:
	bot.sendMessage(chat_id=sudoer, text="Sorry to tell you, but the bot got terminated from server.")

#update.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")
