# mornGPT Fullstack Architecture & Cost Analysis

## 🏗️ **System Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Load Balancer │
│   (React/Vue)   │◄──►│   (Kong/Nginx)  │◄──►│   (AWS ALB)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Redis Cache   │    │   Message Queue │
│   Application   │◄──►│   (Rate Limiting)│◄──►│   (RabbitMQ)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   MongoDB       │    │   Vector DB     │
│   (User Data)   │    │   (Analytics)   │    │   (Embeddings)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GPT-4 API     │    │   Claude API    │    │   Gemini API    │
│   (OpenAI)      │    │   (Anthropic)   │    │   (Google)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🗄️ **Database Architecture**

### **Primary Database: PostgreSQL**
```sql
-- Users and Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    plan VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    stripe_customer_id VARCHAR(255),
    subscription_status VARCHAR(50) DEFAULT 'active'
);

-- API Keys
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    api_key VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    permissions JSONB DEFAULT '{}'
);

-- Usage Tracking
CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    api_key_id INTEGER REFERENCES api_keys(id),
    module VARCHAR(100) NOT NULL,
    model_version INTEGER NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cost_per_token DECIMAL(10,6) NOT NULL,
    total_cost DECIMAL(10,4) NOT NULL,
    processing_time_ms INTEGER,
    status VARCHAR(50) DEFAULT 'success',
    request_data JSONB,
    response_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Billing Cycles
CREATE TABLE billing_cycles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    cycle_start TIMESTAMP NOT NULL,
    cycle_end TIMESTAMP NOT NULL,
    plan VARCHAR(50) NOT NULL,
    monthly_fee DECIMAL(10,2) NOT NULL,
    usage_cost DECIMAL(10,2) DEFAULT 0,
    total_bill DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active',
    stripe_invoice_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    billing_cycle_id INTEGER REFERENCES billing_cycles(id),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(50),
    stripe_payment_intent_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Rate Limiting
CREATE TABLE rate_limits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    window_type VARCHAR(20) NOT NULL, -- minute, hour, day
    window_start TIMESTAMP NOT NULL,
    request_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, window_type, window_start)
);

-- Module Configurations
CREATE TABLE module_configs (
    id SERIAL PRIMARY KEY,
    module_name VARCHAR(100) NOT NULL,
    model_version INTEGER NOT NULL,
    gpt_model VARCHAR(50) NOT NULL, -- gpt-4, gpt-3.5-turbo, claude-3, gemini-pro
    cost_per_1k_tokens DECIMAL(10,6) NOT NULL,
    max_tokens INTEGER DEFAULT 4000,
    temperature DECIMAL(3,2) DEFAULT 0.7,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(module_name, model_version)
);

-- User Sessions
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Analytics Database: MongoDB**
```javascript
// Usage Analytics Collection
{
  "_id": ObjectId,
  "user_id": Number,
  "date": Date,
  "module": String,
  "model_version": Number,
  "gpt_model": String,
  "total_calls": Number,
  "total_tokens": Number,
  "total_cost": Number,
  "avg_response_time": Number,
  "success_rate": Number,
  "error_count": Number,
  "hourly_breakdown": [
    {
      "hour": Number,
      "calls": Number,
      "tokens": Number,
      "cost": Number
    }
  ]
}

// Performance Metrics Collection
{
  "_id": ObjectId,
  "timestamp": Date,
  "module": String,
  "gpt_model": String,
  "avg_response_time": Number,
  "p95_response_time": Number,
  "p99_response_time": Number,
  "success_rate": Number,
  "error_rate": Number,
  "rate_limit_hits": Number,
  "total_requests": Number
}

// Cost Analysis Collection
{
  "_id": ObjectId,
  "user_id": Number,
  "period": String, // daily, weekly, monthly
  "start_date": Date,
  "end_date": Date,
  "total_cost": Number,
  "cost_by_module": {
    "growth_advisory": Number,
    "interview_job": Number,
    // ... other modules
  },
  "cost_by_gpt_model": {
    "gpt-4": Number,
    "gpt-3.5-turbo": Number,
    "claude-3": Number,
    "gemini-pro": Number
  },
  "efficiency_metrics": {
    "cost_per_call": Number,
    "tokens_per_call": Number,
    "calls_per_dollar": Number
  }
}
```

### **Vector Database: Pinecone/Weaviate**
```python
# Embeddings for semantic search and context
{
  "id": "embedding_id",
  "user_id": 123,
  "module": "growth_advisory",
  "content_type": "request", # request, response, context
  "content": "text content",
  "embedding": [0.1, 0.2, 0.3, ...], # 1536-dimensional vector
  "metadata": {
    "business_type": "SaaS",
    "target_market": "enterprise",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

## 💰 **Detailed Cost Analysis**

### **Infrastructure Costs (Monthly)**

#### **AWS Infrastructure**
| Service | Specification | Monthly Cost |
|---------|---------------|--------------|
| **EC2 (API Servers)** | 4x t3.large (2 vCPU, 8GB RAM) | $280 |
| **RDS PostgreSQL** | db.t3.large (2 vCPU, 8GB RAM) | $150 |
| **ElastiCache Redis** | cache.t3.micro | $15 |
| **Application Load Balancer** | Standard | $20 |
| **CloudFront CDN** | 1TB transfer | $85 |
| **S3 Storage** | 100GB + requests | $3 |
| **CloudWatch** | Monitoring | $10 |
| **Route 53** | DNS | $1 |
| **Total AWS** | | **$564** |

#### **Additional Services**
| Service | Monthly Cost |
|---------|--------------|
| **MongoDB Atlas** (M10 cluster) | $57 |
| **Pinecone** (Starter plan) | $20 |
| **RabbitMQ Cloud** | $20 |
| **Stripe** (0.029% + $0.30 per transaction) | Variable |
| **Total Additional** | **$97** |

#### **GPT Model Costs (10K calls/month)**
| Model Mix | Cost per Call | Monthly Cost |
|-----------|---------------|--------------|
| 70% GPT-3.5 + 30% GPT-4 | $0.042 | $420 |
| 50% GPT-3.5 + 50% GPT-4 | $0.070 | $700 |
| 100% GPT-4 | $0.135 | $1,350 |

### **Revenue Projections**

#### **Pricing Strategy**
- **Free Tier**: 100 calls/month, $0
- **Starter**: 1,000 calls/month, $9.99 + usage
- **Professional**: 10,000 calls/month, $49.99 + usage
- **Enterprise**: 100,000 calls/month, $199.99 + usage

#### **Revenue Calculation (1,000 customers)**
| Plan | Customers | Base Revenue | Usage Revenue | Total |
|------|-----------|--------------|---------------|-------|
| Free | 400 | $0 | $0 | $0 |
| Starter | 400 | $3,996 | $8,000 | $11,996 |
| Professional | 150 | $7,499 | $15,000 | $22,499 |
| Enterprise | 50 | $9,999 | $25,000 | $34,999 |
| **Total** | **1,000** | **$21,494** | **$48,000** | **$69,494** |

### **Profitability Analysis**

#### **Monthly Costs (10K calls, mixed models)**
- Infrastructure: $661
- GPT Models: $420
- **Total Costs**: $1,081

#### **Monthly Revenue (1,000 customers)**
- **Total Revenue**: $69,494
- **Profit Margin**: 98.4%

## 🚀 **Deployment Architecture**

### **Production Environment**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # API Application
  api:
    image: morngpt-api:latest
    deploy:
      replicas: 4
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/morngpt
      - REDIS_URL=redis://redis:6379
      - MONGODB_URL=mongodb://mongo:27017/morngpt
    depends_on:
      - db
      - redis
      - mongo

  # Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=morngpt
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Cache
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  # Analytics DB
  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db

  # Message Queue
  rabbitmq:
    image: rabbitmq:3-management
    environment:
      - RABBITMQ_DEFAULT_USER=user
      - RABBITMQ_DEFAULT_PASS=pass

  # Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

volumes:
  postgres_data:
  redis_data:
  mongo_data:
```

### **Kubernetes Deployment**
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: morngpt-api
spec:
  replicas: 4
  selector:
    matchLabels:
      app: morngpt-api
  template:
    metadata:
      labels:
        app: morngpt-api
    spec:
      containers:
      - name: api
        image: morngpt-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

## 🔧 **Development Environment**

### **Local Development Setup**
```bash
# Install dependencies
pip install -r api/requirements.txt
npm install -g @vue/cli  # or create-react-app

# Start services with Docker
docker-compose -f docker-compose.dev.yml up -d

# Run API server
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run frontend
cd frontend
npm run serve
```

### **Environment Variables**
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/morngpt
MONGODB_URL=mongodb://localhost:27017/morngpt
REDIS_URL=redis://localhost:6379

# GPT APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Payment
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Monitoring
SENTRY_DSN=https://...
```

## 📊 **Monitoring & Analytics**

### **Key Metrics to Track**
- API response times (p50, p95, p99)
- Error rates by module and GPT model
- Cost per call and cost efficiency
- User engagement and retention
- Revenue per user (ARPU)
- Customer acquisition cost (CAC)

### **Alerting Setup**
```yaml
# prometheus-alerts.yaml
groups:
- name: morngpt-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected

  - alert: HighCostPerCall
    expr: cost_per_call > 0.20
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Cost per call is above threshold
```

## 🎯 **Optimization Strategies**

### **Cost Optimization**
1. **Model Selection**: Use GPT-3.5 for simple tasks, GPT-4 for complex ones
2. **Caching**: Cache common responses to reduce API calls
3. **Token Optimization**: Implement smart prompt engineering
4. **Batch Processing**: Group similar requests
5. **Rate Limiting**: Prevent abuse and unnecessary costs

### **Performance Optimization**
1. **Database Indexing**: Optimize query performance
2. **Connection Pooling**: Efficient database connections
3. **CDN**: Cache static content globally
4. **Load Balancing**: Distribute traffic evenly
5. **Auto-scaling**: Scale based on demand

This architecture provides a scalable, cost-effective foundation for the commercial mornGPT API with realistic cost projections and revenue potential. 