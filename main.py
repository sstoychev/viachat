#!/usr/bin/env python3
import sys
import traceback
import importlib
from configparser import ConfigParser
from server.server import Server
# import this explicitly so we can use its .subclasses
from server.commands.basecommand import BaseCommand
# Maybe import * is not the best way
# TODO(Stoycho) review import *
from server.commands import *


CONFIG_FILE = 'config.ini'

config = ConfigParser()
config.read(CONFIG_FILE)

# import db_engine dynamically to be controlled only from the config
db_engine = config.get('server', 'db_engine')
DbEngine = getattr(importlib.import_module(f'server.dbadapters.{db_engine.lower()}'), db_engine)

db = DbEngine(config)

available_commands = ['Available commands:']

# Get all available commands dynamically so when we add a new one not to modify
# message handling.
prefix = config.get('server', 'command_prefix')
cmds = {}
for cls in BaseCommand.subclasses:
    # create an instance of the command and add it to the dictionary
    cmd = cls(db, prefix)
    whole_command = f"{prefix}{cmd.action}"
    available_commands.append(f'{whole_command} - {cmd.describe}')
    cmds[cmd.action] = cmd

available_commands.append('')
available_commands = "\n".join(available_commands)

chat_server = Server(
    config=dict(config.items('server')),
    cmds=cmds,
    available_commands=available_commands
)
try:
    chat_server.run()
except KeyboardInterrupt:
    pass
except Exception as e:
    traceback.print_exc()
finally:
    chat_server.RUN_FOREVER = False
    sys.exit()
