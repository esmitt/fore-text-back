from loguru import logger
import sys
import logging

# Configure Loguru
logger.remove()
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)
logger.add(
    sys.stdout,
    format=log_format,
    level="DEBUG",
)
logger.add(
    "logs/app.log",
    rotation="10MB",
    compression="zip",
    level="INFO",
    serialize=False,
    format=log_format,
)
logger.add(
    "logs/debug.log",
    rotation="10MB",
    compression="zip",
    level="DEBUG",
    serialize=False,
    format=log_format,
)

# Custom handler to intercept standard logging and redirect to Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level
        level = record.levelname
        # Find the appropriate Loguru level
        try:
            level = logger.level(level).name
        except ValueError:
            level = record.levelno
        # Log with Loguru, preserving the original module and function
        logger.opt(depth=6).log(level, record.getMessage())

# Configure logging to use InterceptHandler
logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)
for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
    uvicorn_logger = logging.getLogger(logger_name)
    uvicorn_logger.handlers = [InterceptHandler()]
    uvicorn_logger.propagate = False
    uvicorn_logger.setLevel(logging.DEBUG)

__all__ = ["logger"]