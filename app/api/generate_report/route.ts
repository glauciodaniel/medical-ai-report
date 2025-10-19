import { NextRequest, NextResponse } from "next/server";

// Esta rota usa `request.json()` e precisa ser tratada como dinâmica.
export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { image, age, weight, clinical_history } = body;

    // Validar campos obrigatórios
    if (!image || !age || !weight || !clinical_history) {
      return NextResponse.json(
        { error: "Todos os campos são obrigatórios" },
        { status: 400 }
      );
    }

    // Para demonstração, retornamos um relatório simulado.
    const mockReport = `RELATÓRIO MÉDICO AUTOMATIZADO

DADOS DO PACIENTE:
Idade: ${age} anos
Peso: ${weight} kg

HISTÓRICO CLÍNICO:
${clinical_history}

ANÁLISE DA IMAGEM:
A análise da imagem médica foi processada com sucesso utilizando inteligência artificial especializada.

OBSERVAÇÕES TÉCNICAS:
- Qualidade da imagem: Adequada para análise
- Processamento: Concluído
- Modalidade: Detectada automaticamente

IMPRESSÃO DIAGNÓSTICA:
[Relatório demonstrativo - Em produção, este conteúdo seria gerado pelo modelo MedGemma]

As características observadas na imagem, correlacionadas com o histórico clínico apresentado, sugerem a necessidade de avaliação médica especializada para confirmação diagnóstica.

RECOMENDAÇÕES:
1. Correlação clínica necessária
2. Avaliação médica presencial
3. Considerar exames complementares se indicado

⚠️ AVISO: Este relatório foi gerado por IA e requer validação médica profissional.

Data: ${new Date().toLocaleDateString("pt-BR")}
Sistema: MedIA Reports v1.0`;

    return NextResponse.json({
      report: mockReport,
      success: true,
      message: "Relatório gerado com sucesso (modo demonstração)",
    });
  } catch (error) {
    console.error("Error generating report:", error);
    return NextResponse.json(
      { error: "Erro interno do servidor" },
      { status: 500 }
    );
  }
}
