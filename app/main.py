from fastapi import FastAPI
from dotenv import load_dotenv
from app.endpoints import router as api_router
from common.logger import logger
import uvicorn

app = FastAPI(title="Text Behind Foreground API",
              description="Send your image",
              version="1.0.0"
              )

app.include_router(api_router)


if __name__ == "__main__":
    load_dotenv()
    logger.info("test")
    uvicorn.run("app.main:app",
                host="0.0.0.0",
                port=8000)