from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from logger import logger

from logger import setup_logging
from api.routes import router as api_router

app = FastAPI()

app = FastAPI(
    title="0u0 backend API", docs_url="/docs"
)

# Include CORS middleware setup in main.py
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


setup_logging()

# Include the router in your FastAPI app
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
