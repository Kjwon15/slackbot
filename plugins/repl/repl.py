from __future__ import unicode_literals
import subprocess

from slackbot.bot import listen_to, respond_to
import io
import os
import re
from tempfile import NamedTemporaryFile

TOKENIZE_PATTERN = re.compile(r'```(.+?)```|"(.+?)"|(\S+)', re.U | re.S)


def tokenize(message):
    return list(filter(
        lambda x: x and x.strip(),
        TOKENIZE_PATTERN.split(message)))


def run_code(interpreter, code, stdin=None):
    script_file = NamedTemporaryFile(delete=True)
    with io.open(script_file.name, 'w', encoding='utf-8') as fp:
        fp.write('#!/usr/bin/env {}\n'.format(interpreter))
        fp.write(code)

    os.chmod(script_file.name, 0o755)
    script_file.file.close()

    process = subprocess.Popen(
        [script_file.name],
        env={
            'LC_ALL': 'en_US.UTF-8',
        },
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if stdin is not None:
        process.stdin.write(stdin.encode('utf-8'))
        process.stdin.close()

    process.wait(timeout=3)
    stdout = process.stdout.read()
    stderr = process.stdout.read()

    return stderr or stdout


@listen_to(r'^!python (?P<code>.*)', re.S)
@respond_to(r'^!python (?P<code>.*)', re.S)
def python(message, arg):
    '''Run python code.'''
    tokens = tokenize(arg)
    code = tokens[0]
    stdin = tokens[1] if len(tokens) > 1 else None
    print(tokens)
    result = run_code('python', code, stdin=stdin)
    message.reply(result)


@listen_to(r'^!repl (?P<interpreter>.+?) (?P<code>.*)', re.S)
@respond_to(r'^!repl (?P<interpreter>.+?) (?P<code>.*)', re.S)
def repl(message, interpreter, arg):
    '''Run code with specific interpreter.'''
    tokens = tokenize(arg)
    code = tokens[0]
    stdin = tokens[1] if len(tokens) > 1 else None
    result = run_code(interpreter, code, stdin=stdin)
    message.reply(result)
