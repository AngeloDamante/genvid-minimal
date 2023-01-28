import logging


def configure_logging(log_lvl=logging.DEBUG, log_console=False, log_filename: str = None):
    """

    @param log_lvl: logging level e.g. logging.DEBUG
    @param log_console: set true to log to console instead of file
    @param log_filename: lof filename e.g. out.log or log_out_configurator.txt
    """
    fmt = '%(asctime)s %(levelname)s: %(message)s'
    datefmt = '%m/%d/%Y %I:%M:%S %p'
    if log_console:
        logging.basicConfig(format=fmt, datefmt=datefmt, level=log_lvl)
    else:
        logging.basicConfig(format=fmt, datefmt=datefmt, level=log_lvl, filename=log_filename)