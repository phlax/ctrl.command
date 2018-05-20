
from zope.interface import Interface


class ICommandable(Interface):

    def handle(*args):
        pass


class ICommand(Interface):

    def handle(*args):
        pass


class ISubcommand(Interface):

    def handle(*args):
        pass


class ICommandRunner(Interface):

    def handle(*args):
        pass


class IShell(Interface):
    pass
