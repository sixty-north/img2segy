from img2segy.geometry import Geometry


def test_load_geometry_from_toml_does_not_raise_errors(example_config):
    Geometry.from_config(example_config)

