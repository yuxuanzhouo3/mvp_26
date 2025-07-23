"""
mornGPT - Multi-Module AI System
A comprehensive AI system with specialized modules for various use cases.
"""

from typing import Dict, Any, Optional
from .modules import *


class MornGPT:
    """
    Main mornGPT class that orchestrates all specialized AI modules.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize mornGPT with all specialized modules.
        
        Args:
            config: Configuration dictionary for all modules
        """
        self.config = config or {}
        
        # Initialize all specialized modules
        self.multi_gpt = MultiGPTModule(self.config.get('multi_gpt', {}))
        self.teacher_coach = TeacherCoachModule(self.config.get('teacher_coach', {}))
        self.coder = CoderModule(self.config.get('coder', {}))
        self.content_generation = ContentGenerationModule(self.config.get('content_generation', {}))
        self.content_detection = ContentDetectionModule(self.config.get('content_detection', {}))
        self.person_matching = PersonMatchingModule(self.config.get('person_matching', {}))
        self.interview_job = InterviewJobModule(self.config.get('interview_job', {}))
        self.medical_advice = MedicalAdviceModule(self.config.get('medical_advice', {}))
        self.growth_advisory = GrowthAdvisoryModule(self.config.get('growth_advisory', {}))
        self.product_search = ProductSearchModule(self.config.get('product_search', {}))
        self.restaurant_food = RestaurantFoodModule(self.config.get('restaurant_food', {}))
        self.personalized_clothing = PersonalizedClothingModule(self.config.get('personalized_clothing', {}))
        self.personalized_housing = PersonalizedHousingModule(self.config.get('personalized_housing', {}))
        self.personalized_traveling = PersonalizedTravelingModule(self.config.get('personalized_traveling', {}))
        
        self.modules = {
            'h': self.multi_gpt,
            'q': self.teacher_coach,
            'c': self.coder,
            'w': self.content_generation,
            'd': self.content_detection,
            'p': self.person_matching,
            'b': self.interview_job,
            'e': self.medical_advice,
            'a': self.growth_advisory,
            's': self.product_search,
            'u': self.restaurant_food,
            't': self.personalized_clothing,
            'o': self.personalized_housing,
            'r': self.personalized_traveling
        }
    
    def get_module(self, module_code: str):
        """
        Get a specific module by its code (h, q, c, w, d, p, b, e, a, s, u, t, o, r).
        """
        if module_code not in self.modules:
            raise ValueError(f"Module {module_code} not found. Available modules: {list(self.modules.keys())}")
        return self.modules[module_code]
    
    def get_submodule(self, module_code: str, submodule_id: int, model_version: int = 1):
        """
        Get a specific submodule with specified model version.
        
        Args:
            module_code: Module code (h, q, c, w, d, p, b, e, a, s, u, t, o, r)
            submodule_id: Submodule ID (1-9)
            model_version: Model version (1-9, where 9 is the best)
        """
        module = self.get_module(module_code)
        submodule = module.get_submodule(submodule_id)
        
        # Set model version for the submodule
        submodule.set_model_version(model_version)
        
        return submodule
    
    def process_request(self, module_code: str, submodule_id: int, request: Dict[str, Any], model_version: int = 1):
        """
        Process a request through a specific submodule with specified model version.
        
        Args:
            module_code: Module code (h, q, c, w, d, p, b, e, a, s, u, t, o, r)
            submodule_id: Submodule ID (1-9)
            request: Request data
            model_version: Model version (1-9, where 9 is the best)
        """
        submodule = self.get_submodule(module_code, submodule_id, model_version)
        return submodule.process(request)
    
    def get_model_info(self, module_code: str, submodule_id: int):
        """
        Get information about available model versions for a submodule.
        
        Args:
            module_code: Module code (h, q, c, w, d, p, b, e, a, s, u, t, o, r)
            submodule_id: Submodule ID (1-9)
        """
        module = self.get_module(module_code)
        submodule = module.get_submodule(submodule_id)
        return submodule.get_model_info()
    
    def upgrade_model(self, module_code: str, submodule_id: int, target_version: int):
        """
        Upgrade a submodule to a specific model version.
        
        Args:
            module_code: Module code (h, q, c, w, d, p, b, e, a, s, u, t, o, r)
            submodule_id: Submodule ID (1-9)
            target_version: Target model version (1-9)
        """
        if not 1 <= target_version <= 9:
            raise ValueError("Model version must be between 1 and 9")
        
        module = self.get_module(module_code)
        submodule = module.get_submodule(submodule_id)
        return submodule.upgrade_model(target_version)
    
    def get_all_modules_info(self):
        """
        Get information about all modules and their submodules.
        """
        info = {}
        for code, module in self.modules.items():
            info[code] = module.get_info()
        return info 