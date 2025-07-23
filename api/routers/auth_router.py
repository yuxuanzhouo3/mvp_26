"""
Authentication Router for mornGPT Commercial API

Handles user registration, login, and API key management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import uuid

from ..auth import auth_manager, get_current_user
from ..models import (
    User, UserCreate, UserLogin, APIKey, APIKeyCreate,
    AuthResponse, ErrorResponse
)

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=AuthResponse, summary="Register a new user")
async def register_user(user_data: UserCreate):
    """
    Register a new user account.
    
    - **email**: User's email address
    - **password**: Password (minimum 8 characters)
    - **company_name**: Optional company name
    """
    try:
        # Register user
        user = auth_manager.register_user(user_data)
        
        # Create access token
        access_token = auth_manager.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=None
        )
        
        # Create default API key
        api_key = auth_manager.create_api_key(user.id, "Default API Key")
        
        return AuthResponse(
            access_token=access_token,
            expires_in=1800,  # 30 minutes
            user=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=AuthResponse, summary="Login user")
async def login_user(user_data: UserLogin):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    """
    try:
        # Authenticate user
        user = auth_manager.authenticate_user(user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = auth_manager.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=None
        )
        
        return AuthResponse(
            access_token=access_token,
            expires_in=1800,  # 30 minutes
            user=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=User, summary="Get current user")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.
    """
    return current_user

@router.post("/api-keys", response_model=APIKey, summary="Create API key")
async def create_api_key(
    api_key_data: APIKeyCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new API key for the authenticated user.
    
    - **name**: Name for the API key
    """
    try:
        api_key = auth_manager.create_api_key(current_user.id, api_key_data.name)
        return api_key
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create API key: {str(e)}"
        )

@router.get("/api-keys", response_model=List[APIKey], summary="List API keys")
async def list_api_keys(current_user: User = Depends(get_current_user)):
    """
    Get all API keys for the authenticated user.
    """
    try:
        api_keys = auth_manager.get_user_api_keys(current_user.id)
        return api_keys
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve API keys: {str(e)}"
        )

@router.delete("/api-keys/{key_id}", summary="Revoke API key")
async def revoke_api_key(
    key_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Revoke an API key.
    
    - **key_id**: ID of the API key to revoke
    """
    try:
        success = auth_manager.revoke_api_key(current_user.id, key_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        return {"message": "API key revoked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to revoke API key: {str(e)}"
        )

@router.post("/refresh", response_model=AuthResponse, summary="Refresh access token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh the access token for the authenticated user.
    """
    try:
        # Create new access token
        access_token = auth_manager.create_access_token(
            data={"sub": str(current_user.id)},
            expires_delta=None
        )
        
        return AuthResponse(
            access_token=access_token,
            expires_in=1800,  # 30 minutes
            user=current_user
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh token: {str(e)}"
        )

@router.post("/logout", summary="Logout user")
async def logout_user(current_user: User = Depends(get_current_user)):
    """
    Logout the current user (client-side token invalidation).
    """
    # In a real implementation, you might want to blacklist the token
    # For now, we'll just return a success message
    return {"message": "Logged out successfully"}

@router.get("/validate", summary="Validate token")
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Validate the current access token.
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "plan": current_user.plan
    } 