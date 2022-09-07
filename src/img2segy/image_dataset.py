from pathlib import Path

from PIL import Image, ImageOps
import numpy as np
import datetime

from euclidian.cartesian2 import Point2
from segpy.binary_reel_header import BinaryReelHeader, TraceSorting, FixedLengthTraceFlag, \
    MeasurementSystem
from segpy.dataset import Dataset
from segpy.datatypes import DataSampleFormat, data_sample_format_size_in_bytes, data_sample_format_description
from segpy.revisions import SegYRevision
from segpy.toolkit import format_standard_textual_header
from segpy.trace_header import TraceHeaderRev1, CoordinateUnits

from img2segy.geometry import Geometry, MICROSECONDS_PER_MILLISECOND
from img2segy.trace_header_mapper import TraceHeaderMapper
from img2segy.version import __version__

DMS = "DMS"
ARCSECONDS = "ARCSECONDS"
DEC_DEGREES = "DEC-DEGREES"
FEET = "FEET"
METERS = "METERS"


class ImageDataset(Dataset):

    def __init__(
            self,
            image: Image,
            geometry: Geometry,
            trace_header_mapper: TraceHeaderMapper,
    ):
        self._image = image
        self._geometry = geometry
        # Convert the image to an 8-bit grayscale (uint8 0 to 255) then shift to (int8 -128 to 127)
        self._array = (np.array(ImageOps.grayscale(image)) - 128).view(np.int8)
        self._trace_header_mapper = trace_header_mapper
        # We need to check the geometry and the image up front to determine the
        # xy_scalar value used to scale the coordinates
        self._xy_scalar = 1.0

    @property
    def textual_reel_header(self):
        return format_standard_textual_header(
            revision=SegYRevision.REVISION_1,
            samples_per_trace=self._samples_per_trace(),
            sample_interval=self._sample_interval(),
            bytes_per_sample=self._bytes_per_sample(),
            measurement_system=self._measurement_system(),
            coordinate_units=self._coordinate_units(),
            map_projection=self._map_projection(),
            zone_id=self._zone_id(),
            unassigned1=f"Converted from {self._image_filename()} by img2segy {__version__}",
            unassigned2=f"on {datetime.date.today().isoformat()}",
            unassigned3=f"img2segy <https://github.com/sixty-north/img2segy> by Sixty North AS",
            unassigned4=f"Image size: {self._image.width}x{self._image.height}",
            unassigned5=f"",
            unassigned6=f"Coordinate reference system : {self._map_projection()} {self._zone_id()}",
            unassigned7=f"Horizontal (xy) units : {self._coordinate_units()}",
            unassigned8=f"Vertical (z/depth) units : {self._measurement_system()}",
            unassigned9=f"",
            unassigned10=f"Left : x = {self._left_xy()[0]} y = {self._left_xy()[1]}",
            unassigned11=f"Right  : x = {self._end_xy()[0]} y = {self._end_xy()[1]}",
            unassigned12=f"Depth : top-z = {self._top_z()} bottom-z = {self._bottom_z()}",
            unassigned13=f"",
            unassigned14=f"Data sample format : {self._data_sample_description()}",
            unassigned15=f"Vertical sample interval : {self._sample_interval()} {self._measurement_system()}/{MICROSECONDS_PER_MILLISECOND}",
        )

    @property
    def binary_reel_header(self):
        return BinaryReelHeader(
            sample_interval=self._sample_interval(),
            num_samples=self._samples_per_trace(),
            data_sample_format=self._data_sample_format(),
            trace_sorting=TraceSorting.COMMON_MIDPOINT,
            format_revision_num=SegYRevision.REVISION_1,
            fixed_length_trace_flag=FixedLengthTraceFlag.FIXED_LENGTH,
            measurement_system=self._measurement_system_code(),
            ensemble_fold=1,
        )

    @property
    def extended_textual_header(self):
        return []

    @property
    def dimensionality(self):
        return 2

    def num_traces(self):
        return self._image.width

    def trace_header(self, trace_index):
        proportion = trace_index / (self.num_traces() / 1)
        position = self._geometry.interpolate_xy(proportion)
        position_fields = self._trace_header_mapper.position(position, self._xy_scalar)
        trace_number_fields = self._trace_header_mapper.trace_number(trace_index)

        return TraceHeaderRev1(
            sample_interval=self._sample_interval(),
            coordinate_units=self._coordinate_units_code(),
            **trace_number_fields,
            **position_fields
        )

    def _trace_number(self, trace_index):
        return self._trace_header_mapper.trace_number(trace_index)

    def trace_samples(self, trace_index, start=None, stop=None):
        return self._array[slice(start, stop), trace_index]

    def _samples_per_trace(self):
        return self._image.height

    def _sample_interval(self):
        """The vertical interval between samples in a trace."""
        return self._geometry.sample_interval_z(self._samples_per_trace())

    def _bytes_per_sample(self):
        return data_sample_format_size_in_bytes(self._data_sample_format())

    def _data_sample_description(self):
        return data_sample_format_description(self._data_sample_format())

    def _map_projection(self):
        return self._geometry.coordinate_reference_system.map_projection

    def _zone_id(self):
        return self._geometry.coordinate_reference_system.zone_id

    def _measurement_system(self):
        # TODO: This is wrong, because we don't know the vertical units and have no way of
        #       representing that within SEG-Y. This value should actually pertain to the
        #       horizontal units and comes into play with _coordinate_units_code is LENGTH.
        #       The vertical units in SEG-Y are always milliseconds (or microseconds for the
        #       sample interval), except when they're not.
        vertical_units = self._geometry.coordinate_reference_system.vertical_units.upper()
        if vertical_units in {METERS, "METRES", "M"}:
            return METERS
        if vertical_units in {FEET, "FOOT", "FT", "'"}:
            return FEET
        return vertical_units

    def _measurement_system_code(self):
        system_name = self._measurement_system()
        try:
            return MeasurementSystem[system_name]
        except KeyError:
            return MeasurementSystem.UNKNOWN

    def _coordinate_units(self):
        horizontal_units = self._geometry.coordinate_reference_system.horizontal_units.upper()
        if horizontal_units in {METERS, "METRES", "METER", "METRE", "M"}:
            return METERS
        if horizontal_units in {FEET, "FOOT", "FT", "'"}:
            return FEET
        if horizontal_units in {DEC_DEGREES, "DECIMAL-DEGREES", "DEGREES", "DEG", "D", "°"}:
            return DEC_DEGREES
        if horizontal_units in {DMS}:
            return DMS
        if horizontal_units in {ARCSECONDS, "ARC-SECONDS", "SECONDS-OF-ARC", "SECONDS", "S", '"'}:
            return ARCSECONDS
        return horizontal_units

    def _coordinate_units_code(self):
        coordinate_units = self._coordinate_units()
        if coordinate_units in {METERS, FEET}:
            return CoordinateUnits.LENGTH
        if coordinate_units in {ARCSECONDS}:
            return CoordinateUnits.SECONDS_OF_ARC
        if coordinate_units in {DEC_DEGREES}:
            return CoordinateUnits.DECIMAL_DEGREES
        if coordinate_units in {DMS}:
            return CoordinateUnits.DMS
        return CoordinateUnits.UNKNOWN

    def _data_sample_format(self):
        # Currently we only support 8-bit grayscale. In future we could add support for 16-bit.
        return DataSampleFormat.INT8

    def _left_xy(self) -> Point2:
        """Geographic position of the left side of the image."""
        return self._geometry.left_xy

    def _end_xy(self) -> Point2:
        """Geographic position of the right side of the image."""
        return self._geometry.right_xy

    def _top_z(self):
        return self._geometry.top_z

    def _bottom_z(self):
        return self._geometry.bottom_z

    def _image_filename(self):
        try:
            filename = self._image.filename
            if filename:
                return Path(filename).name
        except AttributeError:
            pass
        return "<unknown>"
