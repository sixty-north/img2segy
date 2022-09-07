========
img2segy
========

A tool for converting images to SEG-Y files.

.. note::
   `img2segy` is offered under an open source non-permissive license, the AGPL 3. Alternative
   commercial license terms may be available from Sixty North AS, as is help on using or
   extending ``img2segy``. Only basic support and fixes are provided gratis.


Installation
============

Install ``img2segy`` from the PyPI with ``pip``::

  python -m pip install img2segy

or if you have pipx and only want to run img2segy from the command line::

  pipx install img2segy

Basic usage
===========

Given an image file, such as a ``my_cross_section.png`` containing a vertical cross-section provide
information about the location of the image in a text (TOML) file called ``my_cross_section.toml``,
and run the ``img2segy convert`` command, supplying the image filename. If the TOML file has the
same filename stem it will be discovered and used::

  img2segy convert my_cross_section.png

The resulting SEG-Y file will be called ``my_cross_section.segy``.

Configuration file format
-------------------------

The configuration file contains subsections which describe the position of the image in geographical
space, the coordinate reference system in use, and control over how the image should be represented
in SEG-Y::

    [position]
    left.x = 527501
    left.y = 4840781

    right.x = 527326
    right.y = 4829018

    depth.top = 0
    depth.bottom = 4300

    [coordinate-reference-system]
    map-projection = "WGS-84 UTM"
    zone-id = 15
    horizontal-units = "m"
    vertical-units = "m"

    [segy]
    # encoding = "ASCII"
    # byte-order = ">"
    trace-position.use-source-coord-fields = true
    trace-position.use-group-coord-fields = true
    trace-position.use-cdp-coord-fields = true
    trace-number.use-trace-number-field = true
    trace-number.use-crossline-number-field = true

    base-trace-number = 1


Some of the fields, such as ``map-projection`` are ignored, but it's wise to include them anyway so
that the date is more self-documenting and the meaning of the numbers is clear to others and your
future self.

The ``[position]`` section contains information which locates the corners of the supplied image in
geographical space. The ``left.x`` and ``left.y`` entries are the geographic eastings and northings
respectively of the left edge of the image. Similarly, the ``right.x`` and ``right.y`` entries are
the geographic eastings and northings respectively of the right edge of the image. The ``depth.top``
and ``depth.bottom`` entries give the depths of the top and bottom edges of the image.

The number of traces in the resulting SEG-Y file will be equal to the horizontal number of pixels
across the supplied image. The number of samples per trace will be equal to the vertical number of
pixels down the image. If you want a different number of traces or samples than that which
corresponds to the pixel dimensions of the image, you should pre-process the image using other tools
before converting to SEG-Y.

The ``[[segy]]`` section specifies how the SEG-Y data will be written and controls which header
fields are used, and for what.

The optional ``trace-position`` entries ``trace-position.use-source-coord-fields``,
``trace-position.use-group-coord-fields`` and ``trace-position.use-cdp-coord-fields`` control
whether the horizontal component of geographic position of the trace, as linearly interpolated
between the two end points of the image, it written into the corresponding trace-header fields.

The ``trace-number`` entries ``trace-number.use-trace-number-field`` and
``trace-number.use-crossline-number-field`` control whether an integer trace number is written into
the corresponding trace-header fields. By default, the left-most column of pixels will be given
a trace-number of zero. You can control this by setting ``base-trace-number`` to some other value,
such as one. If you need trace numbering to start from the right edge of the image, you should flip
the image left-to-right before using ``img2segy``.

