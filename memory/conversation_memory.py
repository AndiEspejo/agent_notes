from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ConversationManager:
    def __init__(self, max_tokens: int = 4000):
        self.messages = []
        self.max_tokens = max_tokens
        
    def add_user_message(self, message: str) -> None:
        """Add a user message to the conversation history"""
        self.messages.append(HumanMessage(content=message))
        self._trim_memory_if_needed()
        
    def add_ai_message(self, message: str) -> None:
        """Add an AI message to the conversation history"""
        self.messages.append(AIMessage(content=message))
        self._trim_memory_if_needed()
        
    def get_conversation_history(self) -> List[Message]:
        """Get the full conversation history"""
        return [
            Message(role="human" if isinstance(msg, HumanMessage) else "ai", content=msg.content)
            for msg in self.messages
        ]
        
    def _trim_memory_if_needed(self) -> None:
        """Trim the memory if it exceeds the max token limit"""
        while self._estimate_token_count() > self.max_tokens and len(self.messages) > 2:
            self.messages.pop(0)
            
    def _estimate_token_count(self) -> int:
        """Estimate the token count in the current memory"""
        # Rough estimation: 4 chars ≈ 1 token
        return sum(len(msg.content) // 4 for msg in self.messages) 