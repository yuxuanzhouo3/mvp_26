"""
Billing and Payment System for mornGPT Commercial API

Handles usage tracking, billing calculations, and payment processing.
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import HTTPException
import json

logger = logging.getLogger(__name__)

# Pricing configuration
PRICING_TIERS = {
    "free": {
        "monthly_calls": 100,
        "price_per_call": 0.00,
        "monthly_fee": 0.00
    },
    "starter": {
        "monthly_calls": 1000,
        "price_per_call": 0.01,
        "monthly_fee": 9.99
    },
    "professional": {
        "monthly_calls": 10000,
        "price_per_call": 0.005,
        "monthly_fee": 49.99
    },
    "enterprise": {
        "monthly_calls": 100000,
        "price_per_call": 0.002,
        "monthly_fee": 199.99
    }
}

MODULE_PRICING = {
    "growth_advisory": 0.02,
    "interview_job": 0.015,
    "coder": 0.025,
    "content_detection": 0.03,
    "medical_advice": 0.04,
    "multi_gpt": 0.035,
    "housing": 0.02,
    "person_matching": 0.025,
    "teacher_coach": 0.02,
    "traveling": 0.02,
    "product_search": 0.015,
    "clothing": 0.02,
    "restaurant_food": 0.02,
    "content_generation": 0.05,
    "anti_ai_protection": 0.10
}

def init_billing_db():
    """Initialize billing database tables"""
    conn = sqlite3.connect('mornGPT_api.db')
    cursor = conn.cursor()
    
    # Usage tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module TEXT NOT NULL,
            calls_count INTEGER DEFAULT 1,
            cost_per_call REAL NOT NULL,
            total_cost REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Billing cycles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS billing_cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cycle_start TIMESTAMP NOT NULL,
            cycle_end TIMESTAMP NOT NULL,
            total_calls INTEGER DEFAULT 0,
            total_cost REAL DEFAULT 0.00,
            plan TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Payment history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            payment_method TEXT,
            status TEXT DEFAULT 'pending',
            billing_cycle_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (billing_cycle_id) REFERENCES billing_cycles (id)
        )
    ''')
    
    conn.commit()
    conn.close()

class BillingManager:
    """Manages billing, usage tracking, and payments"""
    
    def __init__(self):
        init_billing_db()
    
    async def track_usage(self, user_id: int, module: str, calls: int = 1):
        """Track API usage for billing"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # Get user's plan
            cursor.execute("SELECT plan FROM users WHERE id = ?", (user_id,))
            user_plan = cursor.fetchone()[0]
            
            # Calculate cost
            base_cost = PRICING_TIERS[user_plan]["price_per_call"]
            module_cost = MODULE_PRICING.get(module, 0.01)
            total_cost_per_call = base_cost + module_cost
            
            # Record usage
            cursor.execute(
                "INSERT INTO usage_stats (user_id, module, calls_count, cost_per_call, total_cost) VALUES (?, ?, ?, ?, ?)",
                (user_id, module, calls, total_cost_per_call, total_cost_per_call * calls)
            )
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error tracking usage: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_user_usage(self, user_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # Build query
            query = "SELECT module, SUM(calls_count) as total_calls, SUM(total_cost) as total_cost FROM usage_stats WHERE user_id = ?"
            params = [user_id]
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date.isoformat())
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date.isoformat())
            
            query += " GROUP BY module"
            
            cursor.execute(query, params)
            usage_data = cursor.fetchall()
            
            # Get user plan
            cursor.execute("SELECT plan FROM users WHERE id = ?", (user_id,))
            user_plan = cursor.fetchone()[0]
            
            # Calculate totals
            total_calls = sum(row[1] for row in usage_data)
            total_cost = sum(row[2] for row in usage_data)
            
            # Get plan limits
            plan_limits = PRICING_TIERS[user_plan]
            
            return {
                "user_id": user_id,
                "plan": user_plan,
                "usage_by_module": [
                    {
                        "module": row[0],
                        "calls": row[1],
                        "cost": row[2]
                    } for row in usage_data
                ],
                "total_calls": total_calls,
                "total_cost": total_cost,
                "plan_limits": plan_limits,
                "remaining_calls": max(0, plan_limits["monthly_calls"] - total_calls)
            }
            
        finally:
            conn.close()
    
    def create_billing_cycle(self, user_id: int, plan: str) -> int:
        """Create a new billing cycle for a user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # Set cycle dates (monthly)
            now = datetime.now()
            cycle_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            cycle_end = (cycle_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            
            cursor.execute(
                "INSERT INTO billing_cycles (user_id, cycle_start, cycle_end, plan) VALUES (?, ?, ?, ?)",
                (user_id, cycle_start.isoformat(), cycle_end.isoformat(), plan)
            )
            
            cycle_id = cursor.lastrowid
            conn.commit()
            return cycle_id
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_current_billing_cycle(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get the current billing cycle for a user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            now = datetime.now()
            cursor.execute(
                "SELECT * FROM billing_cycles WHERE user_id = ? AND cycle_start <= ? AND cycle_end >= ? AND status = 'active'",
                (user_id, now.isoformat(), now.isoformat())
            )
            
            cycle_row = cursor.fetchone()
            if not cycle_row:
                return None
            
            return {
                "id": cycle_row[0],
                "user_id": cycle_row[1],
                "cycle_start": datetime.fromisoformat(cycle_row[2]),
                "cycle_end": datetime.fromisoformat(cycle_row[3]),
                "total_calls": cycle_row[4],
                "total_cost": cycle_row[5],
                "plan": cycle_row[6],
                "status": cycle_row[7]
            }
            
        finally:
            conn.close()
    
    def calculate_bill(self, user_id: int, cycle_id: int) -> Dict[str, Any]:
        """Calculate the bill for a billing cycle"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # Get billing cycle
            cursor.execute("SELECT * FROM billing_cycles WHERE id = ? AND user_id = ?", (cycle_id, user_id))
            cycle_row = cursor.fetchone()
            
            if not cycle_row:
                raise HTTPException(status_code=404, detail="Billing cycle not found")
            
            # Get usage for this cycle
            cursor.execute(
                "SELECT SUM(calls_count) as total_calls, SUM(total_cost) as total_cost FROM usage_stats WHERE user_id = ? AND timestamp BETWEEN ? AND ?",
                (user_id, cycle_row[2], cycle_row[3])
            )
            
            usage_row = cursor.fetchone()
            total_calls = usage_row[0] or 0
            total_cost = usage_row[1] or 0.0
            
            # Get plan details
            plan = cycle_row[6]
            plan_details = PRICING_TIERS[plan]
            
            # Calculate bill
            monthly_fee = plan_details["monthly_fee"]
            total_bill = monthly_fee + total_cost
            
            return {
                "billing_cycle_id": cycle_id,
                "user_id": user_id,
                "plan": plan,
                "monthly_fee": monthly_fee,
                "usage_cost": total_cost,
                "total_calls": total_calls,
                "total_bill": total_bill,
                "cycle_start": datetime.fromisoformat(cycle_row[2]),
                "cycle_end": datetime.fromisoformat(cycle_row[3])
            }
            
        finally:
            conn.close()
    
    def process_payment(self, user_id: int, amount: float, payment_method: str = "credit_card") -> Dict[str, Any]:
        """Process a payment (placeholder for payment gateway integration)"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            # In a real implementation, this would integrate with Stripe, PayPal, etc.
            payment_id = f"pay_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            cursor.execute(
                "INSERT INTO payments (user_id, amount, payment_method, status, processed_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, amount, payment_method, "completed", datetime.now().isoformat())
            )
            
            payment_db_id = cursor.lastrowid
            conn.commit()
            
            return {
                "payment_id": payment_id,
                "db_id": payment_db_id,
                "user_id": user_id,
                "amount": amount,
                "status": "completed",
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()
    
    def get_payment_history(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get payment history for a user"""
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit)
            )
            
            payments = []
            for row in cursor.fetchall():
                payments.append({
                    "id": row[0],
                    "user_id": row[1],
                    "amount": row[2],
                    "currency": row[3],
                    "payment_method": row[4],
                    "status": row[5],
                    "billing_cycle_id": row[6],
                    "created_at": datetime.fromisoformat(row[7]),
                    "processed_at": datetime.fromisoformat(row[8]) if row[8] else None
                })
            
            return payments
            
        finally:
            conn.close()
    
    def upgrade_plan(self, user_id: int, new_plan: str) -> bool:
        """Upgrade user's plan"""
        if new_plan not in PRICING_TIERS:
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        conn = sqlite3.connect('mornGPT_api.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE users SET plan = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_plan, user_id)
            )
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

# Global billing manager instance
billing_manager = BillingManager() 