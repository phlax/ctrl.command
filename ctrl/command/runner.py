import asyncio

from zope import component, interface

import colorama

from ctrl.command.base import Commandable
from ctrl.config.interfaces import ICtrlConfig
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
        loop.run_until_complete(app.setup(['ctrl.config']))
        config = component.getUtility(ICtrlConfig)
        apps = (
            config.config.get('controller', 'apps').split('\n')
            if config.config.has_section('controller')
            else [])
        loop.run_until_complete(
            app.setup(['ctrl.command'] + apps))
        try:
            print(loop.run_until_complete(self.run(loop, self.parse(*args))))
        finally:
            loop.close()
