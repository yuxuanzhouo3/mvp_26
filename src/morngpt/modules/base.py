"""
Base module class for all mornGPT modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseModule(ABC):
    """
    Base class for all mornGPT modules.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize base module.
        
        Args:
            config: Module configuration
        """
        self.config = config
        self.submodules = {}
        self._initialize_submodules()
    
    @abstractmethod
    def _initialize_submodules(self):
        """
        Initialize sub-modules (h1-h9, q1-q9, etc.).
        Must be implemented by each module.
        """
        pass
    
    def get_submodule(self, submodule_id: int):
        """
        Get a specific sub-module by ID (1-9).
        
        Args:
            submodule_id: Sub-module ID (1-9)
            
        Returns:
            The sub-module instance
        """
        if submodule_id not in range(1, 10):
            raise ValueError("Sub-module ID must be between 1 and 9")
        
        if submodule_id not in self.submodules:
            raise ValueError(f"Sub-module {submodule_id} not found")
        
        return self.submodules[submodule_id]
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get module information.
        
        Returns:
            Module information dictionary
        """
        return {
            "name": self.__class__.__name__,
            "description": self.get_description(),
            "submodules": list(self.submodules.keys()),
            "config": self.config
        }
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get module description.
        Must be implemented by each module.
        
        Returns:
            Module description
        """
        pass


class BaseSubmodule(ABC):
    """
    Base class for all sub-modules.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize sub-module.
        
        Args:
            config: Sub-module configuration
        """
        self.config = config
        self.model_version = 1  # Default to version 1
        self.model_quality = {
            1: "Basic - Standard performance",
            2: "Improved - Better accuracy",
            3: "Enhanced - Advanced features",
            4: "Premium - High quality",
            5: "Expert - Professional grade",
            6: "Master - Elite performance",
            7: "Ultimate - Top tier",
            8: "Perfect - Near flawless",
            9: "Best - Optimal performance"
        }
    
    @abstractmethod
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request.
        Must be implemented by each sub-module.
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        pass
    
    def set_model_version(self, version: int):
        """
        Set the model version for this submodule.
        
        Args:
            version: Model version (1-9, where 9 is the best)
        """
        if not 1 <= version <= 9:
            raise ValueError("Model version must be between 1 and 9")
        self.model_version = version
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about available model versions.
        
        Returns:
            Model version information
        """
        return {
            "current_version": self.model_version,
            "current_quality": self.model_quality[self.model_version],
            "available_versions": self.model_quality,
            "max_version": 9,
            "best_version": 9
        }
    
    def upgrade_model(self, target_version: int) -> Dict[str, Any]:
        """
        Upgrade the model to a specific version.
        
        Args:
            target_version: Target model version (1-9)
            
        Returns:
            Upgrade result information
        """
        if not 1 <= target_version <= 9:
            raise ValueError("Model version must be between 1 and 9")
        
        old_version = self.model_version
        self.model_version = target_version
        
        return {
            "success": True,
            "old_version": old_version,
            "new_version": target_version,
            "quality_improvement": f"From {self.model_quality[old_version]} to {self.model_quality[target_version]}",
            "message": f"Model upgraded from version {old_version} to {target_version}"
        }
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get sub-module information.
        
        Returns:
            Sub-module information dictionary
        """
        return {
            "name": self.__class__.__name__,
            "description": self.get_description(),
            "config": self.config,
            "model_version": self.model_version,
            "model_quality": self.model_quality[self.model_version]
        }
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get sub-module description.
        Must be implemented by each sub-module.
        
        Returns:
            Sub-module description
        """
        pass 