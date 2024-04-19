from unittest.mock import patch

import click
from click.testing import CliRunner

from charsi import __version__
from charsi.__main__ import cli, print_version


def test_cli(cli_runner: CliRunner):
    result = cli_runner.invoke(cli, ['--version'])

    assert not result.exception
    assert result.output.strip() == __version__


def test_print_version():
    ctx = click.Context(click.Command('test-command'))

    with patch.object(click, 'echo') as echo_mock, patch.object(ctx, 'exit'):
        print_version(ctx, None, False)
        echo_mock.assert_not_called()

        print_version(ctx, None, True)
        echo_mock.assert_called_with(__version__)
