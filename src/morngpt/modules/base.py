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
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get sub-module information.
        
        Returns:
            Sub-module information dictionary
        """
        return {
            "name": self.__class__.__name__,
            "description": self.get_description(),
            "config": self.config
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