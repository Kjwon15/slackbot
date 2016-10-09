from __future__ import unicode_literals
from slackbot.bot import respond_to

@respond_to('!echo (.*)')
def echo(message, str):
    message.reply(str)
