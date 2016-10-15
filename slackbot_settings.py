import os

API_TOKEN = os.environ['SLACK_TOKEN']
PLUGINS = [
    'plugins.echo',
    'plugins.rand',
    'plugins.repl',
]
