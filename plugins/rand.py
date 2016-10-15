from __future__ import unicode_literals
import random
from slackbot.bot import listen_to, respond_to

from .util import tokenize


@listen_to('^!rand(?:om)? (.+)')
@respond_to('^!rand(?:om)? (.+)')
def random_select(message, args):
    args = tokenize(args)
    message.reply(random.choice(args))
