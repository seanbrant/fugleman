import sys

from fugleman.cli.runner import CommandRunner


def run():
    runner = CommandRunner(sys.argv)
    runner.run()
