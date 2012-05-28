from optparse import OptionParser, make_option

from fugleman import get_version


class BaseCommand(object):
    help = ''
    args = ''
    option_list = ()

    def __init__(self, prog, name, argv, stdout):
        self.prog = prog
        self.name = name
        self.argv = argv
        self.stdout = stdout
        self.parser = OptionParser(
            prog=self.prog,
            usage=self.usage(),
            version=get_version(),
            option_list=self.option_list,
        )

    def usage(self):
        """
        Returns the usage message for this command.

        """
        usage = "%s %s [options] %s" % (self.prog, self.name, self.args)
        if self.help:
            return '%s\n\n%s' % (usage, self.help)
        else:
            return usage

    def print_help(self):
        """
        Prints the commands help text to stdout.

        """
        self.parser.print_help(self.stdout)

    def run(self):
        """
        Parses the arguments and passes them on to the handler.

        """
        options, args = self.parser.parse_args(self.argv)
        self.handle(*args, **options.__dict__)

    def handle(self, *args, **kwargs):
        """
        Subclasses should overwrite this to preform commands actions.

        """
        raise NotImplementedError


class ServeCommand(BaseCommand):
    help = "Starts a development server for serving your Fugleman project."
    args = '[optional port number, or ipaddr:port] [directory]'

    def handle(self, addrport=None, directory=None, *args, **kwargs):
        pass
