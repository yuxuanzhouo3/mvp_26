# mornGPT Commercial API

A comprehensive commercial API system for monetizing mornGPT AI modules with authentication, billing, rate limiting, and analytics.

## 🚀 Features

### Core Features
- **Authentication & Authorization**: JWT tokens and API key management
- **Rate Limiting**: Plan-based rate limiting with multiple time windows
- **Billing & Payments**: Usage tracking, billing cycles, and payment processing
- **Analytics**: Comprehensive usage analytics and reporting
- **Multi-Module Support**: All 15 mornGPT modules with version control (1-9)

### Pricing Tiers
- **Free**: 100 calls/month, $0.00 per call
- **Starter**: 1,000 calls/month, $0.01 per call, $9.99/month
- **Professional**: 10,000 calls/month, $0.005 per call, $49.99/month
- **Enterprise**: 100,000 calls/month, $0.002 per call, $199.99/month

### Module Pricing
Each module has additional costs per call:
- Growth Advisory: $0.02
- Interview/Job: $0.015
- AI Coder: $0.025
- Content Detection: $0.03
- Medical Advice: $0.04
- Multi-GPT: $0.035
- Housing: $0.02
- Person Matching: $0.025
- Teacher/Coach: $0.02
- Traveling: $0.02
- Product Search: $0.015
- Clothing: $0.02
- Restaurant/Food: $0.02
- Content Generation: $0.05
- Anti-AI Protection: $0.10

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/api-keys` - Create API key
- `GET /api/auth/api-keys` - List API keys
- `DELETE /api/auth/api-keys/{key_id}` - Revoke API key
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/validate` - Validate token

### Billing & Usage
- `GET /api/billing/usage` - Get usage statistics
- `GET /api/billing/current-cycle` - Get current billing cycle
- `GET /api/billing/bill/{cycle_id}` - Calculate bill
- `POST /api/billing/pay` - Process payment
- `GET /api/billing/payments` - Get payment history
- `POST /api/billing/upgrade` - Upgrade plan
- `GET /api/billing/pricing` - Get pricing information
- `GET /api/billing/analytics` - Get analytics
- `GET /api/billing/limits` - Get rate limits

### Analytics
- `GET /api/analytics/overview` - Get analytics overview
- `GET /api/analytics/module-breakdown` - Get module usage breakdown
- `GET /api/analytics/usage-trend` - Get usage trend over time
- `GET /api/analytics/performance` - Get API performance metrics
- `GET /api/analytics/cost-analysis` - Get cost analysis
- `GET /api/analytics/export` - Export analytics data

### Module Endpoints
Each module has its own endpoints:

#### Growth Advisory
- `POST /api/growth_advisory/analyze` - Analyze growth opportunities
- `POST /api/growth_advisory/market-research` - Conduct market research
- `POST /api/growth_advisory/strategy-development` - Develop growth strategy
- `GET /api/growth_advisory/models` - Get available model versions

#### Other Modules (Coming Soon)
- Interview/Job: `/api/interview_job/`
- AI Coder: `/api/coder/`
- Content Detection: `/api/content_detection/`
- Medical Advice: `/api/medical_advice/`
- Multi-GPT: `/api/multi_gpt/`
- Housing: `/api/housing/`
- Person Matching: `/api/person_matching/`
- Teacher/Coach: `/api/teacher_coach/`
- Traveling: `/api/traveling/`
- Product Search: `/api/product_search/`
- Clothing: `/api/clothing/`
- Restaurant/Food: `/api/restaurant_food/`
- Content Generation: `/api/content_generation/`
- Anti-AI Protection: `/api/anti_ai_protection/`

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd mvp_26

# Install API dependencies
cd api
pip install -r requirements.txt

# Run the API server
python main.py
```

### Environment Variables
Create a `.env` file in the `api/` directory:
```env
# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256

# Database
DATABASE_URL=sqlite:///mornGPT_api.db

# Payment Processing
STRIPE_SECRET_KEY=your-stripe-secret-key
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_SECRET=your-paypal-secret

# Rate Limiting
REDIS_URL=redis://localhost:6379  # Optional

# Logging
LOG_LEVEL=INFO
```

## 📖 Usage Examples

### 1. Register and Get API Key
```bash
# Register a new user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "company_name": "Example Corp"
  }'

# Login to get access token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'

# Create API key
curl -X POST "http://localhost:8000/api/auth/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Production API Key"}'
```

### 2. Use Growth Advisory Module
```bash
# Analyze growth opportunities
curl -X POST "http://localhost:8000/api/growth_advisory/analyze" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "business_type": "SaaS",
    "target_market": "Small businesses",
    "current_challenges": ["Customer acquisition", "Scaling"],
    "budget_range": "$10k-50k",
    "model_version": 3
  }'
```

### 3. Check Usage and Billing
```bash
# Get usage statistics
curl -X GET "http://localhost:8000/api/billing/usage" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Get analytics overview
curl -X GET "http://localhost:8000/api/analytics/overview?period=30d" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 🔒 Security

### Authentication
- JWT tokens for session management
- API keys for programmatic access
- Password hashing with SHA-256
- Token expiration and refresh

### Rate Limiting
- Per-minute, per-hour, and per-day limits
- Plan-based rate limiting
- Automatic rate limit enforcement
- Rate limit headers in responses

### Data Protection
- Input validation with Pydantic
- SQL injection prevention
- CORS configuration
- Error handling without sensitive data exposure

## 💰 Billing & Payments

### Usage Tracking
- Automatic usage tracking per API call
- Module-specific pricing
- Plan-based pricing tiers
- Real-time cost calculation

### Payment Processing
- Stripe integration (ready for implementation)
- PayPal integration (ready for implementation)
- Payment history tracking
- Billing cycle management

### Analytics & Reporting
- Usage analytics by module
- Cost analysis and projections
- Performance metrics
- Export capabilities (JSON/CSV)

## 🚀 Deployment

### Development
```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Using Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using Docker (Dockerfile provided)
docker build -t morngpt-api .
docker run -p 8000:8000 morngpt-api
```

### Environment Setup
- Use environment variables for configuration
- Set up proper database connections
- Configure payment gateway credentials
- Set up monitoring and logging

## 📊 Monitoring & Analytics

### Built-in Analytics
- API usage tracking
- Cost analysis
- Performance metrics
- Rate limit monitoring

### Integration Ready
- Prometheus metrics
- Structured logging
- Health check endpoints
- Performance monitoring

## 🔧 Development

### Project Structure
```
api/
├── main.py                 # FastAPI application
├── auth.py                 # Authentication system
├── billing.py              # Billing and payments
├── rate_limiter.py         # Rate limiting
├── models.py               # Pydantic models
├── routers/                # API route modules
│   ├── auth_router.py
│   ├── billing_router.py
│   ├── analytics_router.py
│   └── growth_advisory_router.py
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Adding New Modules
1. Create module router in `routers/`
2. Add module to pricing configuration
3. Update rate limiting if needed
4. Add module to main.py imports
5. Update documentation

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=api

# Run specific test
pytest tests/test_auth.py
```

## 📈 Roadmap

### Phase 1 (Current)
- ✅ Core API infrastructure
- ✅ Authentication system
- ✅ Billing and rate limiting
- ✅ Growth Advisory module
- ✅ Analytics and reporting

### Phase 2 (Q1 2025)
- 🔄 All 15 modules implemented
- 🔄 Payment gateway integration
- 🔄 Advanced analytics
- 🔄 Webhook system

### Phase 3 (Q2 2025)
- 🔄 White-label solutions
- 🔄 Custom integrations
- 🔄 Advanced security features
- 🔄 Global deployment

## 🤝 Support

### Documentation
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- OpenAPI spec: `http://localhost:8000/openapi.json`

### Contact
- Email: support@morngpt.com
- Documentation: https://docs.morngpt.com
- GitHub Issues: https://github.com/your-repo/issues

## 📄 License

Copyright © 2025 Yuxuan Zhou. All rights reserved.

This project is proprietary software. Unauthorized copying, distribution, or use is strictly prohibited. 