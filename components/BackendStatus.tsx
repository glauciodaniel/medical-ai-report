"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { API_CONFIG, buildApiUrl } from "@/lib/config";
import { RefreshCw, Wifi, WifiOff } from "lucide-react";
import { useEffect, useState } from "react";

export function BackendStatus() {
  const [status, setStatus] = useState<"checking" | "online" | "offline">(
    "checking"
  );
  const [lastCheck, setLastCheck] = useState<Date | null>(null);

  const checkBackendStatus = async () => {
    setStatus("checking");
    try {
      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.HEALTH), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        setStatus("online");
      } else {
        setStatus("offline");
      }
    } catch (error) {
      console.error("Erro ao verificar status do backend:", error);
      setStatus("offline");
    }
    setLastCheck(new Date());
  };

  useEffect(() => {
    checkBackendStatus();
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case "online":
        return "bg-green-500";
      case "offline":
        return "bg-red-500";
      case "checking":
        return "bg-yellow-500";
      default:
        return "bg-gray-500";
    }
  };

  const getStatusText = () => {
    switch (status) {
      case "online":
        return "Conectado";
      case "offline":
        return "Desconectado";
      case "checking":
        return "Verificando...";
      default:
        return "Desconhecido";
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case "online":
        return <Wifi className="h-4 w-4 text-green-400" />;
      case "offline":
        return <WifiOff className="h-4 w-4 text-red-400" />;
      case "checking":
        return <RefreshCw className="h-4 w-4 text-yellow-400 animate-spin" />;
      default:
        return <Wifi className="h-4 w-4 text-gray-400" />;
    }
  };

  return (
    <Card className="bg-gray-900 border-gray-800">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center justify-between text-white text-sm">
          Status do Backend
          <Button
            variant="ghost"
            size="sm"
            onClick={checkBackendStatus}
            disabled={status === "checking"}
            className="h-6 w-6 p-0"
          >
            <RefreshCw className="h-3 w-3" />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {getStatusIcon()}
            <span className="text-sm text-gray-300">{getStatusText()}</span>
          </div>
          <Badge
            variant="secondary"
            className={`${getStatusColor()} text-white border-0`}
          >
            {status === "online"
              ? "ONLINE"
              : status === "offline"
              ? "OFFLINE"
              : "VERIFICANDO"}
          </Badge>
        </div>

        <div className="mt-2 text-xs text-gray-500">
          <div>URL: {API_CONFIG.BACKEND_URL}</div>
          {lastCheck && (
            <div>
              Última verificação: {lastCheck.toLocaleTimeString("pt-BR")}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
