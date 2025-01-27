import logging


def initialise_logging(log_level: str = "INFO"):
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
