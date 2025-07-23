"""
Free AI Client - Unified interface for all free and low-cost AI APIs
Supports Ollama, Hugging Face, Google Colab, and commercial APIs with free tiers
"""

import requests
import json
import time
import os
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import subprocess
import google.generativeai as genai
import anthropic
from huggingface_hub import InferenceClient


class AIModel(Enum):
    """Available AI models across different providers"""
    # Free Local Models (Ollama)
    OLLAMA_LLAMA_3_1 = "ollama/llama3.1:8b"
    OLLAMA_MISTRAL = "ollama/mistral:7b"
    OLLAMA_CODELLAMA = "ollama/codellama:7b"
    OLLAMA_PHI_3 = "ollama/phi3:mini"
    
    # Free API Models
    HUGGINGFACE_MISTRAL = "mistralai/Mistral-7B-Instruct-v0.2"
    HUGGINGFACE_LLAMA = "meta-llama/Llama-2-7b-chat-hf"
    HUGGINGFACE_CODEGEN = "Salesforce/codegen-350M-mono"
    
    # Ultra-Cheap Commercial APIs
    GEMINI_FLASH = "gemini-1.5-flash"
    CLAUDE_HAIKU = "claude-3-5-haiku-20241022"
    MISTRAL_MEDIUM = "mistral-medium"
    
    # Free Tier Commercial APIs
    OPENAI_GPT35 = "gpt-3.5-turbo"
    COHERE_COMMAND_R = "command-r"


@dataclass
class AIResponse:
    """Standardized response format"""
    content: str
    model: str
    provider: str
    cost: float
    tokens_used: int
    response_time: float
    success: bool
    error: Optional[str] = None


class FreeAIClient:
    """
    Unified client for all free and low-cost AI APIs
    Supports local models, free APIs, and ultra-cheap commercial APIs
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Free AI Client
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config or {}
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY', self.config.get('openai_key')),
            'anthropic': os.getenv('ANTHROPIC_API_KEY', self.config.get('anthropic_key')),
            'google': os.getenv('GOOGLE_API_KEY', self.config.get('google_key')),
            'huggingface': os.getenv('HUGGINGFACE_API_KEY', self.config.get('huggingface_key')),
            'cohere': os.getenv('COHERE_API_KEY', self.config.get('cohere_key')),
            'mistral': os.getenv('MISTRAL_API_KEY', self.config.get('mistral_key'))
        }
        
        # Initialize API clients
        self._init_clients()
        
        # Model routing configuration
        self.model_routing = {
            'free_local': [AIModel.OLLAMA_LLAMA_3_1, AIModel.OLLAMA_MISTRAL],
            'free_api': [AIModel.HUGGINGFACE_MISTRAL, AIModel.HUGGINGFACE_LLAMA],
            'ultra_cheap': [AIModel.GEMINI_FLASH, AIModel.CLAUDE_HAIKU],
            'cheap': [AIModel.MISTRAL_MEDIUM, AIModel.OPENAI_GPT35]
        }
    
    def _init_clients(self):
        """Initialize API clients"""
        # Google Gemini
        if self.api_keys['google']:
            genai.configure(api_key=self.api_keys['google'])
        
        # Anthropic Claude
        if self.api_keys['anthropic']:
            self.anthropic_client = anthropic.Anthropic(api_key=self.api_keys['anthropic'])
        
        # Hugging Face
        if self.api_keys['huggingface']:
            self.hf_client = InferenceClient(token=self.api_keys['huggingface'])
    
    def generate(
        self,
        prompt: str,
        model: Optional[Union[str, AIModel]] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        budget: str = "free_local",
        fallback: bool = True
    ) -> AIResponse:
        """
        Generate AI response using any available model
        
        Args:
            prompt: Input prompt
            model: Specific model to use (optional)
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0-1.0)
            budget: Budget tier ('free_local', 'free_api', 'ultra_cheap', 'cheap')
            fallback: Whether to fallback to cheaper models on failure
            
        Returns:
            AIResponse object with standardized format
        """
        start_time = time.time()
        
        # Determine model to use
        if model:
            target_model = AIModel(model) if isinstance(model, str) else model
        else:
            target_model = self._select_model(budget)
        
        try:
            # Route to appropriate provider
            if target_model.value.startswith('ollama/'):
                response = self._call_ollama(prompt, target_model, max_tokens, temperature)
            elif target_model.value.startswith('mistralai/') or target_model.value.startswith('meta-llama/'):
                response = self._call_huggingface(prompt, target_model, max_tokens, temperature)
            elif target_model == AIModel.GEMINI_FLASH:
                response = self._call_gemini(prompt, target_model, max_tokens, temperature)
            elif target_model == AIModel.CLAUDE_HAIKU:
                response = self._call_claude(prompt, target_model, max_tokens, temperature)
            elif target_model == AIModel.MISTRAL_MEDIUM:
                response = self._call_mistral(prompt, target_model, max_tokens, temperature)
            elif target_model == AIModel.OPENAI_GPT35:
                response = self._call_openai(prompt, target_model, max_tokens, temperature)
            else:
                raise ValueError(f"Unsupported model: {target_model}")
            
            response.response_time = time.time() - start_time
            return response
            
        except Exception as e:
            if fallback and budget != "free_local":
                # Try fallback to cheaper model
                fallback_budget = self._get_fallback_budget(budget)
                if fallback_budget != budget:
                    return self.generate(prompt, budget=fallback_budget, fallback=False)
            
            return AIResponse(
                content="",
                model=target_model.value,
                provider=self._get_provider(target_model),
                cost=0.0,
                tokens_used=0,
                response_time=time.time() - start_time,
                success=False,
                error=str(e)
            )
    
    def _select_model(self, budget: str) -> AIModel:
        """Select model based on budget"""
        available_models = self.model_routing.get(budget, [AIModel.OLLAMA_LLAMA_3_1])
        return available_models[0]
    
    def _get_fallback_budget(self, current_budget: str) -> str:
        """Get fallback budget tier"""
        fallback_map = {
            'cheap': 'ultra_cheap',
            'ultra_cheap': 'free_api',
            'free_api': 'free_local',
            'free_local': 'free_local'
        }
        return fallback_map.get(current_budget, 'free_local')
    
    def _get_provider(self, model: AIModel) -> str:
        """Get provider name for model"""
        if model.value.startswith('ollama/'):
            return 'ollama'
        elif model.value.startswith('mistralai/') or model.value.startswith('meta-llama/'):
            return 'huggingface'
        elif model == AIModel.GEMINI_FLASH:
            return 'google'
        elif model == AIModel.CLAUDE_HAIKU:
            return 'anthropic'
        elif model == AIModel.MISTRAL_MEDIUM:
            return 'mistral'
        elif model == AIModel.OPENAI_GPT35:
            return 'openai'
        else:
            return 'unknown'
    
    def _call_ollama(self, prompt: str, model: AIModel, max_tokens: int, temperature: float) -> AIResponse:
        """Call Ollama local model"""
        try:
            # Extract model name from enum
            model_name = model.value.replace('ollama/', '')
            
            # Call Ollama via subprocess
            cmd = [
                'ollama', 'run', model_name,
                f'--temperature {temperature}',
                f'--num-predict {max_tokens}',
                prompt
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return AIResponse(
                    content=result.stdout.strip(),
                    model=model.value,
                    provider='ollama',
                    cost=0.0,
                    tokens_used=len(prompt.split()) + len(result.stdout.split()),
                    response_time=0.0,
                    success=True
                )
            else:
                raise Exception(f"Ollama error: {result.stderr}")
                
        except Exception as e:
            raise Exception(f"Ollama call failed: {str(e)}")
    
    def _call_huggingface(self, prompt: str, model: AIModel, max_tokens: int, temperature: float) -> AIResponse:
        """Call Hugging Face model"""
        if not self.api_keys['huggingface']:
            raise Exception("Hugging Face API key required")
        
        try:
            response = self.hf_client.text_generation(
                prompt,
                model=model.value,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True
            )
            
            return AIResponse(
                content=response,
                model=model.value,
                provider='huggingface',
                cost=0.0,  # Free tier
                tokens_used=len(prompt.split()) + len(response.split()),
                response_time=0.0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Hugging Face call failed: {str(e)}")
    
    def _call_gemini(self, prompt: str, model: AIModel, max_tokens: int, temperature: float) -> AIResponse:
        """Call Google Gemini API"""
        if not self.api_keys['google']:
            raise Exception("Google API key required")
        
        try:
            genai_model = genai.GenerativeModel('gemini-1.5-flash')
            response = genai_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            return AIResponse(
                content=response.text,
                model=model.value,
                provider='google',
                cost=self._calculate_gemini_cost(prompt, response.text),
                tokens_used=len(prompt.split()) + len(response.text.split()),
                response_time=0.0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Gemini call failed: {str(e)}")
    
    def _call_claude(self, prompt: str, model: AIModel, max_tokens: int, temperature: float) -> AIResponse:
        """Call Anthropic Claude API"""
        if not self.api_keys['anthropic']:
            raise Exception("Anthropic API key required")
        
        try:
            response = self.anthropic_client.messages.create(
                model=model.value,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return AIResponse(
                content=response.content[0].text,
                model=model.value,
                provider='anthropic',
                cost=self._calculate_claude_cost(prompt, response.content[0].text),
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                response_time=0.0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Claude call failed: {str(e)}")
    
    def _call_mistral(self, prompt: str, model: AIModel, max_tokens: int, temperature: float) -> AIResponse:
        """Call Mistral AI API"""
        if not self.api_keys['mistral']:
            raise Exception("Mistral API key required")
        
        try:
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_keys['mistral']}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mistral-medium",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            return AIResponse(
                content=content,
                model=model.value,
                provider='mistral',
                cost=self._calculate_mistral_cost(prompt, content),
                tokens_used=result['usage']['total_tokens'],
                response_time=0.0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Mistral call failed: {str(e)}")
    
    def _call_openai(self, prompt: str, model: AIModel, max_tokens: int, temperature: float) -> AIResponse:
        """Call OpenAI API (free tier)"""
        if not self.api_keys['openai']:
            raise Exception("OpenAI API key required")
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_keys['openai']}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            return AIResponse(
                content=content,
                model=model.value,
                provider='openai',
                cost=self._calculate_openai_cost(prompt, content),
                tokens_used=result['usage']['total_tokens'],
                response_time=0.0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"OpenAI call failed: {str(e)}")
    
    def _calculate_gemini_cost(self, prompt: str, response: str) -> float:
        """Calculate Gemini API cost"""
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3
        return (input_tokens * 0.000075 + output_tokens * 0.0003) / 1000
    
    def _calculate_claude_cost(self, prompt: str, response: str) -> float:
        """Calculate Claude API cost"""
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3
        return (input_tokens * 0.00025 + output_tokens * 0.00125) / 1000
    
    def _calculate_mistral_cost(self, prompt: str, response: str) -> float:
        """Calculate Mistral API cost"""
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3
        return (input_tokens * 0.0024 + output_tokens * 0.008) / 1000
    
    def _calculate_openai_cost(self, prompt: str, response: str) -> float:
        """Calculate OpenAI API cost"""
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = len(response.split()) * 1.3
        return (input_tokens * 0.0005 + output_tokens * 0.0015) / 1000
    
    def get_available_models(self, budget: str = None) -> List[Dict[str, Any]]:
        """Get list of available models"""
        models = []
        
        if budget is None or budget == "free_local":
            models.extend([
                {"name": "Llama 3.1", "model": AIModel.OLLAMA_LLAMA_3_1.value, "cost": 0.0, "provider": "ollama"},
                {"name": "Mistral 7B", "model": AIModel.OLLAMA_MISTRAL.value, "cost": 0.0, "provider": "ollama"},
                {"name": "CodeLlama", "model": AIModel.OLLAMA_CODELLAMA.value, "cost": 0.0, "provider": "ollama"}
            ])
        
        if budget is None or budget in ["free_api", "free_local"]:
            models.extend([
                {"name": "Mistral 7B (HF)", "model": AIModel.HUGGINGFACE_MISTRAL.value, "cost": 0.0, "provider": "huggingface"},
                {"name": "Llama 2 (HF)", "model": AIModel.HUGGINGFACE_LLAMA.value, "cost": 0.0, "provider": "huggingface"}
            ])
        
        if budget is None or budget in ["ultra_cheap", "free_api", "free_local"]:
            models.extend([
                {"name": "Gemini 1.5 Flash", "model": AIModel.GEMINI_FLASH.value, "cost": 0.000075, "provider": "google"},
                {"name": "Claude 3.5 Haiku", "model": AIModel.CLAUDE_HAIKU.value, "cost": 0.00025, "provider": "anthropic"}
            ])
        
        if budget is None or budget in ["cheap", "ultra_cheap", "free_api", "free_local"]:
            models.extend([
                {"name": "Mistral Medium", "model": AIModel.MISTRAL_MEDIUM.value, "cost": 0.0024, "provider": "mistral"},
                {"name": "GPT-3.5 Turbo", "model": AIModel.OPENAI_GPT35.value, "cost": 0.0005, "provider": "openai"}
            ])
        
        return models
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_requests": 0,  # Would track in production
            "total_cost": 0.0,
            "models_used": [],
            "providers_used": []
        }


# Convenience function for easy usage
def generate_ai_response(
    prompt: str,
    model: Optional[str] = None,
    budget: str = "free_local",
    max_tokens: int = 1000,
    temperature: float = 0.7,
    config: Optional[Dict[str, Any]] = None
) -> AIResponse:
    """
    Convenience function to generate AI response
    
    Args:
        prompt: Input prompt
        model: Specific model to use (optional)
        budget: Budget tier
        max_tokens: Maximum tokens to generate
        temperature: Creativity level
        config: API configuration
        
    Returns:
        AIResponse object
    """
    client = FreeAIClient(config)
    return client.generate(prompt, model, max_tokens, temperature, budget)


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = FreeAIClient()
    
    # Example 1: Free local generation
    print("=== Free Local Generation ===")
    response = client.generate(
        "Write a Python function to calculate fibonacci numbers",
        budget="free_local"
    )
    print(f"Response: {response.content[:100]}...")
    print(f"Cost: ${response.cost:.6f}")
    print(f"Provider: {response.provider}")
    
    # Example 2: Ultra-cheap API generation
    print("\n=== Ultra-Cheap API Generation ===")
    response = client.generate(
        "Explain quantum computing in simple terms",
        budget="ultra_cheap"
    )
    print(f"Response: {response.content[:100]}...")
    print(f"Cost: ${response.cost:.6f}")
    print(f"Provider: {response.provider}")
    
    # Example 3: Get available models
    print("\n=== Available Models ===")
    models = client.get_available_models("free_local")
    for model in models:
        print(f"- {model['name']}: ${model['cost']:.6f}/1K tokens") 