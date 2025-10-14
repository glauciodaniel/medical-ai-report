"""
Hugging Face integration service for medical AI analysis.
"""

import base64
import io
import json
import httpx 
import asyncio
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
    
    def __init__(self, api_token: str, model_url: Optional[str] = None):
        self.api_token = api_token
        
        # URL base do endpoint
        base_url = model_url if model_url else "https://u9yyy2quq9hdyqbu.us-east-1.aws.endpoints.huggingface.cloud"
        
        # Adiciona a rota correta para chat completions
        self.medgemma_url = f"{base_url.rstrip('/')}/v1/chat/completions"
        
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
            # 🔍 LOGS PARA VERIFICAR O ENVIO DA IMAGEM
            print(f"📥 Imagem recebida: {len(image_base64)} caracteres base64")
            print(f"🔍 Primeiros 50 chars: {image_base64[:50]}...")
            
            image_data = base64.b64decode(image_base64)
            print(f"📊 Dados decodificados: {len(image_data)} bytes")
            
            image = Image.open(io.BytesIO(image_data))
            print(f"✅ Imagem carregada: {image.size} pixels, modo {image.mode}")
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                print(f"🔄 Convertido para RGB")
            
            # Resize if too large (max 1024x1024 for API efficiency)
            max_size = 1024
            if image.width > max_size or image.height > max_size:
                original_size = image.size
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                print(f"📏 Redimensionado de {original_size} para {image.size}")
            
            return image
            
        except Exception as e:
            raise Exception(f"Erro ao processar imagem: {str(e)}")
    
    def _create_medical_prompt(
        self, age: str, weight: str, clinical_history: str
    ) -> str:
        """Create a comprehensive medical prompt following MedGemma format."""
        
        prompt = f"""Analise a imagem médica e forneça um relatório estruturado.

PACIENTE: {age} anos, {weight} kg
HISTÓRIA: {clinical_history}

RESPONDA COM ANÁLISE MÉDICA INCLUINDO:

1. QUALIDADE DA IMAGEM:
- Qualidade técnica e adequação diagnóstica

2. ESTRUTURAS ANATÔMICAS:
- Estruturas visíveis e normalidades

3. ACHADOS ANORMAIS:
- Patologias identificadas com localização e características

4. IMPRESSÃO DIAGNÓSTICA:
- Diagnóstico baseado nos achados

5. RECOMENDAÇÕES:
- Próximos passos ou exames complementares

RESPOSTA:"""
        
        return prompt.strip()
    


    async def _call_medgemma_api(self, prompt: str, image: Image.Image) -> str:
        """Call MedGemma model via Hugging Face API using multiple format attempts."""
        
        # Converte a imagem para base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        print(f"🚀 Enviando requisição para: {self.medgemma_url}")
        print(f"📦 Tamanho do prompt: {len(prompt)} | Tamanho da imagem b64: {len(image_b64)}")

        # Tenta múltiplos formatos de payload
        result = await self._try_endpoint_formats(prompt, image_b64)
        
        if result and result.strip():
            return result
        elif result == "":
            # Se conseguimos conectar mas o resultado é vazio, pode ser um problema com o prompt
            print("⚠️ Modelo conectou mas retornou resposta vazia. Tentando prompt simplificado...")
            simple_prompt = "Analise esta imagem médica e descreva os principais achados."
            simple_result = await self._try_endpoint_formats(simple_prompt, image_b64)
            if simple_result and simple_result.strip():
                return simple_result
            else:
                raise Exception("Modelo retornou resposta vazia mesmo com prompt simplificado")
        else:
            raise Exception("Todos os formatos de API falharam - verifique a configuração do endpoint")

    async def _try_endpoint_formats(self, prompt: str, image_b64: str) -> Optional[str]:
        """Try different payload formats for the current endpoint."""
        
        # Format 1: Chat completions with image_url format (OpenAI compatible)
        payload1 = {
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                    ]
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.3,
            "top_p": 0.9,
            "stream": False,
            "stop": None
        }
        
        # Format 2: Simple completions format (v1/completions endpoint)
        # O Model Card especifica que o token <image> deve vir antes do prompt de texto
        # A nova linha (\n) é importante para separar a imagem do texto.
        prompt_com_token = f"<image>\n{prompt}"
        payload2 = {
            "prompt": prompt_com_token,
            "max_tokens": 4096,
            "temperature": 0.3,
            "top_p": 0.9,
            "stream": False,
            "stop": None
        }
        
        # Format 3: Chat completions text only (fallback)
        payload3 = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2048,
            "temperature": 0.3,
            "top_p": 0.9,
            "stream": False,
            "stop": None
        }
        
        # Format 4: Hugging Face inference format com token de imagem
        prompt_hf_format = f"<image>\n{prompt}"
        payload4 = {
            "inputs": prompt_hf_format,
            "parameters": {
                "max_new_tokens": 2048,
                "temperature": 0.3,
                "return_full_text": False,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        # Format 5: MedGemma specific format
        # Usando o formato correto com token <image> e nova linha
        medgemma_prompt = f"<image>\n{prompt}"
        payload5 = {
            "messages": [
                {"role": "user", "content": medgemma_prompt}
            ],
            "images": [image_b64],
            "max_tokens": 4096,
            "temperature": 0.3,
            "top_p": 0.9,
            "stop": None
        }
        
        # Format 6: Formato direto com imagem no payload
        payload6 = {
            "inputs": {
                "text": f"<image>\n{prompt}",
                "image": image_b64
            },
            "parameters": {
                "max_new_tokens": 2048,
                "temperature": 0.3,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        # Format 7: Formato MedGemma simplificado
        simple_medgemma_prompt = f"<image>\nDescreva os achados médicos nesta imagem:"
        payload7 = {
            "messages": [
                {"role": "user", "content": simple_medgemma_prompt}
            ],
            "max_tokens": 2048,
            "temperature": 0.3,
            "top_p": 0.9,
            "stream": False
        }
        
        payloads = [payload1, payload2, payload3, payload4, payload5, payload6, payload7]
        payload_names = ["ChatCompletions-Image-URL", "Simple-Completions", "ChatCompletions-Text", "HF-Inference", "MedGemma-Format", "Direct-Image-Payload", "Simple-MedGemma"]
        
        # URLs para testar (completions vs chat/completions)
        urls_to_try = [
            self.medgemma_url,  # /v1/chat/completions
            self.medgemma_url.replace("/v1/chat/completions", "/v1/completions"),  # /v1/completions
            self.medgemma_url.replace("/v1/chat/completions", "")  # base URL
        ]
        
        print(f"📋 Tentando múltiplos formatos de API:")
        print(f"   - prompt length: {len(prompt)} chars")
        print(f"   - image length: {len(image_b64)} chars")
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            # Tenta diferentes combinações de URL + payload
            for url in urls_to_try:
                print(f"🌐 Testando URL: {url}")
                
                for i, payload in enumerate(payloads):
                    # Pula combinações que não fazem sentido
                    if "/completions" in url and not "/chat/" in url and payload_names[i].startswith("Chat"):
                        continue
                    if "/chat/completions" in url and payload_names[i] == "Simple-Completions":
                        continue
                        
                    try:
                        print(f"🔄 Tentando {payload_names[i]} em {url}")
                        
                        response = await client.post(url, headers=self.headers, json=payload)
                        
                        # Handle model loading (503)
                        if response.status_code == 503:
                            print("⏳ Modelo carregando... aguardando 20 segundos...")
                            await asyncio.sleep(20)
                            response = await client.post(url, headers=self.headers, json=payload)
                        
                        # Success
                        if response.status_code == 200:
                            result = response.json()
                            print(f"✅ Sucesso com {payload_names[i]} em {url}")
                            
                            # Handle chat completions format
                            if isinstance(result, dict) and 'choices' in result:
                                print(f"📋 Resposta em formato chat completions")
                                print(f"🔍 Resultado completo: {json.dumps(result, indent=2)[:500]}...")
                                
                                if result['choices'] and len(result['choices']) > 0:
                                    choice = result['choices'][0]
                                    print(f"🔍 Choice: {json.dumps(choice, indent=2)}")
                                    
                                    if 'message' in choice and 'content' in choice['message']:
                                        content = choice['message']['content']
                                        if content:
                                            content = content.strip()
                                            
                                            # Verifica se o modelo retornou apenas o prompt (problema comum)
                                            if self._is_prompt_echo(content, prompt):
                                                print("⚠️ Modelo retornou apenas o prompt, tentando próximo formato...")
                                                continue
                                            
                                            print(f"✅ Conteúdo extraído: {len(content)} caracteres")
                                            return content
                                        else:
                                            print("⚠️ Conteúdo vazio na resposta")
                                    elif 'text' in choice:
                                        content = choice['text']
                                        if content:
                                            content = content.strip()
                                            print(f"✅ Texto extraído: {len(content)} caracteres")
                                            return content
                                        else:
                                            print("⚠️ Texto vazio na resposta")
                                    else:
                                        print(f"⚠️ Estrutura inesperada no choice: {choice.keys()}")
                                else:
                                    print("⚠️ Lista de choices vazia")
                            
                            # Handle standard Hugging Face format
                            elif isinstance(result, list) and len(result) > 0:
                                print(f"📋 Resposta em formato lista HF")
                                generated_text = result[0].get('generated_text', '').strip()
                                
                                # Verifica se é apenas echo do prompt
                                if self._is_prompt_echo(generated_text, prompt):
                                    print("⚠️ HF formato retornou apenas o prompt, tentando próximo formato...")
                                    continue
                                    
                                return generated_text
                            elif isinstance(result, dict) and 'generated_text' in result:
                                print(f"📋 Resposta em formato dict HF")
                                generated_text = result['generated_text'].strip()
                                
                                # Verifica se é apenas echo do prompt
                                if self._is_prompt_echo(generated_text, prompt):
                                    print("⚠️ HF dict formato retornou apenas o prompt, tentando próximo formato...")
                                    continue
                                    
                                return generated_text
                            else:
                                print(f"⚠️ Formato de resposta inesperado: {type(result)} - {str(result)[:200]}")
                                continue
                        
                        # Log detailed error for debugging
                        error_text = response.text[:500] if response.text else "Sem conteúdo"
                        print(f"⚠️ {payload_names[i]} falhou: {response.status_code} - {error_text}")
                        
                    except httpx.TimeoutException:
                        print(f"⏱️ Timeout no formato {payload_names[i]}")
                        continue
                    except Exception as e:
                        print(f"❌ Erro no formato {payload_names[i]}: {str(e)}")
                        continue
        
        return None

    def _is_prompt_echo(self, response: str, original_prompt: str) -> bool:
        """
        Verifica se a resposta é apenas um echo do prompt original.
        Isso acontece quando o modelo não gera texto novo.
        """
        if not response or not original_prompt:
            return False
        
        # Remove tokens especiais e espaços para comparação
        clean_response = response.replace("<image>", "").replace("\n", " ").strip()
        clean_prompt = original_prompt.replace("<image>", "").replace("\n", " ").strip()
        
        # Se a resposta é muito similar ao prompt (>80% de sobreposição)
        if len(clean_response) > 0 and len(clean_prompt) > 0:
            # Calcula similaridade simples
            words_prompt = set(clean_prompt.lower().split())
            words_response = set(clean_response.lower().split())
            
            if len(words_prompt) > 0:
                overlap = len(words_prompt.intersection(words_response))
                similarity = overlap / len(words_prompt)
                
                print(f"🔍 Similaridade prompt/resposta: {similarity:.2f}")
                
                # Se mais de 80% das palavras do prompt estão na resposta, é provavelmente echo
                return similarity > 0.8
        
        return False

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

    async def check_api_status(self) -> Dict[str, Any]:
        """Check the status of Hugging Face API endpoints."""
        endpoints_to_check = [
            self.medgemma_url,  # /v1/chat/completions
            self.medgemma_url.replace("/v1/chat/completions", "/v1/completions"),  # /v1/completions
            self.medgemma_url.replace("/v1/chat/completions", "")  # base URL
        ]
        
        status_results = []
        
        for endpoint in endpoints_to_check:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Test different payload formats based on endpoint
                    if "/chat/completions" in endpoint:
                        test_payload = {
                            "messages": [{"role": "user", "content": "test"}],
                            "max_tokens": 1
                        }
                    elif "/completions" in endpoint:
                        test_payload = {
                            "prompt": "test",
                            "max_tokens": 1
                        }
                    else:
                        test_payload = {
                            "inputs": "test",
                            "parameters": {"max_new_tokens": 1}
                        }
                    
                    response = await client.post(endpoint, headers=self.headers, json=test_payload)
                    
                    status_results.append({
                        "endpoint": endpoint,
                        "status": "available" if response.status_code in [200, 503] else "unavailable",
                        "status_code": response.status_code,
                        "response_text": response.text[:200] if response.status_code != 200 else "OK",
                        "is_primary": endpoint == self.medgemma_url
                    })
                    
            except Exception as e:
                status_results.append({
                    "endpoint": endpoint,
                    "status": "error",
                    "error": str(e),
                    "is_primary": endpoint == self.medgemma_url
                })
        
        return {
            "endpoints": status_results,
            "primary_endpoint": self.medgemma_url,
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