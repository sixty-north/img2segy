import logging
from pathlib import Path

import toml
from PIL import Image, ImageOps
from segpy.writer import write_segy

from img2segy.geometry import Geometry
from img2segy.image_dataset import ImageDataset
from img2segy.trace_header_mapper import TraceHeaderMapper

logger = logging.getLogger(__name__)


def convert(image_filepath: Path, segy_filepath: Path=None, config_filepath: Path=None, *, force=False):
    """Convert an image to SEG-Y.

    Args:
        image_filepath: The path to a file containing an image.

        segy_filepath: An optional path to the SEG-Y file that will be produced. If not provided
            the path to will be generated by changing the extension of the image file to *.segy

        config_filepath: An optional path to a TOML file containing configuration information.
            If not provided this function will look for a config file with the same name as the
            image file, but with the *.toml file extension.
    """
    image_filepath = Path(image_filepath)
    segy_filepath = (segy_filepath and Path(segy_filepath)) or image_filepath.with_suffix(".segy")
    config_filepath = (config_filepath and Path(config_filepath)) or image_filepath.with_suffix(".toml")

    logger.info("segy_filepath = %s", segy_filepath)
    logger.info("image_filepath = %s", image_filepath)
    logger.info("config_filepath = %s", config_filepath)

    config = toml.load(config_filepath)
    geometry = Geometry.from_config(config)
    trace_header_mapper = TraceHeaderMapper.from_config(config)

    image = Image.open(image_filepath)
    dataset = ImageDataset(image, geometry, trace_header_mapper)

    with open(segy_filepath, 'wb') as segy_file:
        write_segy(segy_file, dataset)
