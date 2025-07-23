"""
Pydantic Models for mornGPT Commercial API

Defines request/response schemas and data validation models.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

# Enums
class PlanType(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class ModuleType(str, Enum):
    GROWTH_ADVISORY = "growth_advisory"
    INTERVIEW_JOB = "interview_job"
    CODER = "coder"
    CONTENT_DETECTION = "content_detection"
    MEDICAL_ADVICE = "medical_advice"
    MULTI_GPT = "multi_gpt"
    HOUSING = "housing"
    PERSON_MATCHING = "person_matching"
    TEACHER_COACH = "teacher_coach"
    TRAVELING = "traveling"
    PRODUCT_SEARCH = "product_search"
    CLOTHING = "clothing"
    RESTAURANT_FOOD = "restaurant_food"
    CONTENT_GENERATION = "content_generation"
    ANTI_AI_PROTECTION = "anti_ai_protection"

class ModelVersion(int, Enum):
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    V5 = 5
    V6 = 6
    V7 = 7
    V8 = 8
    V9 = 9

# Base Models
class User(BaseModel):
    id: int
    email: EmailStr
    company_name: Optional[str] = None
    plan: PlanType
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class APIKey(BaseModel):
    id: int
    user_id: int
    api_key: str
    name: str
    created_at: datetime
    last_used: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True

class UsageStats(BaseModel):
    user_id: int
    module: ModuleType
    calls_count: int
    cost_per_call: float
    total_cost: float
    timestamp: datetime

    class Config:
        from_attributes = True

class BillingPlan(BaseModel):
    name: PlanType
    monthly_calls: int
    price_per_call: float
    monthly_fee: float
    features: List[str]

# Request Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    company_name: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class APIKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class APIRequest(BaseModel):
    model_version: ModelVersion = ModelVersion.V1
    parameters: Dict[str, Any] = Field(default_factory=dict)
    options: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True

# Response Models
class APIResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    request_id: Optional[str] = None
    processing_time: Optional[float] = None
    cost: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class BillingResponse(BaseModel):
    user_id: int
    plan: PlanType
    usage_by_module: List[Dict[str, Any]]
    total_calls: int
    total_cost: float
    plan_limits: Dict[str, Any]
    remaining_calls: int

class RateLimitResponse(BaseModel):
    rate_limited: bool
    usage: Optional[Dict[str, Any]] = None
    window_type: Optional[str] = None
    limit: Optional[int] = None
    current: Optional[int] = None
    reset_time: Optional[datetime] = None

# Module-specific request models
class GrowthAdvisoryRequest(APIRequest):
    business_type: str = Field(..., description="Type of business")
    target_market: str = Field(..., description="Target market description")
    current_challenges: Optional[List[str]] = None
    budget_range: Optional[str] = None

class InterviewJobRequest(APIRequest):
    job_title: str = Field(..., description="Job title or position")
    company_type: str = Field(..., description="Type of company")
    experience_level: str = Field(..., description="Experience level")
    interview_type: Optional[str] = "general"

class CoderRequest(APIRequest):
    programming_language: str = Field(..., description="Programming language")
    task_description: str = Field(..., description="Coding task description")
    code_context: Optional[str] = None
    requirements: Optional[List[str]] = None

class ContentDetectionRequest(APIRequest):
    content_type: str = Field(..., description="Type of content (text, image, audio, video)")
    content_data: str = Field(..., description="Content to analyze")
    detection_method: Optional[str] = "auto"

class MedicalAdviceRequest(APIRequest):
    symptoms: List[str] = Field(..., description="List of symptoms")
    age: int = Field(..., ge=0, le=120, description="Patient age")
    gender: Optional[str] = None
    medical_history: Optional[List[str]] = None

class MultiGPTRequest(APIRequest):
    prompt: str = Field(..., description="Main prompt")
    context: Optional[str] = None
    model_preferences: Optional[List[str]] = None
    output_format: Optional[str] = "text"

class HousingRequest(APIRequest):
    location: str = Field(..., description="Desired location")
    budget: float = Field(..., gt=0, description="Budget amount")
    property_type: str = Field(..., description="Type of property")
    requirements: Optional[List[str]] = None

class PersonMatchingRequest(APIRequest):
    matching_type: str = Field(..., description="Type of matching (job, dating, business)")
    criteria: Dict[str, Any] = Field(..., description="Matching criteria")
    preferences: Optional[Dict[str, Any]] = None

class TeacherCoachRequest(APIRequest):
    subject: str = Field(..., description="Subject to learn")
    skill_level: str = Field(..., description="Current skill level")
    learning_goals: List[str] = Field(..., description="Learning objectives")
    preferred_style: Optional[str] = None

class TravelingRequest(APIRequest):
    destination: str = Field(..., description="Travel destination")
    duration: int = Field(..., gt=0, description="Trip duration in days")
    budget: float = Field(..., gt=0, description="Travel budget")
    preferences: Optional[Dict[str, Any]] = None

class ProductSearchRequest(APIRequest):
    product_name: str = Field(..., description="Product to search for")
    category: Optional[str] = None
    price_range: Optional[Dict[str, float]] = None
    features: Optional[List[str]] = None

class ClothingRequest(APIRequest):
    occasion: str = Field(..., description="Occasion for clothing")
    style_preference: str = Field(..., description="Style preference")
    budget: float = Field(..., gt=0, description="Budget amount")
    body_type: Optional[str] = None

class RestaurantFoodRequest(APIRequest):
    location: str = Field(..., description="Location for dining")
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None

class ContentGenerationRequest(APIRequest):
    content_type: str = Field(..., description="Type of content to generate")
    prompt: str = Field(..., description="Generation prompt")
    style: Optional[str] = None
    length: Optional[int] = None

class AntiAIProtectionRequest(APIRequest):
    protection_scenario: str = Field(..., description="Type of protection scenario")
    ai_system: Optional[str] = None
    threat_level: Optional[str] = None
    human_data: Optional[Dict[str, Any]] = None

# Analytics Models
class AnalyticsRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    module: Optional[ModuleType] = None
    group_by: Optional[str] = "day"

class AnalyticsResponse(BaseModel):
    period: Dict[str, datetime]
    total_calls: int
    total_cost: float
    calls_by_module: Dict[str, int]
    cost_by_module: Dict[str, float]
    usage_trend: List[Dict[str, Any]]

# Webhook Models
class WebhookEvent(BaseModel):
    event_type: str
    user_id: int
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)

class WebhookSubscription(BaseModel):
    url: str
    events: List[str]
    secret: Optional[str] = None
    is_active: bool = True 