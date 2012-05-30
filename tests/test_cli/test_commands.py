from unittest import TestCase

from mock import Mock

from fugleman.management.commands import CommandError, ServeCommand


class ServeCommandTestCase(TestCase):

    def setUp(self):
        self.command = ServeCommand(Mock(), Mock(), Mock(), Mock())

    def test_it_has_a_default_addr(self):
        self.command.handle()
        self.assertEqual(self.command.addr, ServeCommand.DEFAULT_ADDR)

    def test_it_has_a_default_port(self):
        self.command.handle()
        self.assertEqual(self.command.port, int(ServeCommand.DEFAULT_PORT))

    def test_it_supports_colon_seperated_addr_and_port(self):
        self.command.handle('172.0.0.1:9999')
        self.assertEqual(self.command.addr, '172.0.0.1')
        self.assertEqual(int(self.command.port), 9999)

    def test_it_converts_port_to_integer(self):
        self.command.handle('9999')
        self.assertEqual(self.command.port, 9999)

    def test_it_raises_error_when_port_is_not_valid(self):
        self.assertRaises(CommandError, self.command.handle, 'not-a-port-number')
