"""
Analytics Router for mornGPT Commercial API

Provides detailed analytics and reporting endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from ..auth import get_current_user
from ..billing import billing_manager
from ..rate_limiter import rate_limiter
from ..models import User, AnalyticsRequest, AnalyticsResponse

router = APIRouter()

@router.get("/overview", summary="Get analytics overview")
async def get_analytics_overview(
    period: str = Query("30d", description="Analytics period (7d, 30d, 90d, 1y)"),
    current_user: User = Depends(get_current_user)
):
    """
    Get an overview of analytics for the authenticated user.
    
    - **period**: Analytics period (7d, 30d, 90d, 1y)
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        elif period == "90d":
            start_date = end_date - timedelta(days=90)
        elif period == "1y":
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get usage stats
        usage_stats = billing_manager.get_user_usage(
            current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Get rate limit stats
        rate_limit_stats = rate_limiter.get_user_usage_stats(
            current_user.id,
            current_user.plan
        )
        
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "duration": period
            },
            "usage": {
                "total_calls": usage_stats["total_calls"],
                "total_cost": usage_stats["total_cost"],
                "modules_used": len(usage_stats["usage_by_module"]),
                "average_cost_per_call": usage_stats["total_cost"] / max(usage_stats["total_calls"], 1)
            },
            "rate_limits": rate_limit_stats,
            "plan": {
                "current": current_user.plan,
                "remaining_calls": usage_stats["remaining_calls"],
                "usage_percentage": (usage_stats["total_calls"] / usage_stats["plan_limits"]["monthly_calls"]) * 100
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analytics overview: {str(e)}"
        )

@router.get("/module-breakdown", summary="Get module usage breakdown")
async def get_module_breakdown(
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed breakdown of usage by module.
    
    - **start_date**: Optional start date
    - **end_date**: Optional end date
    """
    try:
        usage_stats = billing_manager.get_user_usage(
            current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Calculate percentages
        total_calls = usage_stats["total_calls"]
        total_cost = usage_stats["total_cost"]
        
        module_breakdown = []
        for module_data in usage_stats["usage_by_module"]:
            calls_percentage = (module_data["calls"] / max(total_calls, 1)) * 100
            cost_percentage = (module_data["cost"] / max(total_cost, 1)) * 100
            
            module_breakdown.append({
                "module": module_data["module"],
                "calls": module_data["calls"],
                "cost": module_data["cost"],
                "calls_percentage": calls_percentage,
                "cost_percentage": cost_percentage,
                "average_cost_per_call": module_data["cost"] / max(module_data["calls"], 1)
            })
        
        # Sort by calls (descending)
        module_breakdown.sort(key=lambda x: x["calls"], reverse=True)
        
        return {
            "period": {
                "start": start_date or datetime.now().replace(day=1),
                "end": end_date or datetime.now()
            },
            "total_calls": total_calls,
            "total_cost": total_cost,
            "modules": module_breakdown
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve module breakdown: {str(e)}"
        )

@router.get("/usage-trend", summary="Get usage trend over time")
async def get_usage_trend(
    period: str = Query("30d", description="Trend period (7d, 30d, 90d)"),
    granularity: str = Query("day", description="Time granularity (hour, day, week)"),
    current_user: User = Depends(get_current_user)
):
    """
    Get usage trend over time.
    
    - **period**: Trend period (7d, 30d, 90d)
    - **granularity**: Time granularity (hour, day, week)
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        elif period == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Generate time points
        trend_data = []
        current_point = start_date
        
        while current_point <= end_date:
            # Get usage for this time point
            point_end = current_point + timedelta(days=1) if granularity == "day" else current_point + timedelta(hours=1)
            
            usage_stats = billing_manager.get_user_usage(
                current_user.id,
                start_date=current_point,
                end_date=point_end
            )
            
            trend_data.append({
                "timestamp": current_point.isoformat(),
                "calls": usage_stats["total_calls"],
                "cost": usage_stats["total_cost"],
                "modules_used": len(usage_stats["usage_by_module"])
            })
            
            # Move to next time point
            if granularity == "hour":
                current_point += timedelta(hours=1)
            elif granularity == "day":
                current_point += timedelta(days=1)
            elif granularity == "week":
                current_point += timedelta(weeks=1)
        
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "granularity": granularity
            },
            "trend": trend_data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage trend: {str(e)}"
        )

@router.get("/performance", summary="Get API performance metrics")
async def get_performance_metrics(
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    current_user: User = Depends(get_current_user)
):
    """
    Get API performance metrics for the user.
    
    - **start_date**: Optional start date
    - **end_date**: Optional end date
    """
    try:
        # This would typically integrate with monitoring systems
        # For now, we'll return placeholder data
        
        return {
            "period": {
                "start": start_date or datetime.now().replace(day=1),
                "end": end_date or datetime.now()
            },
            "response_times": {
                "average": 0.15,  # seconds
                "p95": 0.25,
                "p99": 0.35,
                "min": 0.05,
                "max": 0.45
            },
            "success_rate": 99.8,  # percentage
            "error_rate": 0.2,     # percentage
            "availability": 99.9,   # percentage
            "rate_limit_hits": 0,   # number of times rate limited
            "total_requests": 0     # would be calculated from actual data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve performance metrics: {str(e)}"
        )

@router.get("/cost-analysis", summary="Get cost analysis")
async def get_cost_analysis(
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed cost analysis.
    
    - **start_date**: Optional start date
    - **end_date**: Optional end date
    """
    try:
        usage_stats = billing_manager.get_user_usage(
            current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Calculate cost metrics
        total_calls = usage_stats["total_calls"]
        total_cost = usage_stats["total_cost"]
        
        # Cost breakdown by module
        cost_by_module = {}
        for module_data in usage_stats["usage_by_module"]:
            cost_by_module[module_data["module"]] = {
                "total_cost": module_data["cost"],
                "calls": module_data["calls"],
                "cost_per_call": module_data["cost"] / max(module_data["calls"], 1),
                "percentage": (module_data["cost"] / max(total_cost, 1)) * 100
            }
        
        # Cost efficiency metrics
        avg_cost_per_call = total_cost / max(total_calls, 1)
        
        # Projected costs
        days_in_period = (end_date or datetime.now()) - (start_date or datetime.now().replace(day=1))
        days_in_period = days_in_period.days or 1
        
        daily_cost = total_cost / days_in_period
        monthly_projection = daily_cost * 30
        
        return {
            "period": {
                "start": start_date or datetime.now().replace(day=1),
                "end": end_date or datetime.now(),
                "days": days_in_period
            },
            "summary": {
                "total_cost": total_cost,
                "total_calls": total_calls,
                "average_cost_per_call": avg_cost_per_call,
                "daily_average_cost": daily_cost,
                "monthly_projection": monthly_projection
            },
            "cost_by_module": cost_by_module,
            "efficiency": {
                "cost_per_call": avg_cost_per_call,
                "calls_per_dollar": total_calls / max(total_cost, 1),
                "most_expensive_module": max(cost_by_module.items(), key=lambda x: x[1]["cost_per_call"])[0] if cost_by_module else None,
                "least_expensive_module": min(cost_by_module.items(), key=lambda x: x[1]["cost_per_call"])[0] if cost_by_module else None
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve cost analysis: {str(e)}"
        )

@router.get("/export", summary="Export analytics data")
async def export_analytics(
    format: str = Query("json", description="Export format (json, csv)"),
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    current_user: User = Depends(get_current_user)
):
    """
    Export analytics data in various formats.
    
    - **format**: Export format (json, csv)
    - **start_date**: Optional start date
    - **end_date**: Optional end date
    """
    try:
        # Get comprehensive analytics data
        usage_stats = billing_manager.get_user_usage(
            current_user.id,
            start_date=start_date,
            end_date=end_date
        )
        
        export_data = {
            "user_id": current_user.id,
            "email": current_user.email,
            "plan": current_user.plan,
            "period": {
                "start": start_date or datetime.now().replace(day=1),
                "end": end_date or datetime.now()
            },
            "usage_summary": {
                "total_calls": usage_stats["total_calls"],
                "total_cost": usage_stats["total_cost"],
                "modules_used": len(usage_stats["usage_by_module"])
            },
            "usage_by_module": usage_stats["usage_by_module"],
            "exported_at": datetime.now().isoformat()
        }
        
        if format.lower() == "csv":
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(["Module", "Calls", "Cost", "Cost per Call"])
            
            # Write data
            for module_data in usage_stats["usage_by_module"]:
                writer.writerow([
                    module_data["module"],
                    module_data["calls"],
                    module_data["cost"],
                    module_data["cost"] / max(module_data["calls"], 1)
                ])
            
            return {
                "format": "csv",
                "data": output.getvalue(),
                "filename": f"mornGPT_analytics_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        else:
            return {
                "format": "json",
                "data": export_data
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export analytics: {str(e)}"
        ) 