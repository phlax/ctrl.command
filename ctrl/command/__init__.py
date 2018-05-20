
from zope import component

from ctrl.core.interfaces import ICtrlExtension
from .extension import CtrlCommandExtension


# register the extension
component.provideUtility(
    CtrlCommandExtension(),
    ICtrlExtension,
    'command')
