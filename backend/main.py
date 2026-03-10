from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from word_analyzer import analyze_text

app = FastAPI()

# Add CORS middleware to allow requests from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """
    Health check endpoint.

    Returns:
        Simple message confirming API is running
    """
    return {"message": "Reading Helper API is running!"}

@app.post("/process-text")
async def process_text(file: UploadFile):
    """
    Process uploaded text file and identify hard words.

    Args:
        file: Uploaded text file

    Returns:
        JSON with filename and processed word data
    """
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
    
    
    # Analyze the text
    processed_words = analyze_text(text)

    # Return structured response
    return processed_words
    
