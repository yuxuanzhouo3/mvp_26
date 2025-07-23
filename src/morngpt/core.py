"""
Core MornGPT class that orchestrates all specialized modules.
"""

from typing import Dict, Any, Optional
from .modules import *


class MornGPT:
    """
    Main MornGPT class that manages all specialized AI modules.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize MornGPT with all modules.
        
        Args:
            config: Configuration dictionary for modules
        """
        self.config = config or {}
        
        # Initialize all modules
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
            's': self.product_search
        }
    
    def get_module(self, module_code: str):
        """
        Get a specific module by its code (e.g., 'h1', 'q2', etc.).
        
        Args:
            module_code: Module code like 'h1', 'q2', etc.
            
        Returns:
            The specific sub-module
        """
        if len(module_code) != 2:
            raise ValueError("Module code must be 2 characters (e.g., 'h1', 'q2')")
        
        category = module_code[0]
        submodule = int(module_code[1])
        
        if category not in self.modules:
            raise ValueError(f"Unknown module category: {category}")
        
        return self.modules[category].get_submodule(submodule)
    
    def process_request(self, module_code: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request through a specific module.
        
        Args:
            module_code: Module code like 'h1', 'q2', etc.
            request: Request data
            
        Returns:
            Response from the module
        """
        module = self.get_module(module_code)
        return module.process(request)
    
    def get_available_modules(self) -> Dict[str, list]:
        """
        Get list of all available modules.
        
        Returns:
            Dictionary mapping categories to available sub-modules
        """
        return {
            category: [f"{category}{i}" for i in range(1, 10)]
            for category in self.modules.keys()
        }
    
    def get_module_info(self, module_code: str) -> Dict[str, Any]:
        """
        Get information about a specific module.
        
        Args:
            module_code: Module code like 'h1', 'q2', etc.
            
        Returns:
            Module information
        """
        module = self.get_module(module_code)
        return module.get_info() 