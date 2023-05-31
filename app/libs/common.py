import logging

from app.config.setting import settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
logger = logging.getLogger(settings.service_name)
