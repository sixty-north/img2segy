from functools import lru_cache

from PIL import Image, ImageOps
import numpy as np
from segpy.dataset import Dataset
from segpy.trace_header import TraceHeaderRev1

from img2segy.geometry import Geometry


class TraceHeaderMapper:

    @classmethod
    def from_config(cls, config):
        segy = config["segy"]
        trace_header = segy["trace-header"]
        position_field = segy["position-field"]
        return cls(
            position_in_source_coords=bool(position_field.get("source-coord-fields", True)),
            position_in_group_coords=bool(position_field.get("group-coord-fields", True)),
            position_in_cdp_coords=bool(position_field.get("cdp-coord-fields", True)),
            base_trace_number=int(trace_header.get("base-trace-number", 0)),
        )

    def __init__(
            self, *,
            position_in_source_coords,
            position_in_group_coords,
            position_in_cdp_coords,
            base_trace_number=0
    ):
        self._position_in_source_coords = position_in_source_coords
        self._position_in_group_coords = position_in_group_coords
        self._position_in_cdp_coords = position_in_cdp_coords
        # TODO: Validate that at least one of these is True
        self._base_trace_number = base_trace_number

    def position(self, p, xy_scalar):
        fields = {}
        if self._position_in_source_coords:
            fields["source_x"] = self._scale(p[0], xy_scalar)
            fields["source_y"] = self._scale(p[1], xy_scalar)
        if self._position_in_group_coords:
            fields["group_x"] = self._scale(p[0], xy_scalar)
            fields["group_y"] = self._scale(p[1], xy_scalar)
        if self._position_in_cdp_coords:
            fields["cdp_x"] = self._scale(p[0], xy_scalar)
            fields["cdp_y"] = self._scale(p[1], xy_scalar)
        return fields

    def _scale(self, coord, xy_scalar):
        if xy_scalar > 0:
            return coord / xy_scalar
        elif xy_scalar < 0:
            return coord * xy_scalar
        else:
            raise ValueError("xy_scalar cannot be zero")

    def trace_number(self, trace_index):
        return self._base_trace_number + trace_index


class ImageDataset(Dataset):

    def __init__(
            self,
            image: Image,
            geometry: Geometry,
            trace_header_mapper: TraceHeaderMapper,
    ):
        self._image = ImageOps.grayscale(image)
        self._geometry = geometry
        self._array = np.array(image)
        self._trace_header_mapper = trace_header_mapper
        # We need to check the geometry and the image up front to determine the
        # xy_scalar value used to scale the coordinates
        self._xy_scalar = 1.0

    @property
    def textual_reel_header(self):
        pass

    @property
    def binary_reel_header(self):
        pass

    @property
    def extended_textual_header(self):
        pass

    @property
    def dimensionality(self):
        return 2

    def trace_indexes(self):
        pass

    def num_traces(self):
        return self._image.width()

    def trace_header(self, trace_index):
        proportion = trace_index / (self.num_traces() / 1)
        position = self._geometry.interpolate_xy(proportion)
        position_fields = self._trace_header_mapper.position(position, self._xy_scalar)

        return TraceHeaderRev1(
            trace_num=self._trace_number(trace_index),
            **position_fields
        )

    def _trace_number(self, trace_index):
        return self._trace_header_mapper.trace_number(trace_index)

    def trace_samples(self, trace_index, start=None, stop=None):
        return self._array[slice(start, stop), trace_index]
