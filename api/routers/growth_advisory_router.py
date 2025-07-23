"""
Growth Advisory Router for mornGPT Commercial API

Provides API endpoints for the Growth Advisory module with authentication, rate limiting, and billing.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any
import time
import uuid

from ..auth import get_current_user
from ..billing import billing_manager
from ..rate_limiter import rate_limiter
from ..models import (
    User, GrowthAdvisoryRequest, APIResponse, ErrorResponse
)

router = APIRouter()

@router.post("/analyze", response_model=APIResponse, summary="Analyze business growth opportunities")
async def analyze_growth_opportunities(
    request: GrowthAdvisoryRequest,
    current_user: User = Depends(get_current_user),
    http_request: Request = None
):
    """
    Analyze business growth opportunities and provide strategic advice.
    
    - **business_type**: Type of business
    - **target_market**: Target market description
    - **current_challenges**: Optional list of current challenges
    - **budget_range**: Optional budget range
    - **model_version**: AI model version (1-9)
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        # Check rate limits
        rate_limit_ok, rate_limit_info = rate_limiter.check_rate_limit(
            current_user.id, 
            current_user.plan
        )
        
        if not rate_limit_ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "rate_limit_info": rate_limit_info
                }
            )
        
        # Increment rate limit usage
        rate_limiter.increment_usage(current_user.id, "requests_per_minute")
        rate_limiter.increment_usage(current_user.id, "requests_per_hour")
        rate_limiter.increment_usage(current_user.id, "requests_per_day")
        
        # Import and use the actual Growth Advisory module
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
        
        from src.morngpt.modules.a_growth_advisory.growth_advisory import create_growth_advisory
        
        # Create growth advisory instance
        growth_advisor = create_growth_advisory(request.model_version)
        
        # Prepare parameters for the module
        parameters = {
            "business_type": request.business_type,
            "target_market": request.target_market,
            "current_challenges": request.current_challenges or [],
            "budget_range": request.budget_range,
            **request.parameters
        }
        
        # Call the growth advisory module
        result = growth_advisor.analyze_growth_opportunities(parameters)
        
        # Calculate processing time and cost
        processing_time = time.time() - start_time
        
        # Track usage for billing
        await billing_manager.track_usage(current_user.id, "growth_advisory", 1)
        
        return APIResponse(
            success=True,
            data=result,
            message="Growth analysis completed successfully",
            request_id=request_id,
            processing_time=processing_time,
            cost=0.02  # Base cost for growth advisory
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        return APIResponse(
            success=False,
            message=f"Growth analysis failed: {str(e)}",
            request_id=request_id,
            processing_time=processing_time
        )

@router.post("/market-research", response_model=APIResponse, summary="Conduct market research")
async def conduct_market_research(
    request: GrowthAdvisoryRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Conduct comprehensive market research for business growth.
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        # Check rate limits
        rate_limit_ok, rate_limit_info = rate_limiter.check_rate_limit(
            current_user.id, 
            current_user.plan
        )
        
        if not rate_limit_ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "rate_limit_info": rate_limit_info
                }
            )
        
        # Increment rate limit usage
        rate_limiter.increment_usage(current_user.id, "requests_per_minute")
        rate_limiter.increment_usage(current_user.id, "requests_per_hour")
        rate_limiter.increment_usage(current_user.id, "requests_per_day")
        
        # Import and use the actual Growth Advisory module
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
        
        from src.morngpt.modules.a_growth_advisory.growth_advisory import create_growth_advisory
        
        # Create growth advisory instance
        growth_advisor = create_growth_advisory(request.model_version)
        
        # Prepare parameters
        parameters = {
            "business_type": request.business_type,
            "target_market": request.target_market,
            "research_type": "market_analysis",
            **request.parameters
        }
        
        # Call the market research function
        result = growth_advisor.conduct_market_research(parameters)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Track usage for billing
        await billing_manager.track_usage(current_user.id, "growth_advisory", 1)
        
        return APIResponse(
            success=True,
            data=result,
            message="Market research completed successfully",
            request_id=request_id,
            processing_time=processing_time,
            cost=0.02
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        return APIResponse(
            success=False,
            message=f"Market research failed: {str(e)}",
            request_id=request_id,
            processing_time=processing_time
        )

@router.post("/strategy-development", response_model=APIResponse, summary="Develop growth strategy")
async def develop_growth_strategy(
    request: GrowthAdvisoryRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Develop a comprehensive growth strategy for the business.
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        # Check rate limits
        rate_limit_ok, rate_limit_info = rate_limiter.check_rate_limit(
            current_user.id, 
            current_user.plan
        )
        
        if not rate_limit_ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "rate_limit_info": rate_limit_info
                }
            )
        
        # Increment rate limit usage
        rate_limiter.increment_usage(current_user.id, "requests_per_minute")
        rate_limiter.increment_usage(current_user.id, "requests_per_hour")
        rate_limiter.increment_usage(current_user.id, "requests_per_day")
        
        # Import and use the actual Growth Advisory module
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
        
        from src.morngpt.modules.a_growth_advisory.growth_advisory import create_growth_advisory
        
        # Create growth advisory instance
        growth_advisor = create_growth_advisory(request.model_version)
        
        # Prepare parameters
        parameters = {
            "business_type": request.business_type,
            "target_market": request.target_market,
            "strategy_type": "growth_planning",
            **request.parameters
        }
        
        # Call the strategy development function
        result = growth_advisor.develop_growth_strategy(parameters)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Track usage for billing
        await billing_manager.track_usage(current_user.id, "growth_advisory", 1)
        
        return APIResponse(
            success=True,
            data=result,
            message="Growth strategy developed successfully",
            request_id=request_id,
            processing_time=processing_time,
            cost=0.02
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        return APIResponse(
            success=False,
            message=f"Strategy development failed: {str(e)}",
            request_id=request_id,
            processing_time=processing_time
        )

@router.get("/models", summary="Get available model versions")
async def get_available_models():
    """
    Get information about available Growth Advisory model versions.
    """
    return {
        "module": "growth_advisory",
        "available_versions": [
            {
                "version": 1,
                "name": "Basic Growth Advisory",
                "description": "Standard growth analysis and recommendations",
                "capabilities": ["Market analysis", "Basic strategy development", "Growth opportunities"]
            },
            {
                "version": 2,
                "name": "Improved Growth Advisory",
                "description": "Enhanced analysis with better accuracy",
                "capabilities": ["Advanced market research", "Competitive analysis", "Risk assessment"]
            },
            {
                "version": 3,
                "name": "Enhanced Growth Advisory",
                "description": "Advanced features and deeper insights",
                "capabilities": ["Predictive analytics", "Scenario planning", "ROI projections"]
            },
            {
                "version": 4,
                "name": "Premium Growth Advisory",
                "description": "High-quality strategic planning",
                "capabilities": ["Custom strategies", "Implementation roadmaps", "Performance tracking"]
            },
            {
                "version": 5,
                "name": "Expert Growth Advisory",
                "description": "Professional-grade strategic consulting",
                "capabilities": ["Industry-specific insights", "Advanced forecasting", "Strategic partnerships"]
            },
            {
                "version": 6,
                "name": "Master Growth Advisory",
                "description": "Elite strategic planning capabilities",
                "capabilities": ["Global market analysis", "Innovation strategies", "Disruption planning"]
            },
            {
                "version": 7,
                "name": "Ultimate Growth Advisory",
                "description": "Top-tier strategic consulting",
                "capabilities": ["AI-powered insights", "Real-time market monitoring", "Predictive modeling"]
            },
            {
                "version": 8,
                "name": "Perfect Growth Advisory",
                "description": "Near-flawless strategic planning",
                "capabilities": ["Perfect market timing", "Optimal resource allocation", "Maximum ROI strategies"]
            },
            {
                "version": 9,
                "name": "Best Growth Advisory",
                "description": "Optimal strategic planning performance",
                "capabilities": ["Revolutionary strategies", "Market disruption", "Unlimited growth potential"]
            }
        ],
        "pricing": {
            "base_cost_per_call": 0.02,
            "version_multipliers": {
                1: 1.0,
                2: 1.2,
                3: 1.5,
                4: 2.0,
                5: 2.5,
                6: 3.0,
                7: 4.0,
                8: 5.0,
                9: 6.0
            }
        }
    } 