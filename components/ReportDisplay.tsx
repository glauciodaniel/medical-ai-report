'use client';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, Copy, Printer } from 'lucide-react';

interface ReportDisplayProps {
  report: string;
  isGenerating: boolean;
}

export function ReportDisplay({ report, isGenerating }: ReportDisplayProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(report);
  };

  const handleDownload = () => {
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `relatorio-medico-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Relatório Médico</title>
            <style>
              body {
                font-family: 'Times New Roman', serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #000;
              }
              .medical-report {
                white-space: pre-line;
              }
            </style>
          </head>
          <body>
            <div class="medical-report">${report}</div>
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  if (isGenerating) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4 mx-auto"></div>
          <p className="text-gray-300">Analisando imagem médica...</p>
          <p className="text-gray-500 text-sm mt-2">
            Processando com inteligência artificial
          </p>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="flex items-center justify-center h-96 text-center">
        <div>
          <div className="text-6xl mb-4">📋</div>
          <p className="text-gray-400 text-lg mb-2">
            Nenhum relatório gerado ainda
          </p>
          <p className="text-gray-500">
            Envie uma imagem médica e preencha os dados do paciente para gerar um relatório
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Action Buttons */}
      <div className="flex flex-wrap gap-2 pb-4 border-b border-gray-700">
        <Button
          variant="outline"
          size="sm"
          onClick={handleCopy}
          className="border-gray-600 text-gray-300 hover:bg-gray-800"
        >
          <Copy className="h-4 w-4 mr-1" />
          Copiar
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleDownload}
          className="border-gray-600 text-gray-300 hover:bg-gray-800"
        >
          <Download className="h-4 w-4 mr-1" />
          Download
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handlePrint}
          className="border-gray-600 text-gray-300 hover:bg-gray-800"
        >
          <Printer className="h-4 w-4 mr-1" />
          Imprimir
        </Button>
      </div>

      {/* Medical Report */}
      <Card className="bg-white text-black p-6">
        <div className="medical-report-content">
          <pre className="whitespace-pre-line font-serif text-sm leading-relaxed">
            {report}
          </pre>
        </div>
      </Card>

      {/* Disclaimer */}
      <div className="bg-yellow-900/20 border border-yellow-700 rounded-lg p-4">
        <p className="text-yellow-300 text-sm">
          ⚠️ <strong>Aviso Importante:</strong> Este relatório foi gerado por inteligência artificial e deve ser usado apenas como auxílio ao diagnóstico. É obrigatória a validação e interpretação por um profissional médico qualificado.
        </p>
      </div>
    </div>
  );
}