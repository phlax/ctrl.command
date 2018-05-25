import sys

from zope import component

from ctrl.core.exceptions import CtrlError
from ctrl.core.interfaces import ICommandRunner, ICtrlApp


def main():
    app = component.getUtility(ICtrlApp)
    runner = component.getAdapter(app, ICommandRunner)
    try:
        sys.exit(runner.handle(*sys.argv[1:]))
    except CtrlError as e:
        sys.stdout.write(
            "\n".join(reversed([str(x) for x in e] + ["\nCtrl Error!\n"])))
        sys.exit(1)


if __name__ == '__main__':
    main()
