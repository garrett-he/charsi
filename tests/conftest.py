import importlib.resources
import pytest
from click.testing import CliRunner


@pytest.fixture(scope='function')
def cli_runner():
    return CliRunner()


@pytest.fixture(scope='module')
def presence_states():
    return importlib.resources.files('tests.res').joinpath('presence-states.json')
