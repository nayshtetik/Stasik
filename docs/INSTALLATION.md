# Installation Guide - Stasik v2.0

## 🚀 Quick Installation

### Prerequisites
- **Python**: 3.8 or higher
- **OS**: Windows 10+, macOS 10.14+, or Linux Ubuntu 18.04+
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for knowledge base

### Basic Setup

```bash
# 1. Clone the repository
git clone https://github.com/nayshtetik/Stasik.git
cd Stasik

# 2. Create virtual environment (recommended)
python -m venv stasik-env
source stasik-env/bin/activate  # On Windows: stasik-env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Basic test
python debugging_chat_with_tracking.py
```

---

## 🔧 Advanced Installation

### 1. Environment Setup

#### **Option A: conda (Recommended for Scientific Computing)**
```bash
# Create conda environment
conda create -n stasik python=3.11
conda activate stasik

# Install scientific dependencies via conda
conda install numpy pandas scipy matplotlib seaborn plotly

# Install remaining requirements
pip install -r requirements.txt
```

#### **Option B: Docker (Isolated Deployment)**
```bash
# Build Docker image
docker build -t stasik:2.0 .

# Run container
docker run -it -p 8000:8000 \
  -e OPENAI_API_KEY="your_key" \
  -e SERPAPI_KEY="your_key" \
  stasik:2.0
```

### 2. API Keys Configuration

#### **Required for Enhanced Features**

```bash
# OpenAI GPT-5 Integration
export OPENAI_API_KEY="sk-your-openai-key-here"

# SerpAPI for Enhanced Search
export SERPAPI_KEY="your-serpapi-key-here"
```

#### **Optional Enhancements**
```bash
# SearXNG Self-Hosted Search (optional)
export SEARXNG_URL="http://localhost:8080"

# Custom Configuration
export STASIK_CONFIG_PATH="/path/to/custom/config.yaml"
```

#### **Environment File (.env)**
```bash
# Create .env file in project root
cat > .env << EOF
OPENAI_API_KEY=sk-your-openai-key
SERPAPI_KEY=your-serpapi-key
SEARXNG_URL=http://localhost:8080
STASIK_MODE=enhanced
STASIK_DEBUG=false
EOF
```

---

## 📊 Knowledge Base Setup

### Automatic Setup (Default)
The system automatically uses the recategorized knowledge base:
- **File**: `RECATEGORIZED_KB_562papers_1100patents_58news_20250827_120248.json`
- **Location**: Downloaded automatically on first run
- **Size**: ~500MB (compressed), ~2GB (loaded)

### Manual Knowledge Base
```bash
# Download specific knowledge base version
wget https://github.com/nayshtetik/Stasik/releases/download/v2.0.0/knowledge-base-v2.0.0.json

# Set custom knowledge base path
export STASIK_KB_PATH="/path/to/custom-knowledge-base.json"
```

---

## 🔍 Verification & Testing

### Basic Functionality Test
```python
# test_installation.py
from debugging_chat_with_tracking import DebuggingStasikChat

# Initialize system
chat = DebuggingStasikChat()

# Test knowledge base loading
print(f"Patents loaded: {len(chat.agent.patents)}")
print(f"Papers loaded: {len(chat.agent.papers)}")

# Test basic query
response = chat.process_query("What are MEMS airflow sensors?")
print("✅ Installation successful!" if response else "❌ Installation issues")
```

### Advanced Feature Testing
```bash
# Test GPT-5 integration (requires API key)
python -c "
import openai
client = openai.OpenAI()
response = client.responses.create(
    model='gpt-5',
    input='Test GPT-5 access',
    text={'verbosity': 'low'}
)
print('✅ GPT-5 access confirmed')
"

# Test SerpAPI access (requires API key)
python -c "
import serpapi
search = serpapi.GoogleSearch({
    'q': 'UAV airflow sensors',
    'engine': 'google_scholar',
    'api_key': 'your_key'
})
print('✅ SerpAPI access confirmed')
"
```

---

## ⚙️ Configuration Options

### Basic Configuration (config/config.yaml)
```yaml
stasik:
  # Core settings
  mode: "enhanced"              # standard, enhanced, debug
  gpt_model: "gpt-5"           # gpt-4o, gpt-5
  knowledge_base: "recategorized"
  
  # Search integration
  search_integration: true
  news_updates: true
  relevance_checking: true
  
  # Performance
  cache_enabled: true
  max_response_time: 30
  
  # Logging
  log_level: "INFO"            # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/stasik.log"
```

### Advanced Configuration
```yaml
advanced:
  # AI settings
  temperature: 0.1
  max_tokens: 4000
  reasoning_effort: "medium"    # low, medium, high
  
  # Search settings
  max_search_results: 20
  search_timeout: 10
  relevance_threshold: 0.7
  
  # Knowledge base
  auto_update: false
  backup_enabled: true
  compression: true
  
  # API limits
  openai_rpm: 500
  serpapi_rpm: 100
  
  # Security
  api_key_encryption: true
  request_logging: false
```

---

## 🐛 Troubleshooting

### Common Issues

#### **Import Errors**
```bash
# Issue: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source stasik-env/bin/activate
pip install -r requirements.txt

# Issue: numpy/scipy compilation errors
# Solution: Use conda or pre-compiled wheels
conda install numpy scipy pandas
```

#### **API Key Issues**
```bash
# Issue: OpenAI API errors
# Solution: Verify API key and billing
export OPENAI_API_KEY="sk-correct-key-format"
python -c "import openai; print(openai.OpenAI().models.list())"

# Issue: SerpAPI quota exceeded
# Solution: Check usage and upgrade plan
curl "https://serpapi.com/account?api_key=YOUR_KEY"
```

#### **Knowledge Base Loading**
```bash
# Issue: Knowledge base not found
# Solution: Check file path and permissions
ls -la RECATEGORIZED_KB_*.json
chmod 644 RECATEGORIZED_KB_*.json

# Issue: Memory errors loading knowledge base
# Solution: Increase available memory or use compression
export STASIK_COMPRESSION=true
export STASIK_LAZY_LOADING=true
```

#### **Performance Issues**
```bash
# Issue: Slow response times
# Solution: Enable caching and optimize settings
export STASIK_CACHE_ENABLED=true
export STASIK_PARALLEL_SEARCH=true

# Issue: High memory usage
# Solution: Reduce knowledge base size or use streaming
export STASIK_STREAM_MODE=true
export STASIK_MAX_PAPERS=1000
```

### Debug Mode
```bash
# Enable comprehensive debugging
export STASIK_DEBUG=true
export STASIK_LOG_LEVEL=DEBUG
python debugging_chat_with_tracking.py

# View detailed logs
tail -f logs/stasik-debug.log
```

---

## 📦 Optional Dependencies

### Machine Learning Features
```bash
# Semantic embeddings for enhanced search
pip install sentence-transformers faiss-cpu

# Advanced NLP processing
pip install spacy transformers
python -m spacy download en_core_web_sm
```

### Development Tools
```bash
# Testing and quality assurance
pip install pytest pytest-cov black flake8 mypy pre-commit

# Documentation generation
pip install sphinx sphinx-rtd-theme myst-parser

# Performance monitoring
pip install memory-profiler line-profiler
```

### System Integration
```bash
# Jupyter notebook integration
pip install jupyter ipywidgets

# Web interface (experimental)
pip install streamlit gradio

# Database backends (optional)
pip install postgresql psycopg2-binary  # PostgreSQL
pip install mysql-connector-python      # MySQL
```

---

## 🚀 Performance Optimization

### Memory Optimization
```python
# config/performance.yaml
memory:
  lazy_loading: true
  compression: true
  cache_size_mb: 512
  gc_frequency: 100
```

### Processing Optimization
```python
# Enable parallel processing
processing:
  parallel_search: true
  max_workers: 4
  batch_size: 50
  timeout_seconds: 30
```

### Network Optimization
```python
# Optimize API calls
network:
  connection_pooling: true
  request_timeout: 10
  retry_attempts: 3
  rate_limiting: true
```

---

## ✅ Installation Verification Checklist

### Basic Installation
- [ ] Python 3.8+ installed and accessible
- [ ] Virtual environment created and activated
- [ ] All requirements installed without errors
- [ ] Basic chat interface starts successfully
- [ ] Knowledge base loads (check paper/patent counts)

### Enhanced Features
- [ ] OpenAI API key configured and tested
- [ ] SerpAPI key configured and tested
- [ ] GPT-5 model accessible
- [ ] News integration working
- [ ] Enhanced search functional

### Optional Components
- [ ] Docker setup (if using containerization)
- [ ] Development tools installed (if contributing)
- [ ] Documentation builds successfully
- [ ] All tests pass

### Performance Verification
- [ ] Response time <3 seconds for basic queries
- [ ] Memory usage stable during operation
- [ ] No errors in debug logs
- [ ] API rate limits respected

---

## 🆘 Getting Help

### Self-Help Resources
1. **Documentation**: Check README.md and docs/ directory
2. **Logs**: Review logs/stasik.log for error details
3. **Configuration**: Verify config/config.yaml settings
4. **Dependencies**: Ensure all requirements.txt items installed

### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community help
- **Documentation**: Comprehensive guides and tutorials
- **Examples**: Sample code and use cases

### Professional Support
For enterprise deployments or custom integrations, contact the development team through GitHub or professional consulting channels.

---

**Installation complete! You're ready to explore UAV airflow sensing technologies with Stasik v2.0.**

*Next: See the README.md for usage examples and the full feature overview.*