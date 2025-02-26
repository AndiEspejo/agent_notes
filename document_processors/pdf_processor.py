from typing import List
import fitz  # PyMuPDF
from .base_processor import BaseDocumentProcessor
from utils.text_chunker import chunk_text

class PDFProcessor(BaseDocumentProcessor):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def process(self, file_path: str) -> List[str]:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        
        return chunk_text(text, self.chunk_size, self.chunk_overlap) 