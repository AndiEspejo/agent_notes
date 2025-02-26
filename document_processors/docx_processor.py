from typing import List
import docx
from .base_processor import BaseDocumentProcessor
from utils.text_chunker import chunk_text

class DocxProcessor(BaseDocumentProcessor):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def process(self, file_path: str) -> List[str]:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return chunk_text(text, self.chunk_size, self.chunk_overlap) 