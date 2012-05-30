from unittest import TestCase

from mock import Mock

from fugleman.commands import CommandError, ServeCommand


class ServeCommandTestCase(TestCase):

    def setUp(self):
        self.command = ServeCommand(Mock(), Mock(), Mock(), Mock())
        self.command.run = Mock()

    def test_it_has_a_defaults(self):
        self.command.handle()
        self.command.run.assert_called_with(ServeCommand.DEFAULT_ADDR, int(ServeCommand.DEFAULT_PORT))

    def test_it_supports_colon_seperated_addr_and_port(self):
        self.command.handle('172.0.0.1:9999')
        self.command.run.assert_called_with('172.0.0.1', 9999)

    def test_it_converts_port_to_integer(self):
        self.command.handle('9999')
        self.command.run.assert_called_with(ServeCommand.DEFAULT_ADDR, 9999)

    def test_it_raises_error_when_port_is_not_valid(self):
        self.assertRaises(CommandError, self.command.handle, 'not-a-port-number')
