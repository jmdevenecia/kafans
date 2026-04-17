import { NextRequest, NextResponse } from "next/server";

const BACKEND = process.env.BACKEND_URL!;
const SECRET  = process.env.API_SECRET!;

export async function POST(req: NextRequest) {
  const body = await req.json();

  const res = await fetch(`${BACKEND}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-secret": SECRET,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    return NextResponse.json(
      { error: "Backend error" },
      { status: res.status }
    );
  }

  const data = await res.json();
  return NextResponse.json(data);
}

export async function GET() {
  const res = await fetch(`${BACKEND}/session`, {
    headers: { "x-api-secret": SECRET },
  });
  const data = await res.json();
  return NextResponse.json(data);
}