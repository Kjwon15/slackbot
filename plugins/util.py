import re


TOKENIZE_PATTERN = re.compile(r'```(.+?)```|"(.+?)"|(\S+)', re.U | re.S)


def tokenize(message):
    return list(filter(
        lambda x: x and x.strip(),
        TOKENIZE_PATTERN.split(message)))
