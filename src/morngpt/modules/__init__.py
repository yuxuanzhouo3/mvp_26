"""
mornGPT modules package containing all specialized AI modules.
"""

from .base import BaseModule
from .multi_gpt import MultiGPTModule
from .teacher_coach import TeacherCoachModule
from .coder import CoderModule
from .content_generation import ContentGenerationModule
from .content_detection import ContentDetectionModule
from .person_matching import PersonMatchingModule
from .interview_job import InterviewJobModule
from .medical_advice import MedicalAdviceModule
from .growth_advisory import GrowthAdvisoryModule
from .product_search import ProductSearchModule
from .restaurant_food import RestaurantFoodModule
from .personalized_clothing import PersonalizedClothingModule
from .personalized_housing import PersonalizedHousingModule
from .personalized_traveling import PersonalizedTravelingModule

__all__ = [
    "BaseModule",
    "MultiGPTModule",
    "TeacherCoachModule",
    "CoderModule", 
    "ContentGenerationModule",
    "ContentDetectionModule",
    "PersonMatchingModule",
    "InterviewJobModule",
    "MedicalAdviceModule",
    "GrowthAdvisoryModule",
    "ProductSearchModule",
    "RestaurantFoodModule",
    "PersonalizedClothingModule",
    "PersonalizedHousingModule",
    "PersonalizedTravelingModule"
] 