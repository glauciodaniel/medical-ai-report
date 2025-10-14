"use client";

import { Lock, User } from "lucide-react";
import { useState } from "react";

interface Props {
  onSuccess: (token: string, username: string) => void;
}

export function Login({ onSuccess }: Props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (!res.ok || !data?.ok) {
        setError(data?.message || "Credenciais inválidas");
        return;
      }

      // simples token demo
      const token = data.token;
      onSuccess(token, username);
    } catch (err) {
      setError("Erro ao conectar com o servidor");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-2xl shadow-lg p-8">
        <div className="text-center mb-6">
          <div className="flex items-center justify-center mb-3">
            <div className="bg-gradient-to-r from-blue-400 to-purple-500 rounded-full p-3">
              <Lock className="h-6 w-6 text-white" />
            </div>
          </div>
          <h2 className="text-2xl font-semibold">Acesse o MedIA Reports</h2>
          <p className="text-sm text-gray-400">
            Insira suas credenciais para continuar
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block">
            <span className="text-sm text-gray-300">Usuário</span>
            <div className="mt-1 relative">
              <input
                autoFocus
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 pr-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholder="seu.usuario"
                aria-label="Usuário"
              />
              <User className="absolute right-3 top-3 text-gray-400 h-4 w-4" />
            </div>
          </label>

          <label className="block">
            <span className="text-sm text-gray-300">Senha</span>
            <div className="mt-1 relative">
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 pr-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholder="••••••••"
                aria-label="Senha"
              />
              <Lock className="absolute right-3 top-3 text-gray-400 h-4 w-4" />
            </div>
          </label>

          {error && <div className="text-sm text-red-400">{error}</div>}

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white py-2 rounded-md font-medium"
            disabled={loading || !username || !password}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>

          <div className="text-center text-xs text-gray-500">
            <span>
              Sem opção de cadastro — contato do administrador para acesso
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
