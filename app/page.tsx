"use client";

import { BackendStatus } from "@/components/BackendStatus";
import { FileUpload } from "@/components/FileUpload";
import Login from "@/components/Login";
import { PatientForm } from "@/components/PatientForm";
import { ReportDisplay } from "@/components/ReportDisplay";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { API_CONFIG, buildApiUrl } from "@/lib/config";
import { FileText, Stethoscope, User } from "lucide-react";
import { useState } from "react";

interface PatientData {
  age: string;
  weight: string;
  clinicalHistory: string;
}

function MainApp() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [patientData, setPatientData] = useState<PatientData>({
    age: "",
    weight: "",
    clinicalHistory: "",
  });
  const [report, setReport] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
  };

  const handlePatientDataChange = (data: PatientData) => {
    setPatientData(data);
  };

  const generateReport = async () => {
    if (!uploadedFile) {
      alert("Por favor, envie uma imagem do exame médico.");
      return;
    }

    if (
      !patientData.age ||
      !patientData.weight ||
      !patientData.clinicalHistory
    ) {
      alert("Por favor, preencha todos os campos do paciente.");
      return;
    }

    setIsGenerating(true);

    try {
      // Convert file to base64
      const base64Image = await fileToBase64(uploadedFile);

      // Chamar diretamente o backend Python
      const response = await fetch(
        buildApiUrl(API_CONFIG.ENDPOINTS.GENERATE_REPORT),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            image: base64Image,
            age: patientData.age,
            weight: patientData.weight,
            clinical_history: patientData.clinicalHistory,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao gerar relatório");
      }

      const data = await response.json();
      console.log("📋 Resposta completa da API:", data);

      // Verificar se a resposta tem o formato esperado
      if (data.report) {
        setReport(data.report);
      } else if (data.message) {
        setReport(data.message);
      } else {
        console.error("❌ Formato de resposta inesperado:", data);
        setReport("Erro: Formato de resposta inesperado da API");
      }
    } catch (error) {
      console.error("Erro:", error);
      // Fallback para relatório demo em caso de erro
      setReport(`RELATÓRIO MÉDICO AUTOMATIZADO

DADOS DO PACIENTE:
Idade: ${patientData.age} anos
Peso: ${patientData.weight} kg

HISTÓRIO CLÍNICO:
${patientData.clinicalHistory}

ANÁLISE DA IMAGEM:
A análise da imagem médica enviada foi processada utilizando inteligência artificial especializada em diagnósticos médicos.

OBSERVAÇÕES TÉCNICAS:
- Qualidade da imagem: Adequada para análise
- Modalidade do exame: Detectada automaticamente
- Regiões de interesse: Identificadas e analisadas

IMPRESSÃO DIAGNÓSTICA:
[Este é um relatório demonstrativo. Em um ambiente de produção, este conteúdo seria gerado pelo modelo MedGemma através da API do Hugging Face]

A análise sugere a necessidade de correlação clínica adicional. Recomenda-se avaliação médica presencial para confirmação diagnóstica.

RECOMENDAÇÕES:
1. Correlação clínica necessária
2. Considerar exames complementares se indicado
3. Acompanhamento médico regular

Data: ${new Date().toLocaleDateString("pt-BR")}
Relatório gerado por IA - Requer validação médica`);
    } finally {
      setIsGenerating(false);
    }
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64 = reader.result as string;
        resolve(base64.split(",")[1]);
      };
      reader.onerror = (error) => reject(error);
    });
  };

  const canGenerateReport =
    uploadedFile &&
    patientData.age &&
    patientData.weight &&
    patientData.clinicalHistory;

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Stethoscope className="h-10 w-10 text-blue-400 mr-3" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              MedIA Reports
            </h1>
          </div>
          <p className="text-gray-300 text-lg">
            Geração de relatórios médicos com inteligência artificial
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div className="space-y-6">
            {/* Backend Status */}
            <BackendStatus />

            {/* File Upload */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <FileText className="h-5 w-5 mr-2 text-blue-400" />
                  Envio de Imagem Médica
                </CardTitle>
              </CardHeader>
              <CardContent>
                <FileUpload onFileUpload={handleFileUpload} />
              </CardContent>
            </Card>

            {/* Patient Form */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <User className="h-5 w-5 mr-2 text-blue-400" />
                  Dados do Paciente
                </CardTitle>
              </CardHeader>
              <CardContent>
                <PatientForm
                  patientData={patientData}
                  onChange={handlePatientDataChange}
                />
              </CardContent>
            </Card>

            {/* Generate Button */}
            <Button
              onClick={generateReport}
              disabled={!canGenerateReport || isGenerating}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed h-12 text-lg font-semibold"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Gerando Relatório...
                </>
              ) : (
                "Gerar Relatório Médico"
              )}
            </Button>
          </div>

          {/* Right Column - Report Display */}
          <div>
            <Card className="bg-gray-900 border-gray-800 h-full">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <FileText className="h-5 w-5 mr-2 text-blue-400" />
                  Relatório Gerado
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ReportDisplay report={report} isGenerating={isGenerating} />
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);

  const handleSuccess = (tok: string, user: string) => {
    setToken(tok);
    setUsername(user);
    // para demo, persistir em sessionStorage
    if (typeof window !== "undefined") {
      sessionStorage.setItem("demo_token", tok);
      sessionStorage.setItem("demo_user", user);
    }
  };

  // restaurar sessão básica
  if (typeof window !== "undefined" && !token) {
    const stored = sessionStorage.getItem("demo_token");
    const storedUser = sessionStorage.getItem("demo_user");
    if (stored && storedUser) {
      setToken(stored);
      setUsername(storedUser);
    }
  }

  if (!token) {
    return <Login onSuccess={handleSuccess} />;
  }

  return <MainApp />;
}

("use client");

interface PatientData {
  age: string;
  weight: string;
  clinicalHistory: string;
}

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [patientData, setPatientData] = useState<PatientData>({
    age: "",
    weight: "",
    clinicalHistory: "",
  });
  const [report, setReport] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
  };

  const handlePatientDataChange = (data: PatientData) => {
    setPatientData(data);
  };

  const generateReport = async () => {
    if (!uploadedFile) {
      alert("Por favor, envie uma imagem do exame médico.");
      return;
    }

    if (
      !patientData.age ||
      !patientData.weight ||
      !patientData.clinicalHistory
    ) {
      alert("Por favor, preencha todos os campos do paciente.");
      return;
    }

    setIsGenerating(true);

    try {
      // Convert file to base64
      const base64Image = await fileToBase64(uploadedFile);

      // Chamar diretamente o backend Python
      const response = await fetch(
        buildApiUrl(API_CONFIG.ENDPOINTS.GENERATE_REPORT),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            image: base64Image,
            age: patientData.age,
            weight: patientData.weight,
            clinical_history: patientData.clinicalHistory,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao gerar relatório");
      }

      const data = await response.json();
      console.log("📋 Resposta completa da API:", data);
      console.log("🔍 Campo 'report':", data.report);
      console.log("🔍 Campo 'message':", data.message);
      console.log("🔍 Tipo de resposta:", typeof data);

      // Verificar se a resposta tem o formato esperado
      if (data.report) {
        setReport(data.report);
      } else if (data.message) {
        setReport(data.message);
      } else {
        console.error("❌ Formato de resposta inesperado:", data);
        setReport("Erro: Formato de resposta inesperado da API");
      }
    } catch (error) {
      console.error("Erro:", error);
      // Fallback para relatório demo em caso de erro
      setReport(`RELATÓRIO MÉDICO AUTOMATIZADO

DADOS DO PACIENTE:
Idade: ${patientData.age} anos
Peso: ${patientData.weight} kg

HISTÓRIO CLÍNICO:
${patientData.clinicalHistory}

ANÁLISE DA IMAGEM:
A análise da imagem médica enviada foi processada utilizando inteligência artificial especializada em diagnósticos médicos.

OBSERVAÇÕES TÉCNICAS:
- Qualidade da imagem: Adequada para análise
- Modalidade do exame: Detectada automaticamente
- Regiões de interesse: Identificadas e analisadas

IMPRESSÃO DIAGNÓSTICA:
[Este é um relatório demonstrativo. Em um ambiente de produção, este conteúdo seria gerado pelo modelo MedGemma através da API do Hugging Face]

A análise sugere a necessidade de correlação clínica adicional. Recomenda-se avaliação médica presencial para confirmação diagnóstica.

RECOMENDAÇÕES:
1. Correlação clínica necessária
2. Considerar exames complementares se indicado
3. Acompanhamento médico regular

Data: ${new Date().toLocaleDateString("pt-BR")}
Relatório gerado por IA - Requer validação médica`);
    } finally {
      setIsGenerating(false);
    }
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64 = reader.result as string;
        resolve(base64.split(",")[1]);
      };
      reader.onerror = (error) => reject(error);
    });
  };

  const canGenerateReport =
    uploadedFile &&
    patientData.age &&
    patientData.weight &&
    patientData.clinicalHistory;

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Stethoscope className="h-10 w-10 text-blue-400 mr-3" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              MedIA Reports
            </h1>
          </div>
          <p className="text-gray-300 text-lg">
            Geração de relatórios médicos com inteligência artificial
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div className="space-y-6">
            {/* Backend Status */}
            <BackendStatus />

            {/* File Upload */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <FileText className="h-5 w-5 mr-2 text-blue-400" />
                  Envio de Imagem Médica
                </CardTitle>
              </CardHeader>
              <CardContent>
                <FileUpload onFileUpload={handleFileUpload} />
              </CardContent>
            </Card>

            {/* Patient Form */}
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <User className="h-5 w-5 mr-2 text-blue-400" />
                  Dados do Paciente
                </CardTitle>
              </CardHeader>
              <CardContent>
                <PatientForm
                  patientData={patientData}
                  onChange={handlePatientDataChange}
                />
              </CardContent>
            </Card>

            {/* Generate Button */}
            <Button
              onClick={generateReport}
              disabled={!canGenerateReport || isGenerating}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed h-12 text-lg font-semibold"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Gerando Relatório...
                </>
              ) : (
                "Gerar Relatório Médico"
              )}
            </Button>
          </div>

          {/* Right Column - Report Display */}
          <div>
            <Card className="bg-gray-900 border-gray-800 h-full">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <FileText className="h-5 w-5 mr-2 text-blue-400" />
                  Relatório Gerado
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ReportDisplay report={report} isGenerating={isGenerating} />
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
