export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

export interface ChatResponse {
  session_id: string;
  reply: string;
  response_language: "english" | "filipino";
  sources: string[];
}

export async function getSession(): Promise<string> {
  const cached = sessionStorage.getItem("chat_session_id");
  if (cached) return cached;
  const res = await fetch("/api/chat");
  const { session_id } = await res.json();
  sessionStorage.setItem("chat_session_id", session_id);
  return session_id;
}

export async function sendMessage(
  sessionId: string,
  message: string
): Promise<ChatResponse> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!res.ok) throw new Error("Failed to send message");
  return res.json();
}