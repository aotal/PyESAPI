from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.core.config import logger
from app.services.esapi_worker import start_worker_thread, esapi_ready
from app.routers import aria

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start ESAPI worker
    logger.info("Starting ESAPI Worker thread...")
    worker_thread = start_worker_thread()
    yield
    # Shutdown logic if needed (handled by atexit in worker mostly, but could signal here)
    logger.info("Shutting down Application...")

app = FastAPI(
    title="PyESAPI Aria Service",
    description="FastAPI service for accessing Varian ARIA via ESAPI",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(aria.router)

@app.get("/")
def root():
    return {"status": "Online", "esapi_ready": esapi_ready.is_set()}

def main():
    """Entry point for running the application directly."""
    logger.info("Arrancando servidor Uvicorn...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
