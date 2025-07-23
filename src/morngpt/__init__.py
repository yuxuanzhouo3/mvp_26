"""
mornGPT - Multi-Module AI System
A comprehensive AI system with specialized modules for various use cases.
"""

__version__ = "1.0.0"
__author__ = "mornGPT Team"

from .core import MornGPT
from .modules import *

__all__ = [
    "MornGPT",
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