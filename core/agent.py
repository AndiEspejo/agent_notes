import os
from typing import Dict, List, Optional
from pathlib import Path

from config.settings import settings
from document_processors.pdf_processor import PDFProcessor
from document_processors.docx_processor import DocxProcessor
from knowledge_base.vector_store import KnowledgeBase
from memory.conversation_memory import ConversationManager
from utils.file_watcher import DocumentWatcher

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class StudyAgent:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.memory = ConversationManager()
        
        self.processors = {
            ".pdf": PDFProcessor(),
            ".docx": DocxProcessor()
        }
        
        self.llm = ChatOpenAI(
            model=settings.completion_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.7
        )
        
        os.makedirs(settings.documents_dir, exist_ok=True)
        
        self.watcher = DocumentWatcher(
            settings.documents_dir,
            self.process_new_document
        )
        
    def start(self):
        """Start the agent and file watcher"""
        self._process_existing_documents()
        
        self.watcher.start()
        print(f"Study Agent initialized. Watching for new documents in {settings.documents_dir}")
        
    def stop(self):
        """Stop the agent and file watcher"""
        self.watcher.stop()
        
    def _process_existing_documents(self):
        """Process any existing documents in the documents directory"""
        for root, _, files in os.walk(settings.documents_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self.process_new_document(file_path)
                
    def process_new_document(self, file_path: str):
        """Process a new document and add it to the knowledge base"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in self.processors:
            print(f"Unsupported file type: {file_ext}")
            return
            
        print(f"Processing new document: {file_path}")
        
        processor = self.processors[file_ext]
        chunks = processor.process(file_path)
        
        metadata = [{
            "source": file_path,
            "chunk_idx": i
        } for i in range(len(chunks))]
        
        self.knowledge_base.add_texts(chunks, metadata)
        print(f"Added {len(chunks)} chunks to knowledge base from {file_path}")
        
    def chat(self, user_message: str) -> str:
        """Process a user message and return a response"""
        self.memory.add_user_message(user_message)
        
        context = self.knowledge_base.search(user_message)
        
        messages = [
            SystemMessage(content=(
                "You are a helpful study assistant. Use the provided context from the user's notes "
                "to answer their questions accurately. If the context doesn't contain the answer, "
                "just say you don't have enough information about that topic in your knowledge base."
            )),
            SystemMessage(content=f"Context from user's notes:\n\n{' '.join(context)}"),
        ]
        
        for msg in self.memory.get_conversation_history():
            if msg.role == "human":
                messages.append(HumanMessage(content=msg.content))
            else:
                messages.append(AIMessage(content=msg.content))
        
        response = self.llm.invoke(messages)
        
        self.memory.add_ai_message(response.content)
        
        return response.content 