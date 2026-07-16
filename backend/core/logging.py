import logging
from logging.handlers import RotatingFileHandler
import os
from core.config import settings

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

def configure_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            RotatingFileHandler(
                os.path.join(settings.data_dir, 'app.log'),
                maxBytes=10485760,
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    
    if settings.sentry_dsn:
        import sentry_sdk
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=1.0
        )
