import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { username, password } = body || {};

    const expectedUser = process.env.NEXT_PUBLIC_DEMO_USER || "mr-user-review";
    const expectedPass = process.env.NEXT_PUBLIC_DEMO_PASS || "_!0*MR-PASS!";

    if (!username || !password) {
      return NextResponse.json(
        { ok: false, message: "Usuário e senha são necessários" },
        { status: 400 }
      );
    }

    if (username === expectedUser && password === expectedPass) {
      // token simples e não seguro para demo
      const token = Buffer.from(`${username}:${Date.now()}`).toString("base64");
      return NextResponse.json({ ok: true, token });
    }

    return NextResponse.json(
      { ok: false, message: "Credenciais inválidas" },
      { status: 401 }
    );
  } catch (err) {
    console.error(err);
    return NextResponse.json(
      { ok: false, message: "Erro interno" },
      { status: 500 }
    );
  }
}
