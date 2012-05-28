from unittest import TestCase
from StringIO import StringIO

from mock import Mock

from fugleman import get_version
from fugleman.cli.runner import CommandRunner


class BaseCommandRunnerTestCase(TestCase):

    def call_command(self, *args):
        self.output = StringIO()
        runner = CommandRunner(list(args), stdout=self.output)
        runner = self.pre_command_run(runner)
        try:
            runner.run()
        except SystemExit:
            pass  # Ignore error exits
        self.output.seek(0)
        lines = self.output.readlines()
        self.output.close()
        return lines

    def pre_command_run(self, runner):
        """
        Subclasses can hook into this to modify the runner before run
        is called.

        """
        return runner


class CommandRunnerTestCase(BaseCommandRunnerTestCase):

    def test_it_defaults_to_help_when_no_arguments_are_passed(self):
        response = self.call_command('PROGNAME')
        self.assertIn('Usage: PROGNAME subcommand [options] [args]\n', response)
        self.assertIn("Type 'PROGNAME help <subcommand>' for help on a specific subcommand.\n", response)

    def test_it_has_a_version_subcommand(self):
        response = self.call_command('PROGNAME', 'version')
        self.assertIn('%s\n' % get_version(), response)

    def test_it_prints_a_command_error_on_invalid_command(self):
        response = self.call_command('PROGNAME', 'not-a-subcommand')
        self.assertIn("Unknown command: 'not-a-subcommand'\n", response)
        self.assertIn("Type 'PROGNAME help' for usage.\n", response)


class CommandRunnerWithSubcommandTestCase(BaseCommandRunnerTestCase):

    def setUp(self):
        self.subcommand = Mock()
        self.subcommand_class = Mock(return_value=self.subcommand)

    def pre_command_run(self, runner):
        runner.subcommands = {'dostuff': self.subcommand_class}
        return runner

    def test_it_passed_argv_to_the_subcommand(self):
        self.call_command('PROGNAME', 'dostuff')
        self.subcommand_class.assert_called_with('PROGNAME', 'dostuff', [], self.output)

    def test_it_runs_the_subcommand(self):
        self.call_command('PROGNAME', 'dostuff')
        self.subcommand.run.assert_called_with()

    def test_it_prints_help_for_the_subcommand(self):
        self.call_command('PROGNAME', 'help', 'dostuff')
        self.subcommand.print_help.assert_called_with()
