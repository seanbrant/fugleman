import sys

from fugleman.management.runner import CommandRunner


def run():
    runner = CommandRunner(sys.argv)
    runner.run()
