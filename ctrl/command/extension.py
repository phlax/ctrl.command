
from zope import component

from ctrl.core.extension import CtrlExtension
from ctrl.core.interfaces import (
    IApp, ICommandRunner, ICtrlExtension, IShell)

from .runner import CtrlRunner
from .shell import Shell


class CtrlCommandExtension(CtrlExtension):

    @property
    def requires(self):
        return ['config']

    def register_adapters(self):
        component.provideAdapter(
            CtrlRunner,
            (IApp, ),
            ICommandRunner)

    async def register_utilities(self):
        shell = Shell()
        component.provideUtility(
            shell,
            provides=IShell)


# register the extension
component.provideUtility(
    CtrlCommandExtension(),
    ICtrlExtension,
    'command')
