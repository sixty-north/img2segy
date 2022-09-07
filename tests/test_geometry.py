from euclidian.cartesian2 import Point2

from img2segy.geometry import Geometry


def test_load_geometry_from_toml_does_not_raise_errors(example_config):
    Geometry.from_config(example_config)


def test_left_xy(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.left_xy == Point2(527501, 4840781)


def test_right_xy(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.right_xy == Point2(527326, 4829018)


def test_depth_top(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.top_z == 0


def test_depth_bottom(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.bottom_z == 4300


def test_crs_map_projection(example_config):
    geometry = Geometry.from_config(example_config)
    crs = geometry.coordinate_reference_system
    assert crs.map_projection == "WGS-84 UTM"


def test_crs_zone_id(example_config):
    geometry = Geometry.from_config(example_config)
    crs = geometry.coordinate_reference_system
    assert crs.zone_id == "19"


def test_crs_zone_horizontal_units(example_config):
    geometry = Geometry.from_config(example_config)
    crs = geometry.coordinate_reference_system
    assert crs.horizontal_units == "m"


def test_crs_zone_vertical_units(example_config):
    geometry = Geometry.from_config(example_config)
    crs = geometry.coordinate_reference_system
    assert crs.vertical_units == "m"


def test_interpolate_xy_at_zero(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.interpolate_xy(0) == geometry.left_xy


def test_interpolate_xy_at_one(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.interpolate_xy(1) == geometry.right_xy


def test_sample_interval(example_config):
    geometry = Geometry.from_config(example_config)
    assert geometry.sample_interval_z(2150) == 2000.9306654257794