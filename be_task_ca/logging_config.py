import logging


def initialise_logging(log_level: str = "INFO", sqlalchemy_level: str = "WARNING"):
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)
