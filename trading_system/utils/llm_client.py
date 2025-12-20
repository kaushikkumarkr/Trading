from typing import Optional, Literal
import os
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

LLMProvider = Literal["gemini", "groq", "openrouter"]

class LLMClient:
    """
    Unified client for LLM Rotation.
    Supports:
    - Gemini (Deep Reasoning)
    - Groq (Fast/Cheap)
    - OpenRouter (Universal Backup)
    """
    
    def __init__(self):
        self.google_key = os.getenv("GOOGLE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")

        # Configurable Defaults
        self.default_fast_model = "llama3-8b-8192" # Groq
        self.default_smart_model = "gemini-flash-latest" # Google (Stable, better quotas)
        
    def get_model(self, provider: LLMProvider = "gemini", model_name: Optional[str] = None, temperature: float = 0.0) -> BaseChatModel:
        """
        Returns a LangChain Chat Model based on provider.
        """
        
        # 1. Gemini (Default Smart)
        if provider == "gemini":
            if not self.google_key:
                raise ValueError("GOOGLE_API_KEY is missing")
            return ChatGoogleGenerativeAI(
                model=model_name or self.default_smart_model,
                temperature=temperature,
                google_api_key=self.google_key,
                convert_system_message_to_human=True 
            )

        # 2. Groq (Fast Inference)
        elif provider == "groq":
            if not self.groq_key:
                # Fallback to Gemini if Groq missing
                print("⚠️ Warning: GROQ_API_KEY missing, falling back to Gemini")
                return self.get_model("gemini", temperature=temperature)
                
            return ChatGroq(
                model_name=model_name or self.default_fast_model,
                temperature=temperature,
                groq_api_key=self.groq_key
            )

        # 3. OpenRouter (Universal / OpenAI Protocol)
        elif provider == "openrouter":
            if not self.openrouter_key:
                raise ValueError("OPENROUTER_API_KEY is missing")
                
            return ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_key,
                model=model_name or "openai/gpt-4o",
                temperature=temperature
            )
            
        else:
            raise ValueError(f"Unknown provider: {provider}")

# Singleton Instance
llm_client = LLMClient()
