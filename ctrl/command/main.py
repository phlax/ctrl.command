import sys

from zope import component

from ctrl.core.exceptions import CtrlError
from ctrl.core.interfaces import ICommandRunner, IApp


def main():
    app = component.getUtility(IApp).initialize(
        modules=['ctrl.config', 'ctrl.command'])
    try:
        sys.exit(component.getAdapter(app, ICommandRunner).run(*sys.argv[1:]))
    except CtrlError as e:
        sys.stdout.write(
            "\n".join(reversed([str(x) for x in e] + ["\nCtrl Error!\n"])))
        sys.exit(1)


if __name__ == '__main__':
    main()
