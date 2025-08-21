import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MedIA Reports - Relatórios Médicos com IA',
  description: 'Geração automatizada de relatórios médicos usando inteligência artificial especializada',
  keywords: 'medicina, IA, relatórios médicos, diagnóstico, MedGemma',
  authors: [{ name: 'MedIA Reports Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#1a1a1a',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={`${inter.className} bg-gray-950 text-white min-h-screen`}>
        {children}
      </body>
    </html>
  );
}