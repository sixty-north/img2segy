from dataclasses import dataclass

from euclidian.cartesian2 import Point2, Segment2


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
            start = position["start"]
            end = position["end"]
            depth = position["depth"]
            crs = config.get("coordinate-reference-system", {})

            return cls(
                start_xy=Point2(start["x"], float(start["y"])),
                end_xy=Point2(float(end["x"]), float(end["y"])),
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
            start_xy: Point2,
            end_xy: Point2,
            top_z: float,
            bottom_z: float,
            coordinate_reference_system: CoordinateReferenceSystem
    ):
        self._segment = Segment2(start_xy, end_xy)
        self._top_z = top_z
        self._bottom_z = bottom_z
        self._coordinate_reference_system = coordinate_reference_system

    def __repr__(self):
        return f"{type(self).__name__}(start_xy={self._segment.source}, end_xy={self._segment.target}, top_z={self._top_z}, bottom_z={self._bottom_z})"

    @property
    def start_xy(self):
        return self._segment.source

    @property
    def end_xy(self):
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

        Returns: A Point2 on the line between start and end.
        """
        return self._segment.lerp(proportion)

    def sample_interval_z(self, num_samples):
        """The sample interval of the data.
        """
        return (self._bottom_z - self._top_z) / (num_samples - 1)

    @property
    def coordinate_reference_system(self):
        """A string describing the coordinate reference system used.
        """
        return self._coordinate_reference_system




