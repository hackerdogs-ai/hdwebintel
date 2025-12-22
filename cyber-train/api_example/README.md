# NER & Intent Classification API

Production-ready FastAPI application for entity extraction and intent classification.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure Models are Available

Make sure the trained models are in:
- `cyber-train/models/ner_model/model-best`
- `cyber-train/models/intent_model/model-best`

### 3. Run the API

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /health
```

### Extract Entities
```
POST /api/v1/entities/extract
Body: {"text": "Check IP 192.168.1.1"}
```

### Classify Intents
```
POST /api/v1/intents/classify
Body: {"text": "Check IP 192.168.1.1", "threshold": 0.3}
```

### Analyze (Entities + Intents)
```
POST /api/v1/analyze
Body: {"text": "Check IP 192.168.1.1", "threshold": 0.3}
```

### Batch Process
```
POST /api/v1/batch/process
Body: {"texts": ["text1", "text2"], "threshold": 0.3}
```

## Docker

### Build
```bash
docker build -t nlp-api .
```

### Run
```bash
docker run -p 8000:8000 -v $(pwd)/cyber-train/models:/app/models nlp-api
```

## Production Deployment

See `PRODUCTIZATION_GUIDE.md` for complete deployment instructions.

