"""
mornGPT Commercial API Server

A comprehensive API system for commercializing mornGPT modules with:
- Authentication and authorization
- Rate limiting and billing
- API key management
- Usage tracking and analytics
- Multiple pricing tiers
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import hashlib
import secrets

# Import our modules
from .auth import AuthManager, get_current_user
from .billing import BillingManager
from .rate_limiter import RateLimiter
from .models import (
    User, APIKey, UsageStats, BillingPlan,
    APIRequest, APIResponse, ErrorResponse
)
from .routers import (
    auth_router, billing_router, analytics_router,
    growth_advisory_router, interview_job_router, coder_router,
    content_detection_router, medical_advice_router, multi_gpt_router,
    housing_router, person_matching_router, teacher_coach_router,
    traveling_router, product_search_router, clothing_router,
    restaurant_food_router, content_generation_router, anti_ai_protection_router
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="mornGPT Commercial API",
    description="Commercial API for mornGPT AI modules with billing and rate limiting",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
auth_manager = AuthManager()
billing_manager = BillingManager()
rate_limiter = RateLimiter()

# Security
security = HTTPBearer()

# Pricing tiers (per API call)
PRICING_TIERS = {
    "free": {
        "monthly_calls": 100,
        "price_per_call": 0.00,
        "features": ["Basic API access", "Standard response time"]
    },
    "starter": {
        "monthly_calls": 1000,
        "price_per_call": 0.01,
        "features": ["Priority support", "Faster response time", "Basic analytics"]
    },
    "professional": {
        "monthly_calls": 10000,
        "price_per_call": 0.005,
        "features": ["Premium support", "Fastest response time", "Advanced analytics", "Custom integrations"]
    },
    "enterprise": {
        "monthly_calls": 100000,
        "price_per_call": 0.002,
        "features": ["Dedicated support", "Custom rate limits", "White-label solutions", "SLA guarantees"]
    }
}

# Module pricing (additional cost per call)
MODULE_PRICING = {
    "growth_advisory": 0.02,
    "interview_job": 0.015,
    "coder": 0.025,
    "content_detection": 0.03,
    "medical_advice": 0.04,
    "multi_gpt": 0.035,
    "housing": 0.02,
    "person_matching": 0.025,
    "teacher_coach": 0.02,
    "traveling": 0.02,
    "product_search": 0.015,
    "clothing": 0.02,
    "restaurant_food": 0.02,
    "content_generation": 0.05,
    "anti_ai_protection": 0.10  # Premium safety feature
}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time and track API usage"""
    start_time = time.time()
    
    # Track API usage
    if request.url.path.startswith("/api/"):
        await track_api_usage(request)
    
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

async def track_api_usage(request: Request):
    """Track API usage for billing and analytics"""
    try:
        # Extract API key from headers
        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not api_key:
            return
        
        # Get user from API key
        user = auth_manager.get_user_by_api_key(api_key)
        if not user:
            return
        
        # Track usage
        module = request.url.path.split("/")[2] if len(request.url.path.split("/")) > 2 else "unknown"
        await billing_manager.track_usage(user.id, module, 1)
        
    except Exception as e:
        logger.error(f"Error tracking API usage: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to mornGPT Commercial API",
        "version": "1.0.0",
        "modules": list(MODULE_PRICING.keys()),
        "pricing_tiers": list(PRICING_TIERS.keys()),
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "auth": "operational",
            "billing": "operational",
            "rate_limiter": "operational"
        }
    }

@app.get("/pricing")
async def get_pricing():
    """Get current pricing information"""
    return {
        "pricing_tiers": PRICING_TIERS,
        "module_pricing": MODULE_PRICING,
        "currency": "USD",
        "billing_cycle": "monthly"
    }

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(billing_router, prefix="/api/billing", tags=["Billing"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])

# Include module routers
app.include_router(growth_advisory_router, prefix="/api/growth_advisory", tags=["Growth Advisory"])
app.include_router(interview_job_router, prefix="/api/interview_job", tags=["Interview/Job"])
app.include_router(coder_router, prefix="/api/coder", tags=["AI Coder"])
app.include_router(content_detection_router, prefix="/api/content_detection", tags=["Content Detection"])
app.include_router(medical_advice_router, prefix="/api/medical_advice", tags=["Medical Advice"])
app.include_router(multi_gpt_router, prefix="/api/multi_gpt", tags=["Multi-GPT"])
app.include_router(housing_router, prefix="/api/housing", tags=["Personalized Housing"])
app.include_router(person_matching_router, prefix="/api/person_matching", tags=["Person Matching"])
app.include_router(teacher_coach_router, prefix="/api/teacher_coach", tags=["Teacher/Coach"])
app.include_router(traveling_router, prefix="/api/traveling", tags=["Personalized Traveling"])
app.include_router(product_search_router, prefix="/api/product_search", tags=["Product Search"])
app.include_router(clothing_router, prefix="/api/clothing", tags=["Personalized Clothing"])
app.include_router(restaurant_food_router, prefix="/api/restaurant_food", tags=["Restaurant/Food"])
app.include_router(content_generation_router, prefix="/api/content_generation", tags=["Content Generation"])
app.include_router(anti_ai_protection_router, prefix="/api/anti_ai_protection", tags=["Anti-AI Protection"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 