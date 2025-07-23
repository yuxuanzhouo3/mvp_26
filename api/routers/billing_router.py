"""
Billing Router for mornGPT Commercial API

Handles billing, usage tracking, and payment endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timedelta

from ..auth import get_current_user
from ..billing import billing_manager
from ..models import (
    User, BillingResponse, AnalyticsRequest, AnalyticsResponse
)

router = APIRouter()

@router.get("/usage", response_model=BillingResponse, summary="Get usage statistics")
async def get_usage_stats(
    start_date: Optional[datetime] = Query(None, description="Start date for usage period"),
    end_date: Optional[datetime] = Query(None, description="End date for usage period"),
    current_user: User = Depends(get_current_user)
):
    """
    Get usage statistics for the authenticated user.
    
    - **start_date**: Optional start date for the usage period
    - **end_date**: Optional end date for the usage period
    """
    try:
        usage_stats = billing_manager.get_user_usage(
            current_user.id, 
            start_date=start_date, 
            end_date=end_date
        )
        return BillingResponse(**usage_stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage stats: {str(e)}"
        )

@router.get("/current-cycle", summary="Get current billing cycle")
async def get_current_billing_cycle(current_user: User = Depends(get_current_user)):
    """
    Get information about the current billing cycle.
    """
    try:
        cycle = billing_manager.get_current_billing_cycle(current_user.id)
        if not cycle:
            # Create a new billing cycle if none exists
            cycle_id = billing_manager.create_billing_cycle(current_user.id, current_user.plan)
            cycle = billing_manager.get_current_billing_cycle(current_user.id)
        
        return cycle
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve billing cycle: {str(e)}"
        )

@router.get("/bill/{cycle_id}", summary="Calculate bill for billing cycle")
async def calculate_bill(
    cycle_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Calculate the bill for a specific billing cycle.
    
    - **cycle_id**: ID of the billing cycle
    """
    try:
        bill = billing_manager.calculate_bill(current_user.id, cycle_id)
        return bill
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate bill: {str(e)}"
        )

@router.post("/pay", summary="Process payment")
async def process_payment(
    amount: float = Query(..., gt=0, description="Payment amount"),
    payment_method: str = Query("credit_card", description="Payment method"),
    current_user: User = Depends(get_current_user)
):
    """
    Process a payment for the authenticated user.
    
    - **amount**: Payment amount
    - **payment_method**: Payment method (credit_card, paypal, etc.)
    """
    try:
        payment = billing_manager.process_payment(
            current_user.id, 
            amount, 
            payment_method
        )
        return payment
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment processing failed: {str(e)}"
        )

@router.get("/payments", summary="Get payment history")
async def get_payment_history(
    limit: int = Query(10, ge=1, le=100, description="Number of payments to retrieve"),
    current_user: User = Depends(get_current_user)
):
    """
    Get payment history for the authenticated user.
    
    - **limit**: Number of payments to retrieve (1-100)
    """
    try:
        payments = billing_manager.get_payment_history(current_user.id, limit)
        return payments
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve payment history: {str(e)}"
        )

@router.post("/upgrade", summary="Upgrade plan")
async def upgrade_plan(
    new_plan: str = Query(..., description="New plan to upgrade to"),
    current_user: User = Depends(get_current_user)
):
    """
    Upgrade the user's plan.
    
    - **new_plan**: New plan to upgrade to (free, starter, professional, enterprise)
    """
    try:
        success = billing_manager.upgrade_plan(current_user.id, new_plan)
        if success:
            return {"message": f"Successfully upgraded to {new_plan} plan"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to upgrade plan"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plan upgrade failed: {str(e)}"
        )

@router.get("/pricing", summary="Get pricing information")
async def get_pricing():
    """
    Get current pricing information for all plans and modules.
    """
    from ..billing import PRICING_TIERS, MODULE_PRICING
    
    return {
        "pricing_tiers": PRICING_TIERS,
        "module_pricing": MODULE_PRICING,
        "currency": "USD",
        "billing_cycle": "monthly"
    }

@router.get("/analytics", response_model=AnalyticsResponse, summary="Get analytics")
async def get_analytics(
    request: AnalyticsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed analytics for the authenticated user.
    
    - **start_date**: Start date for analytics period
    - **end_date**: End date for analytics period
    - **module**: Optional module filter
    - **group_by**: Grouping method (day, hour, module)
    """
    try:
        # Get usage data
        usage_stats = billing_manager.get_user_usage(
            current_user.id,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        # Calculate analytics
        total_calls = usage_stats["total_calls"]
        total_cost = usage_stats["total_cost"]
        
        calls_by_module = {
            item["module"]: item["calls"] 
            for item in usage_stats["usage_by_module"]
        }
        
        cost_by_module = {
            item["module"]: item["cost"] 
            for item in usage_stats["usage_by_module"]
        }
        
        # Generate usage trend (simplified)
        usage_trend = []
        if request.start_date and request.end_date:
            current_date = request.start_date
            while current_date <= request.end_date:
                usage_trend.append({
                    "date": current_date.isoformat(),
                    "calls": 0,  # Would need to implement daily breakdown
                    "cost": 0.0
                })
                current_date += timedelta(days=1)
        
        return AnalyticsResponse(
            period={
                "start": request.start_date or datetime.now().replace(day=1),
                "end": request.end_date or datetime.now()
            },
            total_calls=total_calls,
            total_cost=total_cost,
            calls_by_module=calls_by_module,
            cost_by_module=cost_by_module,
            usage_trend=usage_trend
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analytics: {str(e)}"
        )

@router.get("/limits", summary="Get rate limits")
async def get_rate_limits(current_user: User = Depends(get_current_user)):
    """
    Get rate limits for the user's current plan.
    """
    from ..rate_limiter import RATE_LIMITS
    
    plan_limits = RATE_LIMITS.get(current_user.plan, {})
    return {
        "user_id": current_user.id,
        "plan": current_user.plan,
        "rate_limits": plan_limits
    } 