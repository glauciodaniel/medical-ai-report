"""
Hugging Face integration service for medical AI analysis.
"""

import base64
import io
import json
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import requests
    from PIL import Image
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

class HuggingFaceService:
    """Service for interacting with Hugging Face Inference API."""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://r2y80g16msuhn4pg.us-east-1.aws.endpoints.huggingface.cloud"
        self.medgemma_url = f"{self.base_url}"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def analyze_medical_image(
        self,
        image_base64: str,
        patient_age: str,
        patient_weight: str,
        clinical_history: str
    ) -> str:
        """
        Analyze medical image using MedGemma model.
        
        Args:
            image_base64: Base64 encoded medical image
            patient_age: Patient age in years
            patient_weight: Patient weight in kg
            clinical_history: Patient clinical history
            
        Returns:
            Generated medical report text
            
        Raises:
            Exception: If API call fails or dependencies are not available
        """
        
        if not DEPENDENCIES_AVAILABLE:
            raise Exception(
                "Dependências necessárias não estão disponíveis. "
                "Instale: pip install requests pillow transformers"
            )
        
        try:
            # Validate and process image
            image = self._process_image(image_base64)
            
            # Create comprehensive prompt
            prompt = self._create_medical_prompt(
                patient_age, patient_weight, clinical_history
            )
            
            # Call Hugging Face API
            response = await self._call_medgemma_api(prompt, image)
            
            # Process and format response
            formatted_report = self._format_medical_report(
                response, patient_age, patient_weight, clinical_history
            )
            
            return formatted_report
            
        except Exception as e:
            raise Exception(f"Erro na análise de imagem médica: {str(e)}")
    
    def _process_image(self, image_base64: str) -> Image.Image:
        """Process and validate medical image."""
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (max 1024x1024 for API efficiency)
            max_size = 1024
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            raise Exception(f"Erro ao processar imagem: {str(e)}")
    
    def _create_medical_prompt(
        self, age: str, weight: str, clinical_history: str
    ) -> str:
        """Create a comprehensive and direct prompt for medical analysis."""
        
        prompt = f"""
        SYSTEM: Você é um cardiologista experiente. Sua tarefa é analisar a imagem de Eletrocardiograma (ECG) fornecida e gerar um laudo médico detalhado e objetivo.
        **DADOS DO PACIENTE:**
        - **Idade:** {age} anos
        - **Peso:** {weight} kg
        - **Histórico Clínico:** {clinical_history}

       **TAREFA:**
        Baseado exclusivamente na imagem do ECG e no histórico clínico, elabore o laudo médico. O laudo deve ser estruturado e conter as seguintes seções obrigatórias com suas respectivas análises:

        1.  **Análise do Traçado e Calibração:** (Avalie a qualidade técnica da imagem).
        2.  **Ritmo e Frequência Cardíaca (FC):** (Identifique o ritmo e calcule a FC).
        3.  **Análise de Intervalos:** (Calcule e avalie os valores de PR, QRS, QT e QTc).
        4.  **Eixo Elétrico:** (Determine o eixo elétrico).
        5.  **Análise Morfológica:** (Descreva a morfologia da onda P, complexo QRS, segmento ST e onda T).
        6.  **Arritmias e Distúrbios de Condução:** (Identifique quaisquer anormalidades).
        7.  **Conclusão e Impressão Diagnóstica:** (Sintetize os achados em uma conclusão clara).
        8.  **Recomendações:** (Sugira os próximos passos ou exames, se necessário).

        Gere apenas o texto do laudo, seguindo estritamente as seções acima.
        """
        
        return prompt.strip()
    
    async def _call_medgemma_api(self, prompt: str, image: Image.Image) -> str:
        """Call MedGemma model via Hugging Face API."""
        
        try:
            # Convert image to base64 for API
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_b64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Prepare API payload for multimodal model
            payload = {
                "inputs": prompt,
                "image": f"data:image/png;base64,{image_b64}",
                "parameters": {
                    "max_new_tokens": 2048,
                    "temperature": 0.7,
                    "return_full_text": False,
                    "do_sample": True, 
                    "top_p": 0.95,
                    "repetition_penalty": 1.1
                }
            }
            
            # Make API request with increased timeout
            response = requests.post(
                self.medgemma_url,
                headers=self.headers,
                json=payload,
                timeout=180  # Aumentado para 2 minutos
            )
            
            if response.status_code == 503:
                # Model is loading, wait and retry with longer timeout
                import time
                print("⏳ Modelo carregando... aguardando 20 segundos...")
                time.sleep(20)
                response = requests.post(
                    self.medgemma_url,
                    headers=self.headers,
                    json=payload,
                    timeout=180  # 3 minutos para retry
                )
            
            if response.status_code != 200:
                raise Exception(
                    f"Erro da API Hugging Face: {response.status_code} - {response.text}"
                )
            
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Com return_full_text=False, não precisa remover o prompt
                report = generated_text.strip()
            else:
                raise Exception("Formato de resposta inválido da API Hugging Face")
            
            return report
            
        except requests.exceptions.Timeout:
            raise Exception("Timeout na chamada da API - tente novamente")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição HTTP: {str(e)}")
    
    def _format_medical_report(
        self, ai_response: str, age: str, weight: str, clinical_history: str
    ) -> str:
        """Format the AI response into a professional medical report."""
        
        current_time = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        formatted_report = f"""RELATÓRIO MÉDICO AUTOMATIZADO

═══════════════════════════════════════════════════════════════
DADOS DO PACIENTE:
Idade: {age} anos
Peso: {weight} kg
Data do Relatório: {current_time}

HISTÓRICO CLÍNICO:
{clinical_history}

═══════════════════════════════════════════════════════════════
ANÁLISE POR INTELIGÊNCIA ARTIFICIAL:

{ai_response}

═══════════════════════════════════════════════════════════════
OBSERVAÇÕES IMPORTANTES:

⚠️  AVISO MÉDICO-LEGAL:
• Este relatório foi gerado por inteligência artificial
• A análise é baseada exclusivamente na imagem fornecida
• Requer validação e interpretação por médico especialista
• Não substitui avaliação clínica presencial
• Considerar sempre o contexto clínico completo

📋 RECOMENDAÇÕES GERAIS:
• Correlação clínica obrigatória
• Avaliação médica presencial recomendada
• Considerar exames complementares conforme indicação

═══════════════════════════════════════════════════════════════
Sistema: MedIA Reports v1.0
Modelo: MedGemma (Google)
Processado em: {current_time}
"""
        
        return formatted_report

    def check_api_status(self) -> Dict[str, Any]:
        """Check the status of Hugging Face API."""
        try:
            response = requests.get(
                f"{self.medgemma_url}",
                headers=self.headers,
                timeout=10
            )
            return {
                "status": "available" if response.status_code == 200 else "unavailable",
                "status_code": response.status_code,
                "dependencies_available": DEPENDENCIES_AVAILABLE
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "dependencies_available": DEPENDENCIES_AVAILABLE
            }

# Demo service for WebContainer environment
class DemoHuggingFaceService:
    """Demo service that provides sample responses when real API is not available."""
    
    def __init__(self):
        pass
    
    async def analyze_medical_image(
        self,
        image_base64: str,
        patient_age: str,
        patient_weight: str,
        clinical_history: str
    ) -> str:
        """Generate a demo medical report."""
        
        current_time = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        demo_report = f"""RELATÓRIO MÉDICO DEMONSTRATIVO

═══════════════════════════════════════════════════════════════
DADOS DO PACIENTE:
Idade: {patient_age} anos
Peso: {patient_weight} kg
Data do Relatório: {current_time}

HISTÓRICO CLÍNICO:
{clinical_history}

═══════════════════════════════════════════════════════════════
ANÁLISE DEMONSTRATIVA:

QUALIDADE DA IMAGEM:
A imagem médica enviada apresenta qualidade adequada para análise. 
Parâmetros técnicos dentro dos padrões aceitáveis para avaliação.

ESTRUTURAS ANATÔMICAS IDENTIFICADAS:
[Em ambiente de produção, esta seção seria preenchida com a identificação 
detalhada das estruturas anatômicas visíveis na imagem, baseada na análise 
do modelo MedGemma]

ACHADOS PRINCIPAIS:
[Aqui seriam descritos os achados específicos identificados pela IA, 
incluindo medidas, densidades, padrões de sinal/intensidade e outras 
características relevantes]

IMPRESSÃO DIAGNÓSTICA:
[Esta seção conteria a interpretação clínica dos achados, correlacionada 
com o histórico do paciente e as características da imagem]

═══════════════════════════════════════════════════════════════
OBSERVAÇÕES IMPORTANTES:

⚠️  MODO DEMONSTRAÇÃO:
Este é um relatório gerado em modo demonstração para fins de teste 
do sistema. Em ambiente de produção, o conteúdo seria gerado pelo 
modelo MedGemma através da API do Hugging Face.

📋 FUNCIONALIDADES EM PRODUÇÃO:
• Análise detalhada por IA especializada em medicina
• Identificação automática de estruturas anatômicas
• Detecção de possíveis patologias
• Correlação com dados clínicos
• Recomendações baseadas em evidências

═══════════════════════════════════════════════════════════════
Sistema: MedIA Reports v1.0 (Modo Demo)
Processado em: {current_time}
"""
        
        return demo_report
    
    def check_api_status(self) -> Dict[str, Any]:
        """Return demo API status."""
        return {
            "status": "demo_mode",
            "message": "Rodando em modo demonstração - API real não disponível",
            "dependencies_available": DEPENDENCIES_AVAILABLE
        }