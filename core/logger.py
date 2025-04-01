from loguru import logger
import sys

# Remove default logger to prevent duplicates
logger.remove()

# Configure logger
logger.add(
    sys.stdout,  # Output logs to the console
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>",
    level="DEBUG",
)

logger.add(
    "logs/app.log",  # Save logs to file
    rotation="10MB",  # Rotate logs when they reach 10MB
    compression="zip",  # Compress old logs
    level="INFO",  # Log only INFO and higher levels to file
    serialize=False  # Set to True for JSON logs (optional)
)

# Redirect standard logging (FastAPI logs) to Loguru
import logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Convert standard logging messages to Loguru
        level = record.levelname.lower()
        logger.opt(depth=6).log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
logging.getLogger().handlers = [InterceptHandler()]

# FastAPI internal logger redirection
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]

# Export logger to be used everywhere
__all__ = ["logger"]
