# Deployment Guide - Stasik v2.0

## 🚀 Deployment Overview

This guide covers deployment strategies for Stasik in various environments, from development to production-scale enterprise deployments.

---

## 🏠 Local Development Deployment

### Quick Development Setup
```bash
# Clone and setup
git clone https://github.com/nayshtetik/Stasik.git
cd Stasik
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Development configuration
cp config/config.yaml.example config/config.yaml
export STASIK_MODE="development"
export STASIK_DEBUG="true"

# Run development server
python debugging_chat_with_tracking.py
```

### Development Configuration
```yaml
# config/development.yaml
stasik:
  mode: "development"
  debug: true
  log_level: "DEBUG"
  auto_reload: true
  cache_disabled: true
  
development:
  hot_reload: true
  verbose_logging: true
  skip_auth: true
  mock_apis: false
```

---

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 stasik && chown -R stasik:stasik /app
USER stasik

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD python -c "from debugging_chat_with_tracking import DebuggingStasikChat; DebuggingStasikChat()" || exit 1

# Run application
CMD ["python", "debugging_chat_with_tracking.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  stasik:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SERPAPI_KEY=${SERPAPI_KEY}
      - STASIK_MODE=production
    volumes:
      - ./config:/app/config:ro
      - ./logs:/app/logs
      - knowledge_base:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - stasik
    restart: unless-stopped

volumes:
  knowledge_base:
  redis_data:
```

### Build and Deploy
```bash
# Build image
docker build -t stasik:2.0 .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f stasik

# Scale horizontally
docker-compose up -d --scale stasik=3
```

---

## ☁️ Cloud Deployments

### AWS Deployment

#### **AWS ECS (Elastic Container Service)**
```json
{
  "family": "stasik-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "stasik",
      "image": "your-registry/stasik:2.0",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "STASIK_MODE",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:stasik/openai"
        },
        {
          "name": "SERPAPI_KEY", 
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:stasik/serpapi"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/stasik",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### **AWS Lambda (Serverless)**
```python
# lambda_handler.py
import json
from debugging_chat_with_tracking import DebuggingStasikChat

# Initialize once (outside handler for container reuse)
stasik_chat = None

def lambda_handler(event, context):
    global stasik_chat
    
    if stasik_chat is None:
        stasik_chat = DebuggingStasikChat()
    
    query = json.loads(event['body'])['query']
    response = stasik_chat.process_query(query)
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'response': response,
            'timestamp': context.aws_request_id
        })
    }
```

### Google Cloud Platform

#### **Cloud Run Deployment**
```yaml
# cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: stasik
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/memory: "2Gi"
        run.googleapis.com/cpu: "1000m"
    spec:
      containerConcurrency: 10
      containers:
      - image: gcr.io/PROJECT-ID/stasik:2.0
        ports:
        - containerPort: 8000
        env:
        - name: STASIK_MODE
          value: "production"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: stasik-secrets
              key: openai-key
        - name: SERPAPI_KEY
          valueFrom:
            secretKeyRef:
              name: stasik-secrets
              key: serpapi-key
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

```bash
# Deploy to Cloud Run
gcloud run deploy stasik \
  --image gcr.io/PROJECT-ID/stasik:2.0 \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 1 \
  --max-instances 10 \
  --allow-unauthenticated
```

### Microsoft Azure

#### **Azure Container Instances**
```json
{
  "apiVersion": "2021-03-01",
  "type": "Microsoft.ContainerInstance/containerGroups",
  "name": "stasik-container-group",
  "location": "East US",
  "properties": {
    "containers": [
      {
        "name": "stasik",
        "properties": {
          "image": "your-registry.azurecr.io/stasik:2.0",
          "resources": {
            "requests": {
              "cpu": 1.0,
              "memoryInGb": 2.0
            }
          },
          "ports": [
            {
              "port": 8000,
              "protocol": "TCP"
            }
          ],
          "environmentVariables": [
            {
              "name": "STASIK_MODE",
              "value": "production"
            }
          ]
        }
      }
    ],
    "osType": "Linux",
    "ipAddress": {
      "type": "Public",
      "ports": [
        {
          "protocol": "TCP",
          "port": 8000
        }
      ]
    }
  }
}
```

---

## 🔧 Production Configuration

### Production Settings
```yaml
# config/production.yaml
stasik:
  mode: "production"
  debug: false
  log_level: "INFO"
  
production:
  # Performance
  workers: 4
  max_requests: 1000
  timeout: 30
  keepalive: 2
  
  # Security
  ssl_enabled: true
  cors_origins: ["https://yourdomain.com"]
  api_key_required: true
  rate_limiting: true
  
  # Monitoring
  metrics_enabled: true
  health_checks: true
  error_tracking: true
  
  # Caching
  redis_url: "redis://redis:6379/0"
  cache_ttl: 3600
  
  # Knowledge base
  kb_readonly: true
  kb_backup: true
  kb_compression: true
```

### Environment Variables
```bash
# Production environment variables
export STASIK_MODE="production"
export STASIK_DEBUG="false"
export STASIK_LOG_LEVEL="INFO"
export STASIK_WORKERS="4"
export STASIK_MAX_REQUESTS="1000"

# API keys (use secure secret management)
export OPENAI_API_KEY="sk-production-key"
export SERPAPI_KEY="production-serpapi-key"

# Database and caching
export REDIS_URL="redis://redis-cluster:6379/0"
export DATABASE_URL="postgresql://user:pass@db:5432/stasik"

# Security
export SECRET_KEY="your-secret-key-here"
export CORS_ORIGINS="https://yourdomain.com,https://api.yourdomain.com"
```

---

## 📊 Monitoring & Observability

### Health Checks
```python
# health.py
from flask import Flask, jsonify
from debugging_chat_with_tracking import DebuggingStasikChat

app = Flask(__name__)
stasik_chat = DebuggingStasikChat()

@app.route('/health')
def health_check():
    try:
        # Test knowledge base
        patent_count = len(stasik_chat.agent.patents)
        paper_count = len(stasik_chat.agent.papers)
        
        # Test AI service
        test_response = stasik_chat.process_query("health check")
        
        return jsonify({
            'status': 'healthy',
            'knowledge_base': {
                'patents': patent_count,
                'papers': paper_count,
                'loaded': patent_count > 0 and paper_count > 0
            },
            'ai_service': {
                'responsive': bool(test_response),
                'model': 'gpt-5'
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/metrics')
def metrics():
    return jsonify({
        'requests_total': request_counter.get(),
        'response_time_avg': response_time.average(),
        'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
        'cpu_percent': psutil.Process().cpu_percent()
    })
```

### Logging Configuration
```python
# logging_config.py
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'json',
            'filename': '/app/logs/stasik.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10
        }
    },
    'loggers': {
        'stasik': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## 🔒 Security Configuration

### API Security
```python
# security.py
from functools import wraps
from flask import request, jsonify
import jwt

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(requests_per_minute=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            if is_rate_limited(client_ip, requests_per_minute):
                return jsonify({'error': 'Rate limit exceeded'}), 429
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### SSL/TLS Configuration
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    location / {
        proxy_pass http://stasik:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🚀 Scaling Strategies

### Horizontal Scaling
```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stasik-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stasik
  template:
    metadata:
      labels:
        app: stasik
    spec:
      containers:
      - name: stasik
        image: stasik:2.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: STASIK_MODE
          value: "production"

---
apiVersion: v1
kind: Service
metadata:
  name: stasik-service
spec:
  selector:
    app: stasik
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: stasik-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: stasik-deployment
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

### Load Balancing
```nginx
# Load balancer configuration
upstream stasik_backend {
    least_conn;
    server stasik-1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server stasik-2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server stasik-3:8000 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://stasik_backend;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
    }
}
```

---

## 📈 Performance Optimization

### Caching Strategy
```python
# caching.py
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='redis', port=6379, db=0)

def cache_response(ttl=3600):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"stasik:{f.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Generate response
            result = f(*args, **kwargs)
            
            # Cache result
            redis_client.setex(cache_key, ttl, json.dumps(result))
            
            return result
        return decorated_function
    return decorator
```

### Database Optimization
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Optimized database connection
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] API keys secured in secret management
- [ ] SSL certificates installed
- [ ] Database migrations completed
- [ ] Knowledge base loaded and validated
- [ ] Dependencies installed and updated
- [ ] Configuration files reviewed
- [ ] Security settings verified

### Deployment
- [ ] Application containers built
- [ ] Services deployed and running
- [ ] Load balancer configured
- [ ] Health checks passing
- [ ] Monitoring systems active
- [ ] Logging configured and working
- [ ] Scaling policies defined

### Post-Deployment
- [ ] Functionality testing completed
- [ ] Performance benchmarks met
- [ ] Error rates within acceptable limits
- [ ] Monitoring alerts configured
- [ ] Backup systems verified
- [ ] Documentation updated
- [ ] Team trained on new deployment

---

## 🆘 Troubleshooting

### Common Issues
1. **High Memory Usage**: Enable compression, lazy loading
2. **Slow Response Times**: Check caching, database queries
3. **API Rate Limits**: Implement proper rate limiting
4. **SSL Certificate Issues**: Verify certificate chain
5. **Database Connections**: Check connection pool settings

### Debug Commands
```bash
# Check system resources
docker stats
kubectl top pods

# View logs
docker logs stasik-container
kubectl logs deployment/stasik-deployment

# Test connectivity
curl -f http://localhost:8000/health
kubectl exec -it pod/stasik-pod -- wget -O- http://localhost:8000/health
```

---

**Your Stasik v2.0 deployment is now ready for production! 🚀**

*For additional support, see the troubleshooting guides or contact the development team.*