import logging
import sys

class SystemdHandler(logging.Handler):
    PREFIX = {
        logging.CRITICAL: "<CRITICAL> ",
        logging.ERROR: "<ERROR> ",
        logging.WARNING: "<WARNING> ",
        logging.INFO: "<INFO> ",
        logging.DEBUG: "<DEBUG> ",
        logging.NOTSET: "<DEBUG> "
    }

    def __init__(self, stream=sys.stdout):
        self.stream = stream
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            msg = self.PREFIX[record.levelno] + self.format(record)
            msg = msg.replace("\n", "\\n")
            self.stream.write(msg + "\n")
            self.stream.flush()
        except Exception:
            self.handleError(record)
