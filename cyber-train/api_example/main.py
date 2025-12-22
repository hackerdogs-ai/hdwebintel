"""
Example FastAPI Application for NER and Intent Classification

This is a template for production API development.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
import spacy
import time
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NER & Intent Classification API",
    version="1.0.0",
    description="Production API for entity extraction and intent classification",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
ner_model = None
intent_model = None
models_loaded = False

# Request/Response Models
class EntityExtractionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to extract entities from")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()

class IntentClassificationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to classify intent for")
    threshold: float = Field(0.3, ge=0.0, le=1.0, description="Minimum confidence threshold")

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze")
    threshold: float = Field(0.3, ge=0.0, le=1.0, description="Minimum confidence threshold for intents")

class BatchRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100, description="List of texts to process")
    threshold: float = Field(0.3, ge=0.0, le=1.0, description="Minimum confidence threshold")

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int

class Intent(BaseModel):
    intent: str
    score: float

class EntityExtractionResponse(BaseModel):
    entities: List[Entity]
    count: int
    processing_time_ms: float

class IntentClassificationResponse(BaseModel):
    intents: List[Intent]
    count: int
    processing_time_ms: float

class AnalyzeResponse(BaseModel):
    entities: List[Entity]
    intents: List[Intent]
    entity_count: int
    intent_count: int
    processing_time_ms: float

class BatchResponse(BaseModel):
    results: List[Dict]
    total_processed: int
    total_entities: int
    total_intents: int
    processing_time_ms: float

# Model Loading
def load_models():
    """Load NER and Intent models."""
    global ner_model, intent_model, models_loaded
    
    try:
        ner_path = Path("cyber-train/models/ner_model/model-best")
        intent_path = Path("cyber-train/models/intent_model/model-best")
        
        if not ner_path.exists():
            raise FileNotFoundError(f"NER model not found at {ner_path}")
        if not intent_path.exists():
            raise FileNotFoundError(f"Intent model not found at {intent_path}")
        
        logger.info("Loading NER model...")
        ner_model = spacy.load(str(ner_path))
        logger.info(f"✅ NER model loaded: {len(ner_model.get_pipe('ner').labels)} labels")
        
        logger.info("Loading Intent model...")
        intent_model = spacy.load(str(intent_path))
        logger.info(f"✅ Intent model loaded: {len(intent_model.get_pipe('textcat_multilabel').labels)} labels")
        
        models_loaded = True
        logger.info("✅ All models loaded successfully")
        
    except Exception as e:
        logger.error(f"❌ Error loading models: {e}")
        models_loaded = False
        raise

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    load_models()

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if models_loaded else "unhealthy",
        "models_loaded": models_loaded,
        "timestamp": datetime.utcnow().isoformat()
    }

# Entity Extraction Endpoint
@app.post("/api/v1/entities/extract", response_model=EntityExtractionResponse)
async def extract_entities(request: EntityExtractionRequest):
    """Extract entities from text."""
    if not models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    try:
        doc = ner_model(request.text)
        entities = [
            Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            )
            for ent in doc.ents
        ]
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"Extracted {len(entities)} entities in {processing_time:.2f}ms")
        
        return EntityExtractionResponse(
            entities=entities,
            count=len(entities),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Intent Classification Endpoint
@app.post("/api/v1/intents/classify", response_model=IntentClassificationResponse)
async def classify_intents(request: IntentClassificationRequest):
    """Classify intents from text."""
    if not models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    try:
        doc = intent_model(request.text)
        intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
        intents = [
            Intent(intent=intent, score=score)
            for intent, score in intents
            if score >= request.threshold
        ]
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"Classified {len(intents)} intents in {processing_time:.2f}ms")
        
        return IntentClassificationResponse(
            intents=intents,
            count=len(intents),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error classifying intents: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Combined Analysis Endpoint
@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Extract entities and classify intents from text."""
    if not models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    try:
        # Extract entities
        doc_ner = ner_model(request.text)
        entities = [
            Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            )
            for ent in doc_ner.ents
        ]
        
        # Classify intents
        doc_intent = intent_model(request.text)
        intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
        intents = [
            Intent(intent=intent, score=score)
            for intent, score in intents
            if score >= request.threshold
        ]
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"Analyzed: {len(entities)} entities, {len(intents)} intents in {processing_time:.2f}ms")
        
        return AnalyzeResponse(
            entities=entities,
            intents=intents,
            entity_count=len(entities),
            intent_count=len(intents),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Batch Processing Endpoint
@app.post("/api/v1/batch/process", response_model=BatchResponse)
async def process_batch(request: BatchRequest, background_tasks: BackgroundTasks):
    """Process multiple texts in batch."""
    if not models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    try:
        results = []
        total_entities = 0
        total_intents = 0
        
        for text in request.texts:
            # Extract entities
            doc_ner = ner_model(text)
            entities = [
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                }
                for ent in doc_ner.ents
            ]
            
            # Classify intents
            doc_intent = intent_model(text)
            intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
            intents = [
                {"intent": intent, "score": score}
                for intent, score in intents
                if score >= request.threshold
            ]
            
            results.append({
                "text": text,
                "entities": entities,
                "intents": intents,
                "entity_count": len(entities),
                "intent_count": len(intents)
            })
            
            total_entities += len(entities)
            total_intents += len(intents)
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(f"Processed {len(results)} texts: {total_entities} entities, {total_intents} intents in {processing_time:.2f}ms")
        
        return BatchResponse(
            results=results,
            total_processed=len(results),
            total_entities=total_entities,
            total_intents=total_intents,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing batch: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

