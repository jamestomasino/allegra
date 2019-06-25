import logging
import sys

class SystemdHandler(logging.Handler):
    PREFIX = {
        #logging.EMERG: "<0>",
        #logging.ALERT: "<1>",
        logging.CRITICAL: "<2>",
        logging.ERROR: "<3>",
        logging.WARNING: "<4>",
        #logging.NOTICE: "<5>",
        logging.INFO: "<6>",
        logging.DEBUG: "<7>",
        logging.NOTSET: "<7>"
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
