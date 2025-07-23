"""
FastAPI Backend for mornGPT with Free AI Client Integration
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
import os
import sys

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from morngpt.clients.free_ai_client import FreeAIClient, generate_ai_response, AIResponse

app = FastAPI(
    title="mornGPT API",
    description="Multi-Module AI System with Free AI Client Integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Free AI Client
ai_client = FreeAIClient()

# Pydantic models
class GenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    budget: str = "free_local"
    max_tokens: int = 1000
    temperature: float = 0.7

class GenerateResponse(BaseModel):
    content: str
    model: str
    provider: str
    cost: float
    tokens_used: int
    response_time: float
    success: bool
    error: Optional[str] = None

class ModelInfo(BaseModel):
    name: str
    model: str
    cost: float
    provider: str

class UsageStats(BaseModel):
    total_requests: int
    total_cost: float
    models_used: List[str]
    providers_used: List[str]

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "mornGPT API with Free AI Client",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/api/v1/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Generate AI response using any available model
    
    Args:
        request: Generation request with prompt and parameters
        
    Returns:
        Standardized AI response
    """
    try:
        response = ai_client.generate(
            prompt=request.prompt,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            budget=request.budget
        )
        
        return GenerateResponse(
            content=response.content,
            model=response.model,
            provider=response.provider,
            cost=response.cost,
            tokens_used=response.tokens_used,
            response_time=response.response_time,
            success=response.success,
            error=response.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/models", response_model=List[ModelInfo])
async def get_models(budget: Optional[str] = None):
    """
    Get available models for specified budget tier
    
    Args:
        budget: Budget tier (free_local, free_api, ultra_cheap, cheap)
        
    Returns:
        List of available models
    """
    try:
        models = ai_client.get_available_models(budget)
        return [ModelInfo(**model) for model in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/usage", response_model=UsageStats)
async def get_usage_stats():
    """
    Get usage statistics
    
    Returns:
        Usage statistics
    """
    try:
        stats = ai_client.get_usage_stats()
        return UsageStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

# mornGPT Integration Routes
@app.post("/api/v1/morngpt/h1/orchestrate")
async def h1_orchestrate(request: Dict[str, Any]):
    """
    H1 Prompt Orchestration with Free AI Client
    """
    try:
        prompt = request.get('prompt', '')
        models = request.get('models', ['ollama/llama3.1:8b'])
        strategy = request.get('strategy', 'parallel')
        complexity = request.get('complexity', 'medium')
        model_version = request.get('model_version', 1)
        
        # Use the first available model
        model = models[0] if models else 'ollama/llama3.1:8b'
        
        # Generate response using free AI client
        response = ai_client.generate(
            prompt=prompt,
            model=model,
            budget="free_local" if model_version <= 3 else "ultra_cheap",
            max_tokens=1000
        )
        
        return {
            'orchestrated_prompt': response.content,
            'model_coordination': {
                'primary_model': model,
                'secondary_models': models[1:] if len(models) > 1 else [],
                'strategy': strategy,
                'estimated_tokens': response.tokens_used
            },
            'quality_metrics': {
                'coherence_score': 0.85 if response.success else 0.5,
                'complexity_handling': model_version >= 5,
                'multi_model_sync': len(models) > 1
            },
            'api_usage': {
                'endpoint': '/api/v1/morngpt/h1/orchestrate',
                'rate_limit': '1000 requests/hour',
                'cost_per_request': response.cost,
                'subscription_tier': 'Free' if response.cost == 0 else 'Ultra-Cheap'
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/morngpt/h1/chain")
async def h1_chain(request: Dict[str, Any]):
    """
    H1 Prompt Chaining with Free AI Client
    """
    try:
        prompts = request.get('prompts', [])
        chain_type = request.get('chain_type', 'sequential')
        output_format = request.get('output_format', 'json')
        model_version = request.get('model_version', 1)
        
        chained_prompts = []
        total_cost = 0.0
        
        for i, prompt in enumerate(prompts):
            # Generate response for each prompt
            response = ai_client.generate(
                prompt=prompt,
                budget="free_local" if model_version <= 3 else "ultra_cheap",
                max_tokens=500
            )
            
            chained_prompts.append(response.content)
            total_cost += response.cost
        
        return {
            'chained_prompts': chained_prompts,
            'chain_configuration': {
                'type': chain_type,
                'prompt_count': len(prompts),
                'output_format': output_format,
                'estimated_steps': len(prompts)
            },
            'api_usage': {
                'endpoint': '/api/v1/morngpt/h1/chain',
                'rate_limit': '500 requests/hour',
                'cost_per_request': total_cost,
                'subscription_tier': 'Free' if total_cost == 0 else 'Ultra-Cheap'
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/morngpt/h1/optimize")
async def h1_optimize(request: Dict[str, Any]):
    """
    H1 Prompt Optimization with Free AI Client
    """
    try:
        original_prompt = request.get('prompt', '')
        optimization_goal = request.get('optimization_goal', 'performance')
        target_model = request.get('target_model', 'ollama/llama3.1:8b')
        model_version = request.get('model_version', 1)
        
        # Create optimization prompt
        optimization_prompt = f"""
        Optimize the following prompt for {optimization_goal}:
        
        Original: {original_prompt}
        
        Please provide an optimized version that is more {optimization_goal}.
        """
        
        # Generate optimized prompt
        response = ai_client.generate(
            prompt=optimization_prompt,
            model=target_model,
            budget="free_local" if model_version <= 3 else "ultra_cheap",
            max_tokens=500
        )
        
        # Calculate token reduction
        original_tokens = len(original_prompt.split())
        optimized_tokens = len(response.content.split())
        token_reduction = ((original_tokens - optimized_tokens) / original_tokens * 100) if original_tokens > 0 else 0
        
        return {
            'original_prompt': original_prompt,
            'optimized_prompt': response.content,
            'optimization_metrics': {
                'token_reduction': round(token_reduction, 2),
                'performance_improvement': 0.85 if response.success else 0.5,
                'cost_savings': response.cost * 0.3  # Estimated savings
            },
            'api_usage': {
                'endpoint': '/api/v1/morngpt/h1/optimize',
                'rate_limit': '2000 requests/hour',
                'cost_per_request': response.cost,
                'subscription_tier': 'Free' if response.cost == 0 else 'Ultra-Cheap'
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "detail": str(exc)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": str(exc)}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 