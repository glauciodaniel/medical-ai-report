'use client';

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

interface PatientData {
  age: string;
  weight: string;
  clinicalHistory: string;
}

interface PatientFormProps {
  patientData: PatientData;
  onChange: (data: PatientData) => void;
}

export function PatientForm({ patientData, onChange }: PatientFormProps) {
  const handleInputChange = (field: keyof PatientData, value: string) => {
    onChange({
      ...patientData,
      [field]: value
    });
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="age" className="text-white">
            Idade *
          </Label>
          <Input
            id="age"
            type="number"
            placeholder="Ex: 45"
            value={patientData.age}
            onChange={(e) => handleInputChange('age', e.target.value)}
            className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-blue-400"
            min="0"
            max="120"
          />
          <p className="text-xs text-gray-500">Anos de idade</p>
        </div>

        <div className="space-y-2">
          <Label htmlFor="weight" className="text-white">
            Peso *
          </Label>
          <Input
            id="weight"
            type="number"
            placeholder="Ex: 70.5"
            value={patientData.weight}
            onChange={(e) => handleInputChange('weight', e.target.value)}
            className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-blue-400"
            min="0"
            max="500"
            step="0.1"
          />
          <p className="text-xs text-gray-500">Peso em quilogramas</p>
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="clinicalHistory" className="text-white">
          Histórico Clínico *
        </Label>
        <Textarea
          id="clinicalHistory"
          placeholder="Descreva o histórico clínico relevante do paciente, sintomas atuais, medicações em uso, cirurgias anteriores, alergias, etc."
          value={patientData.clinicalHistory}
          onChange={(e) => handleInputChange('clinicalHistory', e.target.value)}
          className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 focus:border-blue-400 min-h-[120px] resize-vertical"
          rows={5}
        />
        <p className="text-xs text-gray-500">
          Forneça informações detalhadas para uma análise mais precisa
        </p>
      </div>
    </div>
  );
}