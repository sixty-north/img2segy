from pathlib import Path

import pytest
import toml

TESTS_DIRPATH = Path(__file__).resolve().parent
DATA_DIRPATH = TESTS_DIRPATH.parent / "data"
EXAMPLE_DIRPATH = DATA_DIRPATH / "example"

@pytest.fixture
def example_dirpath() -> Path:
    return EXAMPLE_DIRPATH


@pytest.fixture
def example_config(example_dirpath):
    config_filepath = example_dirpath / "example.toml"
    return toml.load(config_filepath)
