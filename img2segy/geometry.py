from euclidian.cartesian2 import Point2, Segment2


class ConfigurationError(Exception):
    pass


class Geometry:

    @classmethod
    def from_config(cls, config):
        try:
            position = config["position"]
            start = position["start"]
            end = position["end"]
            depth = position["depth"]
            return cls(
                start_xy=Point2(start["easting"], float(start["northing"])),
                end_xy=Point2(float(end["easting"]), float(end["northing"])),
                top_z=float(depth["top"]),
                bottom_z=float(depth["bottom"]),
            )
        except (KeyError, ValueError) as e:
            raise ConfigurationError(str(e)) from e


    def __init__(self, start_xy: Point2, end_xy: Point2, top_z: float, bottom_z: float):
        self._segment = Segment2(start_xy, end_xy)
        self._top_z = top_z
        self._bottom_z = bottom_z

    def __repr__(self):
        return f"{type(self).__name__}(start_xy={self._segment.source}, end_xy={self._segment.target}, top_z={self._top_z}, bottom_z={self._bottom_z})"

    def interpolate_xy(self, proportion):
        """Interpolate between the start and end positions.

        Args:
            proportion: A number between zero and one inclusive.

        Returns: A Point2 on the line between start and end.
        """
        return self._segment.lerp(proportion)

