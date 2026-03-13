import logging
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from word_analyzer import analyze_text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Configure root logger for the application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("reading_helper")

app = FastAPI()

# Add CORS middleware to allow requests from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-text")
async def process_text(file: UploadFile):
    """
    Process uploaded text file and identify hard words.

    Args:
        file: Uploaded text file

    Returns:
        JSON with filename and processed word data
    """
    logger.info("Received file upload: %s", file.filename)
    # Read file content
    content = await file.read()
    text = content.decode("utf-8")
    
    # Analyze the text
    processed_words = analyze_text(text)

    # Return structured response
    return {
        "filename": file.filename,
        "processed_words": processed_words
    }
@app.post("/test-text")
async def test_text(text: str):
    """
    Process uploaded text file and identify hard words.

    Args:
        text string

    Returns:
        JSON with filename and processed word data
    """
    
    
    logger.info("Received test-text request (len=%d)", len(text))
    # Analyze the text
    processed_words = analyze_text(text)

    # Return structured response
    return processed_words

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    """
    Serve the React app's index.html for the root URL.
    """
    return FileResponse("static/index.html")

