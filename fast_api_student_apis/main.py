from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os

# Try importing the router safely
try:
    from controllers.student_controller import router as student_router
except ModuleNotFoundError:
    student_router = None
    print("Warning: student_controller module not found. Swagger will still load.")

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Student API",
    description="API documentation for student management",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("student_api")
logger.info("Starting the FastAPI application...")

# CORS and security headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers if available
if student_router:
    app.include_router(student_router, prefix="/api/students")

# Redirect root to Swagger UI
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(
        path=os.path.join("static", "favicon-32x32.png"),
        media_type="image/png"
    )
