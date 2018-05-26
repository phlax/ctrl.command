import argparse
import sys

from termcolor import colored


FAIL = 1
WARN = 2


class Command(object):
    prog_name = ''
    username = 'cloud'
    appsdir = '/apps'

    def __init__(self, config):
        self.config = config
        self._parser = None

    @property
    def prog(self):
        parent = super(Command, self)
        prog = getattr(parent, 'prog', '')
        return ' '.join([prog, self.prog_name])

    @property
    def parser(self):
        self._parser = self._parser or argparse.ArgumentParser(prog=self.prog)
        return self._parser

    @property
    def stdout(self):
        return sys.stdout

    def add_args(self, parser):
        return parser

    def parse(self, *args):
        self.add_args(self.parser)
        return self.parser.parse_args(args)

    async def handle(self, *args):
        return await self.run(self.parse(*args))

    def get_message(self, message, status=None):
        if status is FAIL:
            return colored("%s ☠" % message, 'red')
        if status is WARN:
            return colored("%s ⚠" % message, 'yellow')
        return colored("%s ✓" % message, 'green')

    def respond(self, action, message=None, status=None, terminator=None):
        terminator = "\n" if terminator is None else terminator
        format_str = '{} {:>%s}%s' % ((80 - len(action), terminator))
        self.stdout.write(
            format_str.format(
                action,
                self.get_message(message, status)))


class Commandable(Command):
    subcommands = None

    def __init__(self, config):
        super(Commandable, self).__init__(config)

    def add_args(self, parser):
        parser.add_argument('subcommand', choices=self.subcommands.keys())
        return parser

    def command_args(self, options, config):
        return config

    def parse(self, *args):
        self.add_args(self.parser)
        kwargs, args = self.parser.parse_known_args(args)
        kwargs.args = args
        return kwargs

    def get_commands(self, options):
        if self.subcommands:
            return {
                name: command
                for name, command
                in self.subcommands.items()}

    async def run(self, loop, options):
        self.commands = self.get_commands(options) or {}
        if self.commands.get(options.subcommand):
            return await self.commands[
                options.subcommand].handle(*options.args, loop=loop)
