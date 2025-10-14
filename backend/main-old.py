"""
Medical AI Report Backend
FastAPI server for generating medical reports using Hugging Face MedGemma model.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
from typing import Optional

# Import configuration
from config import (
    HUGGINGFACE_API_TOKEN, 
    MEDGEMMA_MODEL_URL, 
    API_HOST, 
    API_PORT,
    CORS_ORIGINS,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
    validate_config
)

# Import statements for production
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL not available")

# Import requests separately to ensure it's always available
import requests

app = FastAPI(
    title="Medical AI Report API", 
    version="1.0.0",
    # Configurações para suportar respostas longas
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para aumentar limites de tamanho (comentado por enquanto)
# @app.middleware("http")
# async def increase_payload_size(request, call_next):
#     # Aumentar limite de tamanho da requisição
#     if hasattr(request, '_body'):
#         request._body_size_limit = 100 * 1024 * 1024  # 100MB
#     
#     response = await call_next(request)
#     return response

class ReportRequest(BaseModel):
    image: str  # base64 encoded image
    age: str
    weight: str
    clinical_history: str

class ReportResponse(BaseModel):
    report: str
    success: bool
    message: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Medical AI Report API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "pil_available": PIL_AVAILABLE}

@app.post("/generate_report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a medical report based on image and patient data using MedGemma model.
    
    This endpoint processes the medical image and patient context to generate
    a comprehensive medical report using AI.
    """
    
    try:
        # Validate input
        if not request.image or not request.age or not request.weight or not request.clinical_history:
            raise HTTPException(
                status_code=400,
                detail="Todos os campos são obrigatórios: imagem, idade, peso e histórico clínico"
            )
        
        # Check if Hugging Face API token is configured
        if not validate_config():
            return ReportResponse(
                report=generate_demo_report(request),
                success=True,
                message="Token da API Hugging Face não configurado. Configure HUGGINGFACE_API_TOKEN"
            )
        
        # Try to use Hugging Face API
        try:
            print(f"🚀 Iniciando processamento IA para paciente {request.age} anos...")
            report_text = await process_medical_image_with_ai(request)
            print(f"✅ Processamento IA concluído com sucesso!")
            return ReportResponse(
                report=report_text,
                success=True,
                message="Relatório gerado com sucesso usando modelo MedGemma"
            )
        except Exception as ai_error:
            # If AI processing fails, return demo report with error info
            print(f"❌ Erro no processamento IA: {str(ai_error)}")
            print(f"🔍 Tipo de erro: {type(ai_error).__name__}")
            demo_report = generate_demo_report(request)
            return ReportResponse(
                report=demo_report,
                success=True,
                message=f"Erro no processamento IA: {str(ai_error)}. Retornando relatório demonstrativo."
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

async def process_medical_image_with_ai(request: ReportRequest) -> str:
    """
    Process medical image with AI using Hugging Face MedGemma model.
    This function requires proper API token and dependencies for production use.
    """
    
    try:
        print(f"🔍 Decodificando imagem base64...")
        # Decode base64 image
        image_data = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(image_data))
        print(f"✅ Imagem decodificada: {image.size[0]}x{image.size[1]} pixels")
        
        # Prepare the prompt for MedGemma-4B-IT-YMF
        prompt = f"""Analise esta imagem médica e forneça um relatório médico abrangente.

Informações do Paciente:
- Idade: {request.age} anos
- Peso: {request.weight} kg
- Histórico Clínico: {request.clinical_history}

Por favor, forneça:
1. Avaliação da qualidade da imagem
2. Estruturas anatômicas visíveis
3. Achados patológicos (se houver)
4. Impressão clínica
5. Recomendações para avaliação adicional

Formate a resposta como um relatório médico profissional em português (Brasil)."""
        
        # Prepare API request to Hugging Face
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Convert image to format suitable for MedGemma API
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Payload otimizado para endpoint customizado (formato inputs)
        payload = {
            "inputs": prompt,
            "image": image_b64,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            # Parâmetros para evitar truncamento
            "truncate": False,
            "truncation": False,
            "max_length": None,
            "cutoff": None,
            "do_sample": True,
            "return_full_text": True
        }
        
        print(f"🌐 Enviando requisição para: {MEDGEMMA_MODEL_URL}")
        print(f"📊 Parâmetros: max_new_tokens={MAX_NEW_TOKENS}, temp={TEMPERATURE}, top_p={TOP_P}")
        print(f"📝 Tamanho do prompt: {len(prompt)} caracteres")
        print(f"🖼️  Tamanho da imagem: {len(image_b64)} caracteres base64")
        print(f"📋 Formato: Endpoint customizado (inputs + image)")
        print(f"⚠️  ATENÇÃO: Solicitando {MAX_NEW_TOKENS} tokens - verificar se o endpoint suporta")
        print(f"🔍 Payload completo:")
        print(f"   - inputs: {len(prompt)} caracteres")
        print(f"   - image: {len(image_b64)} caracteres base64")
        print(f"   - total payload: ~{len(str(payload))} caracteres")
        
        # Tentar diferentes estratégias para capturar resposta completa
        print(f"🔄 Tentando capturar resposta completa...")
        
        # Estratégia 1: Requisição normal com timeout maior
        print(f"⏱️  Timeout configurado: 60 segundos")
        response = requests.post(MEDGEMMA_MODEL_URL, headers=headers, json=payload, timeout=60)
        
        print(f"📡 Status da resposta: {response.status_code}")
        print(f"⏱️  Tempo de resposta: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code != 200:
            print(f"❌ Erro na API: {response.status_code} - {response.text}")
            raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
        
        result = response.json()
        print(f"📋 Resposta recebida: {type(result)} - {len(str(result))} caracteres")
        print(f"🔍 Resposta completa da API:")
        print(f"   {result}")
        
        # Estratégia 2: Verificar se a resposta foi cortada
        response_text = str(result)
        if len(response_text) < 1000:  # Se muito curta, pode ter sido cortada
            print(f"⚠️  Resposta parece muito curta, tentando estratégia alternativa...")
            
            # Tentar com timeout muito maior
            headers_with_timeout = headers.copy()
            headers_with_timeout["X-Timeout"] = "300"  # 5 minutos
            
            print(f"⏱️  Segunda tentativa com timeout: 300 segundos")
            response2 = requests.post(MEDGEMMA_MODEL_URL, headers=headers_with_timeout, json=payload, timeout=300)
            if response2.status_code == 200:
                result2 = response2.json()
                print(f"📋 Segunda tentativa: {type(result2)} - {len(str(result2))} caracteres")
                if len(str(result2)) > len(response_text):
                    result = result2
                    print(f"✅ Segunda tentativa retornou mais dados!")
            
            # Estratégia 3: Tentar com parâmetros anti-truncamento
            if len(str(result)) < 2000:  # Se ainda muito curta
                print(f"🔄 Tentando com parâmetros anti-truncamento...")
                payload_no_truncate = {
                    "inputs": prompt,
                    "image": image_b64,
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    # Forçar sem truncamento
                    "truncate": False,
                    "truncation": False,
                    "max_length": 0,  # 0 = sem limite
                    "cutoff": 0,      # 0 = sem corte
                    "do_sample": True,
                    "return_full_text": True,
                    "stream": False
                }
                
                print(f"⏱️  Terceira tentativa com timeout: 180 segundos")
                response3 = requests.post(MEDGEMMA_MODEL_URL, headers=headers, json=payload_no_truncate, timeout=180)
                if response3.status_code == 200:
                    result3 = response3.json()
                    print(f"📋 Terceira tentativa (anti-truncamento): {type(result3)} - {len(str(result3))} caracteres")
                    if len(str(result3)) > len(str(result)):
                        result = result3
                        print(f"✅ Terceira tentativa retornou mais dados!")
                
                # Estratégia 4: Tentar com streaming se ainda falhar
                if len(str(result)) < 3000:  # Se ainda muito curta
                    print(f"🔄 Tentando com streaming para capturar resposta completa...")
                    payload_stream = {
                        "inputs": prompt,
                        "image": image_b64,
                        "temperature": TEMPERATURE,
                        "top_p": TOP_P,
                        "stream": True,
                        "truncate": False
                    }
                    
                    try:
                        print(f"⏱️  Quarta tentativa (streaming) com timeout: 300 segundos")
                        response4 = requests.post(MEDGEMMA_MODEL_URL, headers=headers, json=payload_stream, timeout=300, stream=True)
                        if response4.status_code == 200:
                            # Coletar resposta em streaming
                            full_response = ""
                            for line in response4.iter_lines():
                                if line:
                                    full_response += line.decode('utf-8')
                            
                            print(f"📋 Quarta tentativa (streaming): {len(full_response)} caracteres")
                            if len(full_response) > len(str(result)):
                                result = {"streamed_response": full_response}
                                print(f"✅ Streaming retornou mais dados!")
                    except Exception as e:
                        print(f"⚠️  Streaming falhou: {e}")
        
        # Handle different response formats from Hugging Face API
        if isinstance(result, list) and len(result) > 0:
            print(f"📝 Processando resposta em formato LISTA:")
            print(f"   Primeiro item: {result[0]}")
            # Standard format
            if 'generated_text' in result[0]:
                generated_text = result[0]['generated_text']
                print(f"✅ Texto gerado encontrado em 'generated_text'")
            elif 'text' in result[0]:
                generated_text = result[0]['text']
                print(f"✅ Texto gerado encontrado em 'text'")
            else:
                generated_text = str(result[0])
                print(f"⚠️  Usando string do primeiro item")
        elif isinstance(result, dict):
            print(f"📝 Processando resposta em formato DICIONÁRIO:")
            print(f"   Chaves disponíveis: {list(result.keys())}")
            # Alternative format
            if 'generated_text' in result:
                generated_text = result['generated_text']
                print(f"✅ Texto gerado encontrado em 'generated_text'")
            elif 'text' in result:
                generated_text = str(result)
                print(f"✅ Texto gerado encontrado em 'text'")
            else:
                generated_text = str(result)
                print(f"⚠️  Usando string do dicionário")
        else:
            generated_text = str(result)
            print(f"⚠️  Usando string da resposta")
        
        print(f"📄 Texto extraído ({len(generated_text)} caracteres):")
        print(f"   {generated_text[:200]}...")
        
        # Clean up the response to extract only the report part
        print(f"🧹 Limpando resposta...")
        print(f"   Prompt original: {len(prompt)} caracteres")
        print(f"   Texto gerado: {len(generated_text)} caracteres")
        
        # Remove the prompt from the beginning if it exists
        if generated_text.startswith(prompt):
            report = generated_text[len(prompt):].strip()
            print(f"✅ Prompt removido do início")
        elif prompt in generated_text:
            report = generated_text.replace(prompt, '').strip()
            print(f"✅ Prompt removido do meio")
        else:
            report = generated_text.strip()
            print(f"⚠️  Prompt não encontrado, usando texto completo")
        
        # If report is empty or too short, use the full response
        if not report or len(report) < 50:
            report = generated_text.strip()
            print(f"⚠️  Relatório muito curto, usando resposta completa")
        
        print(f"📄 Relatório limpo: {len(report)} caracteres")
        print(f"   Primeiros 200: {report[:200]}...")
        print(f"   Meio (1000-1200): {report[1000:1200] if len(report) > 1200 else 'Muito curto'}...")
        print(f"   Últimos 200: {report[-200:] if len(report) > 200 else report}")
        print(f"   Tamanho total: {len(report)} caracteres")
        
        # Detectar se a resposta foi cortada
        if report.endswith('...') or report.endswith('...') or len(report) < 500:
            print(f"⚠️  ALERTA: Resposta pode ter sido cortada!")
            print(f"   Final da resposta: {report[-100:]}")
            print(f"   Recomendação: Verificar limite do endpoint ou aumentar timeout")
        
        # Format the final report
        final_report = format_medical_report(report, request)
        
        print(f"📋 RELATÓRIO FINAL GERADO:")
        print(f"   Tamanho: {len(final_report)} caracteres")
        print(f"   Primeiros 300 caracteres:")
        print(f"   {final_report[:300]}...")
        print(f"   Últimos 200 caracteres:")
        print(f"   ...{final_report[-200:]}")
        
        return final_report
        
    except Exception as e:
        raise Exception(f"Erro ao processar imagem com IA: {str(e)}")

def format_medical_report(ai_response: str, request: ReportRequest) -> str:
    """Format the AI response into a proper medical report structure."""
    
    from datetime import datetime
    
    report = f"""RELATÓRIO MÉDICO AUTOMATIZADO

DADOS DO PACIENTE:
Idade: {request.age} anos
Peso: {request.weight} kg

HISTÓRICO CLÍNICO:
{request.clinical_history}

ANÁLISE POR INTELIGÊNCIA ARTIFICIAL:
{ai_response}

OBSERVAÇÕES IMPORTANTES:
- Este relatório foi gerado por inteligência artificial
- Requer validação e interpretação médica profissional
- Não substitui a avaliação clínica presencial

Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
Sistema: MedIA Reports v1.0
"""
    
    return report

def generate_demo_report(request: ReportRequest) -> str:
    """Generate a demo report for WebContainer environment."""
    
    from datetime import datetime
    
    return f"""RELATÓRIO MÉDICO DEMONSTRATIVO

DADOS DO PACIENTE:
Idade: {request.age} anos
Peso: {request.weight} kg

HISTÓRICO CLÍNICO:
{request.clinical_history}

ANÁLISE DA IMAGEM:
A imagem médica enviada foi processada pelo sistema de inteligência artificial. 
Este é um relatório demonstrativo que mostra a estrutura e formato do documento final.

OBSERVAÇÕES TÉCNICAS:
- Qualidade da imagem: Adequada para análise
- Modalidade detectada: Imagem médica digital
- Processamento: Concluído com sucesso

IMPRESSÃO DEMONSTRATIVA:
[Em ambiente de produção, esta seção conteria a análise detalhada gerada pelo modelo MedGemma da Google através da API do Hugging Face, incluindo identificação de estruturas anatômicas, possíveis achados patológicos e recomendações clínicas baseadas na imagem e histórico do paciente.]

RECOMENDAÇÕES GERAIS:
1. Correlação clínica sempre necessária
2. Avaliação médica presencial recomendada
3. Considerar exames complementares conforme indicação clínica

AVISO IMPORTANTE:
Este é um relatório demonstrativo gerado para fins de teste do sistema. 
Em ambiente de produção, o conteúdo seria gerado por IA especializada em análise médica.

Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
Sistema: MedIA Reports v1.0 (Modo Demonstração)
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=API_HOST, 
        port=API_PORT,
        # Configurações para suportar respostas longas
        timeout_keep_alive=30
    )