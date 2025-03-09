from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.khan_data import router as khan_router
from configurations import client
import logging
import uvicorn


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Include router with the full prefix
app.include_router(khan_router, prefix="/api/khan", tags=["khan"])

@app.get("/")
async def root():
    return {"message": "Khan Academy Data API"}

@app.get("/api-test")
async def api_test():
    """Simple test endpoint at the app level"""
    return {"status": "success", "message": "API root is working"}

if __name__ == "__main__":
    print("Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

