from dataclasses import dataclass

from euclidian.cartesian2 import Point2, Segment2

MICROSECONDS_PER_MILLISECOND = 1000


class ConfigurationError(Exception):
    pass


@dataclass(frozen=True)
class CoordinateReferenceSystem:
    horizontal_units: str
    vertical_units: str
    map_projection: str
    zone_id: str


class Geometry:

    @classmethod
    def from_config(cls, config):
        try:
            position = config["position"]
            left = position["left"]
            right = position["right"]
            depth = position["depth"]
            crs = config.get("coordinate-reference-system", {})

            return cls(
                left_xy=Point2(left["x"], float(left["y"])),
                right_xy=Point2(float(right["x"]), float(right["y"])),
                top_z=float(depth["top"]),
                bottom_z=float(depth["bottom"]),
                coordinate_reference_system=CoordinateReferenceSystem(
                    map_projection=str(crs.get("map-projection", "")),
                    horizontal_units=str(crs.get("horizontal-units", "")),
                    vertical_units=str(crs.get("vertical-units", "")),
                    zone_id=str(crs.get("zone-id", "")),
                )
            )
        except (KeyError, ValueError) as e:
            raise ConfigurationError(str(e)) from e


    def __init__(
            self,
            left_xy: Point2,
            right_xy: Point2,
            top_z: float,
            bottom_z: float,
            coordinate_reference_system: CoordinateReferenceSystem
    ):
        self._segment = Segment2(left_xy, right_xy)
        self._top_z = top_z
        self._bottom_z = bottom_z
        self._coordinate_reference_system = coordinate_reference_system

    def __repr__(self):
        return f"{type(self).__name__}(start_xy={self._segment.source}, end_xy={self._segment.target}, top_z={self._top_z}, bottom_z={self._bottom_z})"

    @property
    def left_xy(self):
        return self._segment.source

    @property
    def right_xy(self):
        return self._segment.target

    @property
    def top_z(self):
        return self._top_z

    @property
    def bottom_z(self):
        return self._bottom_z

    def interpolate_xy(self, proportion):
        """Interpolate between the start and end positions.

        Args:
            proportion: A number between zero and one inclusive.

        Returns: A Point2 on the line between left and right.
        """
        return self._segment.lerp(proportion)

    def sample_interval_z(self, num_samples):
        """The sample interval of the data.

        Note the units are 1000 times smaller than the depth units.
        This is in microseconds where two-way-time might be in milliseconds, or in millimetres
        where depth might be in metres, or thousands of a foot if depth is in feet.
        """
        return MICROSECONDS_PER_MILLISECOND * (self._bottom_z - self._top_z) / (num_samples - 1)

    @property
    def coordinate_reference_system(self):
        """A string describing the coordinate reference system used.
        """
        return self._coordinate_reference_system




