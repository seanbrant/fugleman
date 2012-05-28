import os
import sys
from optparse import OptionParser

from fugleman import get_version
from fugleman.cli import commands


class CommandRunner(object):
    subcommands = {
        'serve': commands.ServeCommand
    }

    def __init__(self, argv, stdout=sys.stdout):
        self.argv = argv
        self.stdout = stdout
        self.prog = os.path.basename(self.argv[0])
        self.parser = OptionParser(
           usage='%s subcommand [options] [args]' % self.prog,
           version=get_version(),
        )

    def print_help(self):
        """
        Prints the programs help text to stdout.

        """
        self.parser.print_help(self.stdout)

        text = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog,
            "",
            "Available subcommands:",
        ]

        for subcommand_name in self.subcommands.keys():
            text.append('  %s' % subcommand_name)

        text.append('')

        self.stdout.write('\n'.join(text))

    def print_version(self):
        """
        Prints the programs version number to stdout.

        """
        self.stdout.write('%s\n' % self.parser.get_version())

    def print_command_unkown_error(self, name):
        """
        Prints a error about the command being unkown to stdout.

        """
        text = [
            "Unknown command: '%s'" % name,
            "Type '%s help' for usage." % self.prog,
            "",
        ]
        self.stdout.write('\n'.join(text))

    def fetch_subcommand(self, name):
        """
        Returns the subcommand if its found otherwise it prints
        an error message.

        """
        try:
            subcommand_class = self.subcommands[name]
        except KeyError:
            self.print_command_unkown_error(name)
            sys.exit(1)
        return subcommand_class(self.prog, name, self.argv[2:], self.stdout)

    def run(self):
        """
        This figures out the subcommand being run and then runs the it.

        """

        options, args = self.parser.parse_args(self.argv)

        try:
            subcommand_name = self.argv[1]
        except IndexError:
            subcommand_name = 'help'

        if subcommand_name == 'help':
            if len(args) <= 2:
                self.print_help()
            else:
                self.fetch_subcommand(self.argv[2]).print_help()
        elif subcommand_name == 'version':
            self.print_version()
        else:
            self.fetch_subcommand(subcommand_name).run()
