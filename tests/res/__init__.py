from pathlib import Path


def get_filepath(filename: str) -> Path:
    return Path(__file__).parent.joinpath(filename)
