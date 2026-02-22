import logging

from flask import request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_logging(app):
    @app.before_request
    def log_request_info():
        logger.info(f"Incoming Request: {request.method} {request.url}")
        # Be careful logging bodies in production due to PII, but useful in dev
        if request.is_json:
            try:
                pass # logger.info(f"Body: {request.json}")
            except Exception:
                pass
