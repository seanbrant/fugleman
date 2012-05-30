import sys

from fugleman.runner import CommandRunner


def main():
    runner = CommandRunner(sys.argv)
    runner.execute()
