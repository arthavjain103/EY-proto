from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

class BaseAgent(ABC):
    """Base class for all AI agents in the system"""
    
    def __init__(self, agent_name: str, system_prompt: str):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        api_key = os.getenv('OPENAI_API_KEY', '')
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            openai_api_key=api_key
        ) if api_key else None
    
    @abstractmethod
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process the given context and return results"""
        pass
    
    def _call_llm(self, user_message: str, additional_context: Optional[str] = None) -> str:
        """Helper method to call LLM with system and user messages"""
        if not self.llm:
            return "LLM not configured. Please set OPENAI_API_KEY."
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message)
        ]
        
        if additional_context:
            messages.insert(1, HumanMessage(content=f"Additional Context: {additional_context}"))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def log_action(self, action: str, details: Dict[str, Any]):
        """Log agent actions for audit trail"""
        print(f"[{self.agent_name}] {action}: {details}")

