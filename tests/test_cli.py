import importlib.metadata

import click.testing
import click

from charsi.__main__ import cli


def test_cli(cli_runner: click.testing.CliRunner):
    result = cli_runner.invoke(cli, ['--version'])

    if result.exception:
        print(result.output)

    assert not result.exception
    assert result.output.strip() == importlib.metadata.version('charsi')
