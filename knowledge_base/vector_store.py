import os
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config.settings import settings

class KnowledgeBase:
    def __init__(self):
        self.documents_dir = settings.documents_dir
        
        os.makedirs(settings.vector_store_path, exist_ok=True)
        os.makedirs(self.documents_dir, exist_ok=True)
        
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key
        )
        
        self.vector_store = Chroma(
            persist_directory=settings.vector_store_path,
            embedding_function=self.embeddings
        )
        
    def add_texts(self, texts: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Add new texts to the knowledge base with metadata"""
        if not texts:  
            print("Warning: Attempted to add empty text list to knowledge base")
            return
            
        self.vector_store.add_texts(texts=texts, metadatas=metadata)
        
    def search(self, query: str, k: int = 5) -> List[str]:
        """Search the knowledge base for relevant documents"""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return [] 