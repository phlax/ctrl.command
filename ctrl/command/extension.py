
from zope import component

from ctrl.core.interfaces import ICommandRunner, ICtrlApp, IShell

from .runner import CtrlRunner
from .shell import Shell


component.provideAdapter(CtrlRunner, (ICtrlApp, ), ICommandRunner)


class CtrlCommandExtension(object):

    @property
    def requires(self):
        return ['config']

    async def register(self, app):
        shell = Shell()
        component.provideUtility(
            shell,
            provides=IShell)
