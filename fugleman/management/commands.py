import sys
from optparse import OptionParser
from wsgiref.simple_server import make_server

from fugleman import get_version
from fugleman.wsgi import WSGIHandler


class CommandError(Exception):
    """
    Indicates that a problem occurred while running a command.

    If this exception is raised during a command run the runner
    will catch it and print a error to stdout.

    """
    pass


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

    DEFAULT_ADDR = '127.0.0.1'
    DEFAULT_PORT = '8989'

    def handle(self, addrport=None, directory=None, *args, **kwargs):
        if addrport is None:
            self.addr = self.DEFAULT_ADDR
            self.port = self.DEFAULT_PORT
        else:
            try:
                self.addr, self.port = addrport.split(':')
            except ValueError:
                self.addr = self.DEFAULT_ADDR
                self.port = addrport

        try:
            self.port = int(self.port)
        except ValueError:
            raise CommandError("%r is not a valid port number." % self.port)

        self.stdout.write((
            "Fugleman version %(version)s\n"
            "Development server is running at http://%(addr)s:%(port)s/\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            'version': get_version(),
            'addr': self.addr,
            'port': self.port,
            'quit_command': (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C',
        })

        try:
            httpd = make_server(self.addr, self.port, WSGIHandler())
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            sys.exit(0)