# Productization Guide: NER and Intent Classification Models

**Date:** December 20, 2024  
**Status:** Production Readiness Checklist  
**Models:** NER (565 labels) + Intent (3,040 labels)

---

## 📋 Table of Contents

1. [Pre-Production Checklist](#pre-production-checklist)
2. [Model Optimization](#model-optimization)
3. [API Development](#api-development)
4. [Testing & Validation](#testing--validation)
5. [Deployment Infrastructure](#deployment-infrastructure)
6. [Monitoring & Observability](#monitoring--observability)
7. [Security & Compliance](#security--compliance)
8. [Documentation](#documentation)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [Performance Optimization](#performance-optimization)
11. [Scaling Strategy](#scaling-strategy)
12. [Maintenance & Updates](#maintenance--updates)

---

## 1. Pre-Production Checklist

### ✅ Model Quality Requirements

- [ ] **Entity Extraction Performance:**
  - [ ] Recall ≥ 70% (Current: ~35% - **NEEDS IMPROVEMENT**)
  - [ ] Precision ≥ 85% (Current: ~85% - ✅ **PASS**)
  - [ ] F1 Score ≥ 75% (Current: ~55% - **NEEDS IMPROVEMENT**)

- [ ] **Intent Classification Performance:**
  - [ ] Precision ≥ 90% (Current: ~95% - ✅ **PASS**)
  - [ ] Recall ≥ 90% (Current: ~95% - ✅ **PASS**)
  - [ ] F1 Score ≥ 90% (Current: ~95% - ✅ **PASS**)

- [ ] **Critical Entity Types:**
  - [ ] IP_ADDRESS detection ≥ 80%
  - [ ] LLM_MODEL detection ≥ 80%
  - [ ] EMAIL_ADDRESS detection ≥ 80%
  - [ ] DOMAIN detection ≥ 80%
  - [ ] THREAT_ACTOR detection ≥ 70%

- [ ] **Mislabeling Fixes:**
  - [ ] Fix "evil.com" → TIME (should be DOMAIN)
  - [ ] Fix "Optimize" → TOOL (false positive)
  - [ ] Fix "NIST" → FRAMEWORK (should be COMPLIANCE_FRAMEWORK)

### ✅ Code Quality

- [ ] Code review completed
- [ ] Unit tests ≥ 80% coverage
- [ ] Integration tests passing
- [ ] Documentation complete
- [ ] Error handling implemented
- [ ] Logging configured

### ✅ Security

- [ ] Input validation implemented
- [ ] Rate limiting configured
- [ ] Authentication/authorization
- [ ] Data encryption (in transit & at rest)
- [ ] PII handling compliance
- [ ] Security audit completed

---

## 2. Model Optimization

### 2.1 Improve Entity Extraction

**Priority: HIGH** (Current recall: ~35%, Target: ≥70%)

```python
# Steps to improve:
1. Add 1000+ training examples for top missed types:
   - LLM_MODEL: 500+ examples
   - IP_ADDRESS: 300+ examples
   - EMAIL_ADDRESS: 200+ examples
   - Social media entities: 200+ examples
   - Coordinates: 200+ examples

2. Fix mislabeling with negative examples:
   - Add 100+ negative examples for false positives
   - Add examples showing correct labels

3. Retrain model with improved data
4. Validate on test suite
5. Iterate until recall ≥ 70%
```

### 2.2 Model Size Optimization

```python
# Options:
1. Quantization (reduce model size by 50-75%)
2. Pruning (remove unused components)
3. Distillation (create smaller student model)
4. ONNX conversion (faster inference)
```

### 2.3 Inference Speed

```python
# Targets:
- P50 latency: < 50ms per query
- P95 latency: < 200ms per query
- P99 latency: < 500ms per query
- Throughput: ≥ 100 queries/second
```

---

## 3. API Development

### 3.1 API Framework Selection

**Recommended: FastAPI** (Python)

```python
# Why FastAPI:
- Fast performance (async support)
- Automatic OpenAPI documentation
- Type validation
- Easy to deploy
- Great for ML models
```

### 3.2 API Structure

```
api/
├── main.py                 # FastAPI app
├── models/
│   ├── ner_model.py        # NER model wrapper
│   └── intent_model.py     # Intent model wrapper
├── routers/
│   ├── entities.py         # Entity extraction endpoints
│   ├── intents.py          # Intent classification endpoints
│   └── batch.py            # Batch processing endpoints
├── schemas/
│   ├── request.py          # Request models
│   └── response.py         # Response models
├── middleware/
│   ├── auth.py             # Authentication
│   ├── rate_limit.py       # Rate limiting
│   └── logging.py          # Request logging
├── utils/
│   ├── validation.py       # Input validation
│   └── errors.py           # Error handling
└── tests/
    ├── test_api.py
    └── test_models.py
```

### 3.3 API Endpoints

```python
# Core Endpoints:

POST /api/v1/entities/extract
POST /api/v1/intents/classify
POST /api/v1/analyze          # Combined entities + intents
POST /api/v1/batch/process    # Batch processing

# Health & Monitoring:
GET  /health
GET  /metrics
GET  /docs                     # OpenAPI docs
```

### 3.4 Example API Implementation

```python
# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import entities, intents, batch
from middleware import auth, rate_limit, logging

app = FastAPI(
    title="NER & Intent Classification API",
    version="1.0.0",
    description="Production API for entity extraction and intent classification"
)

# Middleware
app.add_middleware(CORSMiddleware, ...)
app.middleware("http")(auth.authenticate)
app.middleware("http")(rate_limit.rate_limit)
app.middleware("http")(logging.log_requests)

# Routers
app.include_router(entities.router, prefix="/api/v1/entities")
app.include_router(intents.router, prefix="/api/v1/intents")
app.include_router(batch.router, prefix="/api/v1/batch")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": True}
```

---

## 4. Testing & Validation

### 4.1 Test Suite Requirements

```python
# tests/
├── unit/
│   ├── test_entity_extraction.py
│   ├── test_intent_classification.py
│   └── test_validation.py
├── integration/
│   ├── test_api_endpoints.py
│   ├── test_batch_processing.py
│   └── test_error_handling.py
├── performance/
│   ├── test_latency.py
│   ├── test_throughput.py
│   └── test_concurrent_requests.py
└── e2e/
    ├── test_production_scenarios.py
    └── test_user_workflows.py
```

### 4.2 Test Coverage Targets

- Unit tests: ≥ 80%
- Integration tests: ≥ 70%
- E2E tests: Critical paths only
- Performance tests: All endpoints

### 4.3 Validation Tests

```python
# Test critical entity types:
- IP_ADDRESS: 100 test cases
- LLM_MODEL: 100 test cases
- EMAIL_ADDRESS: 100 test cases
- DOMAIN: 100 test cases
- THREAT_ACTOR: 50 test cases

# Test edge cases:
- Empty input
- Very long input (>10,000 chars)
- Special characters
- Unicode/emojis
- Malformed data
```

---

## 5. Deployment Infrastructure

### 5.1 Containerization

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Copy models
COPY cyber-train/models/ner_model/model-best /app/models/ner_model/
COPY cyber-train/models/intent_model/model-best /app/models/intent_model/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 5.2 Orchestration Options

**Option 1: Kubernetes (Recommended for scale)**
- Deployments
- Services
- Ingress
- Horizontal Pod Autoscaler
- ConfigMaps & Secrets

**Option 2: Docker Swarm (Simpler)**
- Services
- Stacks
- Load balancing

**Option 3: Cloud Services**
- AWS: ECS/EKS, Lambda
- GCP: Cloud Run, GKE
- Azure: Container Instances, AKS

### 5.3 Infrastructure as Code

```bash
# Terraform example for AWS
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── ecs.tf
├── alb.tf
└── rds.tf
```

---

## 6. Monitoring & Observability

### 6.1 Metrics to Track

**Performance Metrics:**
- Request latency (P50, P95, P99)
- Throughput (requests/second)
- Error rate
- Model inference time
- Queue depth (if using queues)

**Business Metrics:**
- Entity extraction accuracy
- Intent classification accuracy
- API usage by endpoint
- User satisfaction scores

**System Metrics:**
- CPU usage
- Memory usage
- Disk I/O
- Network I/O
- Model loading time

### 6.2 Logging

```python
# Structured logging with JSON
import logging
import json

logger = logging.getLogger(__name__)

def log_request(request_id, endpoint, latency, entities_found, intents_found):
    logger.info(json.dumps({
        "request_id": request_id,
        "endpoint": endpoint,
        "latency_ms": latency,
        "entities_count": entities_found,
        "intents_count": intents_found,
        "timestamp": datetime.utcnow().isoformat()
    }))
```

### 6.3 Monitoring Tools

**Recommended Stack:**
- **Metrics:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana) or Loki
- **Tracing:** Jaeger or Zipkin
- **APM:** New Relic, Datadog, or Sentry

### 6.4 Alerting

```yaml
# Alert rules
alerts:
  - name: HighErrorRate
    condition: error_rate > 5%
    severity: critical
    
  - name: HighLatency
    condition: p95_latency > 500ms
    severity: warning
    
  - name: ModelLoadFailure
    condition: model_load_failed == true
    severity: critical
    
  - name: LowAccuracy
    condition: entity_recall < 50%
    severity: warning
```

---

## 7. Security & Compliance

### 7.1 Security Requirements

- [ ] **Authentication:**
  - API keys or OAuth 2.0
  - JWT tokens
  - Rate limiting per user

- [ ] **Authorization:**
  - Role-based access control (RBAC)
  - Endpoint-level permissions

- [ ] **Input Validation:**
  - Sanitize all inputs
  - Max input length limits
  - Regex validation

- [ ] **Data Protection:**
  - Encrypt data in transit (TLS 1.3)
  - Encrypt data at rest
  - PII handling compliance (GDPR, CCPA)

- [ ] **Vulnerability Management:**
  - Regular security scans
  - Dependency updates
  - Penetration testing

### 7.2 Compliance

- [ ] GDPR compliance (if handling EU data)
- [ ] CCPA compliance (if handling CA data)
- [ ] HIPAA compliance (if handling healthcare data)
- [ ] SOC 2 Type II (if required)
- [ ] ISO 27001 (if required)

---

## 8. Documentation

### 8.1 API Documentation

- [ ] OpenAPI/Swagger specification
- [ ] Endpoint descriptions
- [ ] Request/response examples
- [ ] Error codes and messages
- [ ] Authentication guide
- [ ] Rate limiting documentation

### 8.2 User Documentation

- [ ] Quick start guide
- [ ] Integration examples
- [ ] SDK documentation (if applicable)
- [ ] Best practices
- [ ] Troubleshooting guide
- [ ] FAQ

### 8.3 Developer Documentation

- [ ] Architecture overview
- [ ] Model details
- [ ] Deployment guide
- [ ] Contributing guidelines
- [ ] Changelog

---

## 9. CI/CD Pipeline

### 9.1 Pipeline Stages

```yaml
# .github/workflows/deploy.yml
stages:
  1. Lint & Format
  2. Unit Tests
  3. Integration Tests
  4. Security Scan
  5. Build Docker Image
  6. Push to Registry
  7. Deploy to Staging
  8. E2E Tests
  9. Deploy to Production (manual approval)
```

### 9.2 CI/CD Tools

**Recommended:**
- **CI:** GitHub Actions, GitLab CI, Jenkins
- **CD:** ArgoCD, Flux, Spinnaker
- **Container Registry:** Docker Hub, AWS ECR, GCR

### 9.3 Automated Testing

```bash
# Pre-deployment checks:
- Run test suite
- Check code coverage
- Security vulnerability scan
- Performance benchmarks
- Model validation
```

---

## 10. Performance Optimization

### 10.1 Caching Strategy

```python
# Cache frequently used queries
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_entity_extraction(text_hash, text):
    return extract_entities(text)

def extract_with_cache(text):
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return cached_entity_extraction(text_hash, text)
```

### 10.2 Async Processing

```python
# Use async for I/O-bound operations
from fastapi import BackgroundTasks

@app.post("/api/v1/batch/process")
async def process_batch(queries: List[str], background_tasks: BackgroundTasks):
    # Process in background
    background_tasks.add_task(process_batch_async, queries)
    return {"status": "processing"}
```

### 10.3 Model Optimization

- [ ] Model quantization
- [ ] Batch inference
- [ ] GPU acceleration (if available)
- [ ] Model caching in memory
- [ ] Lazy model loading

---

## 11. Scaling Strategy

### 11.1 Horizontal Scaling

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nlp-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nlp-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 11.2 Load Balancing

- [ ] Application Load Balancer (ALB)
- [ ] Round-robin or least-connections
- [ ] Health checks
- [ ] Session affinity (if needed)

### 11.3 Database/Storage

- [ ] Redis for caching
- [ ] PostgreSQL/MySQL for metadata
- [ ] S3/GCS for model storage
- [ ] CDN for static assets

---

## 12. Maintenance & Updates

### 12.1 Model Updates

```python
# Versioning strategy:
models/
├── ner_model/
│   ├── v1.0.0/
│   ├── v1.1.0/
│   └── latest -> v1.1.0
└── intent_model/
    ├── v1.0.0/
    ├── v1.1.0/
    └── latest -> v1.1.0
```

### 12.2 Update Process

1. Train new model version
2. Validate on test suite
3. Deploy to staging
4. A/B test with production traffic
5. Gradual rollout (10% → 50% → 100%)
6. Monitor metrics
7. Rollback if issues detected

### 12.3 Maintenance Schedule

- **Daily:** Monitor metrics and alerts
- **Weekly:** Review error logs
- **Monthly:** Model performance review
- **Quarterly:** Model retraining
- **Annually:** Security audit

---

## 📊 Production Readiness Scorecard

| Category | Current | Target | Status |
|----------|---------|--------|--------|
| **Model Quality** | 55% | 75% | ⚠️ Needs Work |
| **API Development** | 0% | 100% | ❌ Not Started |
| **Testing** | 30% | 80% | ⚠️ Needs Work |
| **Infrastructure** | 0% | 100% | ❌ Not Started |
| **Monitoring** | 0% | 100% | ❌ Not Started |
| **Security** | 20% | 100% | ⚠️ Needs Work |
| **Documentation** | 60% | 90% | ⚠️ Needs Work |
| **CI/CD** | 0% | 100% | ❌ Not Started |

**Overall Readiness: 28%** ⚠️ **Not Production Ready**

---

## 🚀 Quick Start: Production Deployment

### Step 1: Improve Model Quality (2-4 weeks)
```bash
# Priority: Fix entity extraction recall
1. Add training examples for missed entities
2. Fix mislabeling errors
3. Retrain models
4. Validate on test suite
5. Target: Recall ≥ 70%
```

### Step 2: Build API (1-2 weeks)
```bash
1. Set up FastAPI project structure
2. Implement core endpoints
3. Add authentication/authorization
4. Add input validation
5. Add error handling
```

### Step 3: Testing (1 week)
```bash
1. Write unit tests
2. Write integration tests
3. Write E2E tests
4. Performance testing
5. Security testing
```

### Step 4: Infrastructure (1-2 weeks)
```bash
1. Containerize application
2. Set up Kubernetes/ECS
3. Configure load balancer
4. Set up monitoring
5. Configure logging
```

### Step 5: Deployment (1 week)
```bash
1. Deploy to staging
2. Run E2E tests
3. Deploy to production
4. Monitor metrics
5. Gradual rollout
```

**Total Estimated Time: 6-10 weeks**

---

## 📝 Next Steps

1. **Immediate (Week 1-2):**
   - [ ] Improve entity extraction recall to ≥70%
   - [ ] Fix critical mislabeling errors
   - [ ] Set up basic API structure

2. **Short-term (Week 3-4):**
   - [ ] Complete API development
   - [ ] Write comprehensive tests
   - [ ] Set up CI/CD pipeline

3. **Medium-term (Week 5-8):**
   - [ ] Deploy to staging environment
   - [ ] Set up monitoring and alerting
   - [ ] Security audit

4. **Long-term (Week 9-10):**
   - [ ] Production deployment
   - [ ] Gradual rollout
   - [ ] Monitor and optimize

---

**Status:** 📋 **Productization Guide Complete**

This guide provides a comprehensive roadmap for productizing your NLP models. Focus on improving model quality first, then build the infrastructure and deployment pipeline.

