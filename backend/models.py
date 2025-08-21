"""
Data models for the Medical AI Report API.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class PatientInfo(BaseModel):
    """Patient information model."""
    age: str = Field(..., description="Patient age in years")
    weight: str = Field(..., description="Patient weight in kg")
    clinical_history: str = Field(..., description="Patient clinical history")
    
    @validator('age')
    def validate_age(cls, v):
        try:
            age_int = int(v)
            if age_int < 0 or age_int > 120:
                raise ValueError('Idade deve estar entre 0 e 120 anos')
        except ValueError:
            raise ValueError('Idade deve ser um número válido')
        return v
    
    @validator('weight')
    def validate_weight(cls, v):
        try:
            weight_float = float(v)
            if weight_float <= 0 or weight_float > 500:
                raise ValueError('Peso deve estar entre 0 e 500 kg')
        except ValueError:
            raise ValueError('Peso deve ser um número válido')
        return v
    
    @validator('clinical_history')
    def validate_clinical_history(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Histórico clínico deve ter pelo menos 10 caracteres')
        return v.strip()

class MedicalImage(BaseModel):
    """Medical image model."""
    image_data: str = Field(..., description="Base64 encoded image data")
    image_type: Optional[str] = Field(None, description="Type of medical image (X-ray, MRI, CT, etc.)")
    
    @validator('image_data')
    def validate_image_data(cls, v):
        if not v or len(v) < 100:
            raise ValueError('Dados da imagem inválidos')
        return v

class ReportRequest(BaseModel):
    """Complete request model for report generation."""
    image: str = Field(..., description="Base64 encoded medical image")
    age: str = Field(..., description="Patient age")
    weight: str = Field(..., description="Patient weight")
    clinical_history: str = Field(..., description="Patient clinical history")
    
    class Config:
        schema_extra = {
            "example": {
                "image": "base64_encoded_image_data_here",
                "age": "45",
                "weight": "70.5",
                "clinical_history": "Paciente apresenta dor torácica há 2 semanas, sem antecedentes cardiovasculares conhecidos."
            }
        }

class ReportResponse(BaseModel):
    """Response model for generated medical report."""
    report: str = Field(..., description="Generated medical report")
    success: bool = Field(..., description="Success status")
    message: Optional[str] = Field(None, description="Additional message")
    generated_at: datetime = Field(default_factory=datetime.now, description="Report generation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "report": "RELATÓRIO MÉDICO AUTOMATIZADO\n\n...",
                "success": True,
                "message": "Relatório gerado com sucesso",
                "generated_at": "2024-01-15T10:30:00"
            }
        }

class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0.0")
    dependencies: dict = Field(default_factory=dict)
    
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)