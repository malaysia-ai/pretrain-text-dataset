"""Text deduplication simplified."""

import logging

from rich.logging import RichHandler

logger = logging.getLogger("text_dedup")
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler(rich_tracebacks=True))
logger.propagate = False