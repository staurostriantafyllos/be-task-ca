import logging


def initialise_logging(log_level=logging.INFO, sqlalchemy_level=logging.INFO):
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)
