"use client";

import { useEffect, useRef, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { SendHorizontal } from "lucide-react";
import { MessageBubble } from "./message-bubble";
import { TypingIndicator } from "./typing-indicator";
import { LanguageBadge } from "./language-badge";
import { getSession, sendMessage, type ChatMessage } from "@/lib/api";

export function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm your research assistant. Ask me anything about the research database. " +
        "I understand both English and Filipino, but I'll respond in English by default.\n\n" +
        "Kumusta! Naiintindihan ko ang Ingles at Filipino. " +
        "Magsimula kang magtanong — sumasagot ako sa Ingles bilang default.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [responseLang, setResponseLang] = useState<"english" | "filipino">("english");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getSession().then(setSessionId);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend() {
    if (!input.trim() || !sessionId || loading) return;
    const text = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);
    try {
      const res = await sendMessage(sessionId, text);
      setResponseLang(res.response_language);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.reply, sources: res.sources },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-[calc(100dvh-2rem)] max-w-2xl mx-auto flex-col rounded-2xl border border-border bg-background shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3">
        <div className="flex items-center gap-2.5">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-green-500" />
          </span>
          <span className="text-sm font-medium">Research Assistant</span>
        </div>
        <LanguageBadge lang={responseLang} />
      </div>
      <Separator />

      {/* Messages */}
      <ScrollArea className="flex-1 px-4 py-4">
        <div className="flex flex-col gap-3">
          {messages.map((msg, i) => (
            <MessageBubble
              key={i}
              role={msg.role}
              content={msg.content}
              sources={msg.sources}
            />
          ))}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>
      <Separator />

      {/* Input */}
      <div className="flex items-end gap-2 px-4 py-3">
        <textarea
          className="flex-1 resize-none rounded-xl border border-border bg-muted px-3.5 py-2.5 text-sm outline-none focus:ring-1 focus:ring-ring placeholder:text-muted-foreground"
          rows={1}
          placeholder="Ask about the research… (English or Filipino)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <Button
          size="icon"
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="shrink-0 rounded-xl"
        >
          <SendHorizontal className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}