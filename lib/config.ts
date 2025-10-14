export const API_CONFIG = {
  // URL do backend Python
  BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000",

  // Endpoints da API
  ENDPOINTS: {
    GENERATE_REPORT: "/generate_report",
    HEALTH: "/health",
  },
};

// Função helper para construir URLs completas
export const buildApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BACKEND_URL}${endpoint}`;
};
