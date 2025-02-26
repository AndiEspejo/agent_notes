import os
import uvicorn
import tempfile
from typing import List, Dict
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.agent import StudyAgent

# Request/Response models
class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

class DocumentInfo(BaseModel):
    filename: str
    path: str
    size: int
    extension: str

# Initialize FastAPI app
app = FastAPI(title="Study Agent API", 
              description="API for interacting with the local study agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = StudyAgent()

@app.on_event("startup")
async def startup_event():
    agent.start()

@app.on_event("shutdown")
async def shutdown_event():
    agent.stop()

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """Send a message to the study agent and get a response"""
    try:
        response = agent.chat(request.message)
        return MessageResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/upload", response_model=Dict[str, str])
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload a document to the knowledge base"""
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in agent.processors:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
    
    try:
        file_path = os.path.join(agent.knowledge_base.documents_dir, file.filename)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Read the uploaded file and write to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        os.rename(temp_file_path, file_path)
        
        background_tasks.add_task(agent.process_new_document, file_path)
        
        return {"message": f"Document {file.filename} uploaded successfully and is being processed"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@app.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """List all documents in the knowledge base"""
    try:
        documents = []
        for root, _, files in os.walk(agent.knowledge_base.documents_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_ext = os.path.splitext(filename)[1].lower()
                
                # Only include supported document types
                if file_ext in agent.processors:
                    documents.append(
                        DocumentInfo(
                            filename=filename,
                            path=file_path,
                            size=os.path.getsize(file_path),
                            extension=file_ext
                        )
                    )
        
        return documents
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

frontend_dir = "frontend/dist"
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    @app.get("/")
    async def frontend_not_built():
        return {
            "message": "Frontend not built yet. Please run 'cd frontend && npm install && npm run build'",
            "status": "API is running and healthy. Use the /chat, /upload, and /documents endpoints."
        }

def start_server():
    """Start the FastAPI server"""
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start_server() 