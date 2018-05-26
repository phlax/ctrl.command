import asyncio

from zope import component, interface

import colorama

from ctrl.command.base import Commandable
from ctrl.core.interfaces import (
    ICommandRunner, IApp, ISubcommand)


colorama.init()


@interface.implementer(ICommandRunner)
class CtrlRunner(Commandable):

    @property
    def subcommands(self):
        subcommands = component.getAdapters((self, ), ISubcommand)
        return dict(subcommands)

    def run(self, *args):
        loop = asyncio.get_event_loop()
        component.getUtility(IApp).run(
            super(CtrlRunner, self).run(loop, self.parse(*args)))
