import pytest
from click.testing import CliRunner

from .res import get_filepath


@pytest.fixture(scope='module')
def cli_runner():
    return CliRunner()


@pytest.fixture(scope='module')
def path_presence_states_json():
    return get_filepath('presence-states.json')


@pytest.fixture(scope='module')
def path_recipe1_recipe():
    return get_filepath('recipe1.recipe')


@pytest.fixture(scope='module')
def path_recipe2_recipe():
    return get_filepath('recipe2.recipe')


@pytest.fixture(scope='module')
def path_instructions_lua():
    return get_filepath('instructions.lua')
