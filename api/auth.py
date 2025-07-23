"""
Authentication and Authorization System for mornGPT Commercial API

Handles user registration, API key management, and JWT token authentication.
"""

import jwt
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import sqlite3
import json

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
def init_db():
    """Initialize the database with users and API keys tables"""
    conn = sqlite3.connect('mornGPT_api.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            company_name TEXT,
            plan TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # API Keys table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class APIKeyCreate(BaseModel):
    name: str

class User(BaseModel):
    id: int
    email: str
    company_name: Optional[str]
    plan: str
    created_at: datetime
    is_active: bool

class APIKey(BaseModel):
    id: int
    user_id: int
    api_key: str
    name: str
    created_at: datetime
    last_used: Optional[datetime]
    is_active: bool

class AuthManager:
    """Manages authentication and authorization"""
    
    def __init__(self):
        init_db()
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return self.hash_password(password) == hashed
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None
    
    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists"
                )
            
            # Hash password and create user
            password_hash = self.hash_password(user_data.password)
            cursor.execute(
                "INSERT INTO users (email, password_hash, company_name) VALUES (?, ?, ?)",
                (user_data.email, password_hash, user_data.company_name)
            )
            user_id = cursor.lastrowid
            
            conn.commit()
            
            # Return user data
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_row = cursor.fetchone()
            
            return User(
                id=user_row[0],
                email=user_row[1],
                company_name=user_row[3],
                plan=user_row[4],
                created_at=datetime.fromisoformat(user_row[5]),
                is_active=bool(user_row[7])
            )
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_row = cursor.fetchone()
            
            if not user_row:
                return None
            
            if not self.verify_password(password, user_row[2]):
                return None
            
            return User(
                id=user_row[0],
                email=user_row[1],
                company_name=user_row[3],
                plan=user_row[4],
                created_at=datetime.fromisoformat(user_row[5]),
                is_active=bool(user_row[7])
            )
            
        finally:
            conn.close()
    
    def create_api_key(self, user_id: int, name: str) -> APIKey:
        """Create a new API key for a user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # Generate a secure API key
            api_key = f"morn_{secrets.token_urlsafe(32)}"
            
            cursor.execute(
                "INSERT INTO api_keys (user_id, api_key, name) VALUES (?, ?, ?)",
                (user_id, api_key, name)
            )
            key_id = cursor.lastrowid
            
            conn.commit()
            
            return APIKey(
                id=key_id,
                user_id=user_id,
                api_key=api_key,
                name=name,
                created_at=datetime.now(),
                last_used=None,
                is_active=True
            )
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_user_by_api_key(self, api_key: str) -> Optional[User]:
        """Get user by API key"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT u.* FROM users u
                JOIN api_keys ak ON u.id = ak.user_id
                WHERE ak.api_key = ? AND ak.is_active = TRUE AND u.is_active = TRUE
            """, (api_key,))
            
            user_row = cursor.fetchone()
            if not user_row:
                return None
            
            # Update last used timestamp
            cursor.execute(
                "UPDATE api_keys SET last_used = CURRENT_TIMESTAMP WHERE api_key = ?",
                (api_key,)
            )
            conn.commit()
            
            return User(
                id=user_row[0],
                email=user_row[1],
                company_name=user_row[3],
                plan=user_row[4],
                created_at=datetime.fromisoformat(user_row[5]),
                is_active=bool(user_row[7])
            )
            
        finally:
            conn.close()
    
    def get_user_api_keys(self, user_id: int) -> list[APIKey]:
        """Get all API keys for a user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM api_keys WHERE user_id = ?", (user_id,))
            keys = []
            
            for row in cursor.fetchall():
                keys.append(APIKey(
                    id=row[0],
                    user_id=row[1],
                    api_key=row[2],
                    name=row[3],
                    created_at=datetime.fromisoformat(row[4]),
                    last_used=datetime.fromisoformat(row[5]) if row[5] else None,
                    is_active=bool(row[6])
                ))
            
            return keys
            
        finally:
            conn.close()
    
    def revoke_api_key(self, user_id: int, key_id: int) -> bool:
        """Revoke an API key"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE api_keys SET is_active = FALSE WHERE id = ? AND user_id = ?",
                (key_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()

# Global auth manager instance
auth_manager = AuthManager()

# Security dependency
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token or API key"""
    token = credentials.credentials
    
    # Try JWT token first
    payload = auth_manager.verify_token(token)
    if payload:
        user_id = payload.get("sub")
        if user_id:
            # Get user from database
            conn = sqlite3.connect('mornGPT_api.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_row = cursor.fetchone()
            conn.close()
            
            if user_row:
                return User(
                    id=user_row[0],
                    email=user_row[1],
                    company_name=user_row[3],
                    plan=user_row[4],
                    created_at=datetime.fromisoformat(user_row[5]),
                    is_active=bool(user_row[7])
                )
    
    # Try API key
    user = auth_manager.get_user_by_api_key(token)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) 