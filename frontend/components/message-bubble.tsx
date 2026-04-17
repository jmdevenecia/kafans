import { cn } from "@/lib/utils";

interface Props {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

export function MessageBubble({ role, content, sources }: Props) {
  const isUser = role === "user";
  return (
    <div className={cn("flex flex-col gap-1", isUser ? "items-end" : "items-start")}>
      <div
        className={cn(
          "max-w-[78%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed",
          isUser
            ? "rounded-br-sm bg-primary text-primary-foreground"
            : "rounded-bl-sm bg-muted text-foreground"
        )}
      >
        {content}
      </div>
      {sources && sources.length > 0 && (
        <div className="flex flex-wrap gap-1 px-1">
          {sources.map((src) => (
            <span
              key={src}
              className="rounded-full border border-border bg-background px-2 py-0.5 text-[11px] text-muted-foreground"
            >
              {src}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}