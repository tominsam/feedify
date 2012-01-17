import logging
import traceback

class ExceptionMiddleware(object):

    def process_exception(self, request, exception):
        logging.error(traceback.format_exc())
        return None


