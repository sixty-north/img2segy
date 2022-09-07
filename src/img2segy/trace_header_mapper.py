class TraceHeaderMapper:

    @classmethod
    def from_config(cls, config):
        segy = config["segy"]
        trace_position_field = segy["trace-position"]
        trace_number_field = segy["trace-number"]
        return cls(
            place_position_in_source_coords=bool(trace_position_field.get("use-source-coord-fields", True)),
            place_position_in_group_coords=bool(trace_position_field.get("use-group-coord-fields", True)),
            place_position_in_cdp_coords=bool(trace_position_field.get("use-cdp-coord-fields", True)),
            place_trace_number_in_trace_number=bool(trace_number_field.get("use-trace-number-field", True)),
            place_trace_number_in_crossline_number=bool(trace_number_field.get("use-crossline-number-field", True)),
            base_trace_number=int(trace_position_field.get("base-trace-number", 0)),
        )

    def __init__(
            self, *,
            place_position_in_source_coords,
            place_position_in_group_coords,
            place_position_in_cdp_coords,
            place_trace_number_in_trace_number,
            place_trace_number_in_crossline_number,
            base_trace_number=0
    ):
        self._place_position_in_source_coords = place_position_in_source_coords
        self._place_position_in_group_coords = place_position_in_group_coords
        self._place_position_in_cdp_coords = place_position_in_cdp_coords
        # TODO: Validate that at least one of these is True


        self._place_trace_number_in_trace_number = place_trace_number_in_trace_number
        self._place_trace_number_in_crossline_number = place_trace_number_in_crossline_number
        # TODO: Validate that at least one of these is True


        self._base_trace_number = base_trace_number

    def position(self, p, xy_scalar):
        fields = {}
        if self._place_position_in_source_coords:
            fields["source_x"] = self._scale(p[0], xy_scalar)
            fields["source_y"] = self._scale(p[1], xy_scalar)
        if self._place_position_in_group_coords:
            fields["group_x"] = self._scale(p[0], xy_scalar)
            fields["group_y"] = self._scale(p[1], xy_scalar)
        if self._place_position_in_cdp_coords:
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
        trace_number = self._base_trace_number + trace_index
        fields = {}
        if self._place_trace_number_in_trace_number:
            fields["trace_num"] = trace_number
        if self._place_trace_number_in_crossline_number:
            fields["crossline_number"] = trace_number
        return fields
