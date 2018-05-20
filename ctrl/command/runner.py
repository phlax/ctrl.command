import asyncio

from zope import component, interface

import colorama

from ctrl.command.base import Commandable
from ctrl.core.interfaces import ICtrlApp

from .interfaces import ICommandRunner, ISubcommand


colorama.init()


@interface.implementer(ICommandRunner)
class CtrlRunner(Commandable):

    @property
    def subcommands(self):
        subcommands = component.getAdapters((self, ), ISubcommand)
        return dict(subcommands)

    def handle(self, *args):
        app = component.getUtility(ICtrlApp)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            app.setup(
                ['ctrl.command',
                 'ctrl.zmq',
                 'ctrl.config',
                 'ctrl.compose']))
        try:
            loop.run_until_complete(self.run(self.parse(*args)))
        finally:
            loop.close()
