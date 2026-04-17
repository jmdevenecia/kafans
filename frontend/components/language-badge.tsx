import { Badge } from "@/components/ui/badge";

interface Props {
  lang: "english" | "filipino";
}

export function LanguageBadge({ lang }: Props) {
  return (
    <Badge
      variant="outline"
      className={
        lang === "filipino"
          ? "border-blue-400 text-blue-600 dark:text-blue-400"
          : "border-slate-300 text-slate-500 dark:border-slate-600 dark:text-slate-400"
      }
    >
      {lang === "filipino" ? "🇵🇭 Filipino" : "🇺🇸 English"}
    </Badge>
  );
}