from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI(title="e-com")

# CORS configuration to allow frontend requests from specified origins
origins = [
    "http://localhost:3000",  # Frontend (React) origin
]

# Apply CORS middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(router)

# Entry point for running via Python (not typically used in FastAPI)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
