Documentation_

.. _Documentation: https://sixtynorthartifactory1.jfrog.io/artifactory/documentation/gjenta/index.html

========
img2segy
========

A tool for converting images to SEG-Y files.


Installation
============

Install ``gjenta`` from the PyPI with ``pip``::

  python -m pip install img2segy

or if you have pipx and only want to run img2segy from the command line::

  pipx install img2segy

Basic usage
===========

Given an image file, such as a ``my_cross_section.png`` containing a vertical cross-section provide
information about the location of the image in a text (TOML) file called ``my_cross_section.toml``,
and run the ``img2segy convert`` command, supplying the image filename. If the TOML file has the
same filename stem it will be discovered and used.

  img2segy convert my_cross_section.png

The resulting SEG-Y file will be called ``my_cross_section.segy``.

Configuration file format
-------------------------

The configuration file contains subsections which describe the position of the image in geographical
space, the coordinate reference system in use, and control over how the image should be represented
in SEG-Y:

.. code-block:: toml

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


Development
===========

Deployment
----------

  $ pip install -e .[dev]
  $ bumpversion minor
  $ python setup.py sdist bdist_wheel
  $ twine upload --config-file <path>/sixty-north.pypirc dist/*
  $ git push origin
