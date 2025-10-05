"""
Model provider module for Ollama integration.
This module is complete - students should NOT modify.
"""

import json
import logging
import time
import os
from typing import Dict, List, Optional

from openai import OpenAI, APIError
from dotenv import load_dotenv

load_dotenv()

from .config import (
    MODEL_ENDPOINT,
    MODEL_NAME,
    TIMEOUT_SECONDS,
    get_model_config,
)

logger = logging.getLogger(__name__)


class ModelProvider:
    """Handles communication with Ollama API."""
    
    def __init__(self):
        """Initialize the model provider with retry logic."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable not found. "
                "Please set it in your environment or in a .env file."
            )
        
        # initialize OpenAI Client
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = MODEL_NAME
        
        logger.info(f"Successfully configured ModelProvider for {MODEL_ENDPOINT} using model {self.model_name}")
        self._verify_connection()

    def _verify_connection(self):
        """Verify openai is running and model is available."""
        try:
            self.client.models.retrieve(self.model_name)
            logger.info(f"Model '{self.model_name}' is accessible via OpenAI API.")
        except APIError as e:
            if e.status_code == 404:
                raise RuntimeError(f"Model '{self.model_name}' not found or inaccessible. Check model name.")
            if e.status_code == 401:
                raise RuntimeError("OpenAI API Key is invalid or expired (401 error).")
            raise RuntimeError(f"Failed to verify OpenAI connection: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to verify OpenAI connection: {e}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
        **kwargs
    ) -> Dict:
        """
        Generate response from the model.
        
        Args:
            prompt: User input prompt
            system_prompt: System prompt for behavior
            conversation_history: Previous conversation turns
            **kwargs: Additional parameters to override defaults
            
        Returns:
            Dict containing response and metadata
        """
        start_time = time.time()
        
        # Prepare the full prompt
        full_prompt = self._build_prompt(prompt, system_prompt, conversation_history)
        
        # Get model configuration
        config = get_model_config()
        
        # Override with any provided kwargs
        if kwargs:
            config["options"].update(kwargs)
        
        # Prepare request
        api_params = {
            "model": config["model"],
            "messages": full_prompt,
            "temperature": config["temperature"],
            "top_p": config["top_p"],
            "max_tokens": config["max_tokens"],
            "seed": config["seed"],
            "timeout": TIMEOUT_SECONDS,
            **kwargs # Apply any additional overrides
        }
        
        try:
            logger.debug(f"Sending request to OpenAI with parameters: {api_params}")
            
            # 4. API Call
            completion = self.client.chat.completions.create(**api_params)
            
            response_text = completion.choices[0].message.content
            
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            return {
                "response": response_text,
                "model": completion.model,
                "created_at": str(completion.created),
                "done": True,
                "latency_ms": elapsed_ms,
                "deterministic": api_params["temperature"] == 0,
            }
            
        except APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise RuntimeError(f"OpenAI API Error: {e}")
        except Exception as e:
            logger.error(f"Model generation failed: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")
    
    def _build_prompt(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
    ) -> List[Dict]:
        """
        Build full prompt with system prompt and conversation history.
        
        Args:
            user_prompt: Current user input
            system_prompt: System instructions
            conversation_history: List of previous turns
            
        Returns:
            List of messages (Dicts)
        """
        parts = []
        
        # Add system prompt if provided
        if system_prompt:
            parts.append({"role": "system", "content": system_prompt})
        
        # Add conversation history if provided
        if conversation_history:
            parts.extend(conversation_history)
        
        # Add current user prompt
        parts.append({"role": "user", "content": user_prompt})
        
        return parts
    
    def health_check(self) -> bool:
        """
        Check if model provider is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            self.client.models.retrieve(self.model_name)
            return True
        except:
            return False


# Singleton instance
_provider_instance = None


def get_provider() -> ModelProvider:
    """Get or create singleton model provider instance."""
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = ModelProvider()
    return _provider_instance