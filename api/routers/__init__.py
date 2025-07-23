"""
Router imports for mornGPT Commercial API

Centralized imports for all API routers.
"""

# Core routers
from .auth_router import router as auth_router
from .billing_router import router as billing_router
from .analytics_router import router as analytics_router

# Module routers
from .growth_advisory_router import router as growth_advisory_router

# Placeholder routers for other modules (to be implemented)
# These will be replaced with actual implementations as modules are completed

# Create placeholder routers for remaining modules
from fastapi import APIRouter

def create_placeholder_router(module_name: str, module_display_name: str):
    """Create a placeholder router for modules not yet implemented"""
    router = APIRouter()
    
    @router.get("/", summary=f"Get {module_display_name} information")
    async def get_module_info():
        return {
            "module": module_name,
            "status": "coming_soon",
            "message": f"{module_display_name} module is coming soon!",
            "estimated_availability": "Q1 2025"
        }
    
    @router.post("/placeholder", summary=f"Placeholder endpoint for {module_display_name}")
    async def placeholder_endpoint():
        return {
            "error": "Module not yet implemented",
            "module": module_name,
            "message": f"{module_display_name} module is currently under development"
        }
    
    return router

# Create placeholder routers for all modules
interview_job_router = create_placeholder_router("interview_job", "Interview/Job")
coder_router = create_placeholder_router("coder", "AI Coder")
content_detection_router = create_placeholder_router("content_detection", "Content Detection")
medical_advice_router = create_placeholder_router("medical_advice", "Medical Advice")
multi_gpt_router = create_placeholder_router("multi_gpt", "Multi-GPT")
housing_router = create_placeholder_router("housing", "Personalized Housing")
person_matching_router = create_placeholder_router("person_matching", "Person Matching")
teacher_coach_router = create_placeholder_router("teacher_coach", "Teacher/Coach")
traveling_router = create_placeholder_router("traveling", "Personalized Traveling")
product_search_router = create_placeholder_router("product_search", "Product Search")
clothing_router = create_placeholder_router("clothing", "Personalized Clothing")
restaurant_food_router = create_placeholder_router("restaurant_food", "Restaurant/Food")
content_generation_router = create_placeholder_router("content_generation", "Content Generation")
anti_ai_protection_router = create_placeholder_router("anti_ai_protection", "Anti-AI Protection")

# Export all routers
__all__ = [
    "auth_router",
    "billing_router", 
    "analytics_router",
    "growth_advisory_router",
    "interview_job_router",
    "coder_router",
    "content_detection_router",
    "medical_advice_router",
    "multi_gpt_router",
    "housing_router",
    "person_matching_router",
    "teacher_coach_router",
    "traveling_router",
    "product_search_router",
    "clothing_router",
    "restaurant_food_router",
    "content_generation_router",
    "anti_ai_protection_router"
] 