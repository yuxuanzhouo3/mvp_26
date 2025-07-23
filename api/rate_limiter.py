"""
Rate Limiting System for mornGPT Commercial API

Controls API usage based on user plans and prevents abuse.
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
from fastapi import HTTPException, status
import sqlite3
from collections import defaultdict

logger = logging.getLogger(__name__)

# Rate limits by plan (requests per minute)
RATE_LIMITS = {
    "free": {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "requests_per_day": 1000
    },
    "starter": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000,
        "requests_per_day": 10000
    },
    "professional": {
        "requests_per_minute": 300,
        "requests_per_hour": 10000,
        "requests_per_day": 100000
    },
    "enterprise": {
        "requests_per_minute": 1000,
        "requests_per_hour": 50000,
        "requests_per_day": 1000000
    }
}

def init_rate_limit_db():
    """Initialize rate limiting database tables"""
    conn = sqlite3.connect('mornGPT_api.db')
    cursor = conn.cursor()
    
    # Rate limit tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rate_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            window_type TEXT NOT NULL,  -- 'minute', 'hour', 'day'
            window_start TIMESTAMP NOT NULL,
            request_count INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

class RateLimiter:
    """Manages rate limiting for API requests"""
    
    def __init__(self):
        init_rate_limit_db()
        # In-memory cache for faster rate limiting
        self.cache = defaultdict(lambda: defaultdict(int))
        self.cache_timestamps = defaultdict(lambda: defaultdict(float))
    
    def _get_window_start(self, window_type: str) -> datetime:
        """Get the start of the current time window"""
        now = datetime.now()
        
        if window_type == "minute":
            return now.replace(second=0, microsecond=0)
        elif window_type == "hour":
            return now.replace(minute=0, second=0, microsecond=0)
        elif window_type == "day":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Invalid window type: {window_type}")
    
    def _cleanup_cache(self, user_id: int, window_type: str):
        """Clean up expired cache entries"""
        now = time.time()
        window_start = self._get_window_start(window_type)
        window_timestamp = window_start.timestamp()
        
        if self.cache_timestamps[user_id][window_type] < window_timestamp:
            self.cache[user_id][window_type] = 0
            self.cache_timestamps[user_id][window_type] = now
    
    def check_rate_limit(self, user_id: int, plan: str) -> Tuple[bool, Dict[str, Any]]:
        """Check if user is within rate limits"""
        if plan not in RATE_LIMITS:
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        limits = RATE_LIMITS[plan]
        current_usage = {}
        
        # Check each time window
        for window_type, limit in limits.items():
            self._cleanup_cache(user_id, window_type)
            
            # Get current count from cache
            current_count = self.cache[user_id][window_type]
            
            # If cache is empty, check database
            if current_count == 0:
                current_count = self._get_database_count(user_id, window_type)
                self.cache[user_id][window_type] = current_count
                self.cache_timestamps[user_id][window_type] = time.time()
            
            current_usage[window_type] = {
                "current": current_count,
                "limit": limit,
                "remaining": max(0, limit - current_count)
            }
            
            # Check if limit exceeded
            if current_count >= limit:
                return False, {
                    "rate_limited": True,
                    "window_type": window_type,
                    "limit": limit,
                    "current": current_count,
                    "reset_time": self._get_reset_time(window_type)
                }
        
        return True, {
            "rate_limited": False,
            "usage": current_usage
        }
    
    def _get_database_count(self, user_id: int, window_type: str) -> int:
        """Get request count from database for a time window"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            window_start = self._get_window_start(window_type)
            
            cursor.execute(
                "SELECT SUM(request_count) FROM rate_limits WHERE user_id = ? AND window_type = ? AND window_start = ?",
                (user_id, window_type, window_start.isoformat())
            )
            
            result = cursor.fetchone()
            return result[0] or 0
            
        finally:
            conn.close()
    
    def increment_usage(self, user_id: int, window_type: str, count: int = 1):
        """Increment usage count for a user and time window"""
        # Update cache
        self.cache[user_id][window_type] += count
        self.cache_timestamps[user_id][window_type] = time.time()
        
        # Update database
        self._update_database_usage(user_id, window_type, count)
    
    def _update_database_usage(self, user_id: int, window_type: str, count: int):
        """Update usage count in database"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            window_start = self._get_window_start(window_type)
            
            # Try to update existing record
            cursor.execute(
                "UPDATE rate_limits SET request_count = request_count + ? WHERE user_id = ? AND window_type = ? AND window_start = ?",
                (count, user_id, window_type, window_start.isoformat())
            )
            
            # If no record exists, create one
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO rate_limits (user_id, window_type, window_start, request_count) VALUES (?, ?, ?, ?)",
                    (user_id, window_type, window_start.isoformat(), count)
                )
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error updating rate limit usage: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def _get_reset_time(self, window_type: str) -> datetime:
        """Get the time when the rate limit will reset"""
        now = datetime.now()
        
        if window_type == "requests_per_minute":
            return now.replace(second=0, microsecond=0) + timedelta(minutes=1)
        elif window_type == "requests_per_hour":
            return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        elif window_type == "requests_per_day":
            return now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        else:
            return now
    
    def get_user_usage_stats(self, user_id: int, plan: str) -> Dict[str, Any]:
        """Get detailed usage statistics for a user"""
        if plan not in RATE_LIMITS:
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        limits = RATE_LIMITS[plan]
        stats = {}
        
        for window_type, limit in limits.items():
            self._cleanup_cache(user_id, window_type)
            
            current_count = self.cache[user_id][window_type]
            if current_count == 0:
                current_count = self._get_database_count(user_id, window_type)
            
            stats[window_type] = {
                "current": current_count,
                "limit": limit,
                "remaining": max(0, limit - current_count),
                "percentage": min(100, (current_count / limit) * 100) if limit > 0 else 0,
                "reset_time": self._get_reset_time(window_type)
            }
        
        return {
            "user_id": user_id,
            "plan": plan,
            "usage_stats": stats
        }
    
    def reset_user_limits(self, user_id: int):
        """Reset rate limits for a user (admin function)"""
        # Clear cache
        if user_id in self.cache:
            del self.cache[user_id]
        
        # Clear database
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM rate_limits WHERE user_id = ?", (user_id,))
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error resetting user limits: {e}")
            conn.rollback()
        finally:
            conn.close()

# Global rate limiter instance
rate_limiter = RateLimiter() 