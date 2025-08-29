"""
Medical AI Report Backend
FastAPI server for generating medical reports using a dedicated Hugging Face service.
"""

import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import configuration
from config import (
    HUGGINGFACE_API_TOKEN,
    API_HOST,
    API_PORT,
    CORS_ORIGINS
)

# --- LÓGICA DE INICIALIZAÇÃO DO SERVIÇO CORRIGIDA ---
# Inicializa a variável do serviço como None.
# Ela só será preenchida se a importação e a instanciação forem bem-sucedidas.
ai_service = None
SERVICE_INITIALIZATION_ERROR = None

try:
    # Tenta importar as classes de serviço
    from services.huggingface_service import HuggingFaceService, DemoHuggingFaceService
    
    # Decide qual serviço instanciar com base no token da API
    if HUGGINGFACE_API_TOKEN:
        ai_service = HuggingFaceService(api_token=HUGGINGFACE_API_TOKEN)
        print("✅ Real Hugging Face service initialized.")
    else:
        ai_service = DemoHuggingFaceService()
        print("⚠️  Hugging Face token not found. Initializing in DEMO mode.")

except ImportError:
    # Captura o erro se 'huggingface_service.py' não for encontrado
    SERVICE_INITIALIZATION_ERROR = "CRITICAL: 'huggingface_service.py' not found. The API cannot process reports."
    print(f"❌ {SERVICE_INITIALIZATION_ERROR}")
except Exception as e:
    SERVICE_INITIALIZATION_ERROR = f"CRITICAL: An unexpected error occurred while initializing services: {e}"
    print(f"❌ {SERVICE_INITIALIZATION_ERROR}")

# Import de dependências adicionais
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
# ----------------------------------------------------

# Initialize the main FastAPI application
app = FastAPI(
    title="Medical AI Report API",
    version="2.1.0",
    description="Refactored API with robust service initialization.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ReportRequest(BaseModel):
    image: str
    age: str
    weight: str
    clinical_history: str

class ReportResponse(BaseModel):
    report: str
    success: bool
    message: Optional[str] = None


# API Endpoints
@app.get("/")
async def root():
    return {"message": "Medical AI Report API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify dependencies and API status."""
    service_status = {}
    if ai_service and hasattr(ai_service, 'check_api_status'):
        service_status = ai_service.check_api_status()
    elif SERVICE_INITIALIZATION_ERROR:
        service_status = {"status": "error", "message": SERVICE_INITIALIZATION_ERROR}

    return {
        "status": "healthy" if not SERVICE_INITIALIZATION_ERROR else "degraded",
        "pil_available": PIL_AVAILABLE,
        "service_status": service_status
    }

@app.post("/generate_report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a medical report based on image and patient data.
    """
    # Verifica se o serviço de IA foi inicializado corretamente
    if not ai_service:
        raise HTTPException(
            status_code=503, # 503 Service Unavailable
            detail=f"AI Service is not available. Reason: {SERVICE_INITIALIZATION_ERROR}"
        )

    try:
        if not all([request.image, request.age, request.weight, request.clinical_history]):
            raise HTTPException(status_code=400, detail="All fields are required.")

        print(f"🚀 Initiating AI processing for patient aged {request.age}...")
        
        report_text = await ai_service.analyze_medical_image(
            image_base64=request.image,
            patient_age=request.age,
            patient_weight=request.weight,
            clinical_history=request.clinical_history
        )

        message = "Report generated successfully."
        if isinstance(ai_service, DemoHuggingFaceService):
            message = "API running in demonstration mode. This is a sample report."

        print("✅ AI processing completed successfully!")
        return ReportResponse(report=report_text, success=True, message=message)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"❌ An unexpected error occurred during report generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Main entry point
if __name__ == "__main__":
    # Se o serviço falhou ao inicializar, encerra o programa com uma mensagem clara
    if not ai_service:
        print("\nCould not start the server because the AI service failed to initialize.")
        sys.exit(1) # Encerra com código de erro

    import uvicorn
    print(f"Starting server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        timeout_keep_alive=180
    )