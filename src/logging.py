import contextlib
import logging


@contextlib.contextmanager
def setup_logging():
    try:
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        )

        root.addHandler(handler)

        yield
    finally:
        logging.shutdown()
