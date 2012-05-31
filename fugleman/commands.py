import os
import sys
from importlib import import_module
from optparse import OptionParser, make_option

from werkzeug.serving import run_simple

from fugleman import __version__


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
            version=__version__,
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

    def execute(self):
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
    option_list = (
        make_option('-f', '--fugfile',
            dest='fugfile',
            action='store',
            metavar='PATH',
            default='fugfile',
            help='Tells Fugleman what module to import. Defaults to fugfile.',
        ),
        make_option('-a', '--app',
            dest='application',
            action='store',
            metavar='APP',
            default='app',
            help='Tells Fugleman what the application variable is in the '
                 'fugfile. Defaults to app.',
        ),
    )
    help = "Starts a development server for serving your Fugleman project."
    args = '[optional port number, or ipaddr:port]'

    DEFAULT_ADDR = '127.0.0.1'
    DEFAULT_PORT = '8989'

    def handle(self, addrport=None, *args, **options):
        if addrport is None:
            addr = self.DEFAULT_ADDR
            port = self.DEFAULT_PORT
        else:
            try:
                addr, port = addrport.split(':')
            except ValueError:
                addr = self.DEFAULT_ADDR
                port = addrport

        try:
            port = int(port)
        except ValueError:
            raise CommandError("%r is not a valid port number." % port)

        module_name = options.get('fugfile')
        var_name = options.get('application')
        application = self.load_application(module_name, var_name)

        try:
            self.run(application, addr, port)
        except KeyboardInterrupt:
            sys.exit(0)

    def run(self, application, addr, port):
        self.stdout.write((
            "Fugleman version %(version)s\n"
            "Development server is running at http://%(addr)s:%(port)s/\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            'version': __version__,
            'addr': addr,
            'port': port,
            'quit_command': (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C',
        })
        run_simple(addr, port, application, use_reloader=True, use_debugger=True)

    def load_application(self, module_name, var_name):
        if os.getcwd() not in sys.path:
            sys.path.insert(0, os.getcwd())
            inserted = True
        else:
            inserted = False

        try:
            module = import_module(module_name)
        except ImportError:
            raise CommandError("Could not load the fugfile named '%s'" % module_name)
        finally:
            if inserted:
                del sys.path[0]

        try:
            return getattr(module, var_name)
        except AttributeError:
            raise CommandError("Cound not find the application named '%s'" % var_name)
