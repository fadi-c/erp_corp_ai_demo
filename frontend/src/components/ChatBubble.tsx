// FILE: ./frontend/src/components/ChatBubble.tsx
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import rehypeHighlight from "rehype-highlight"
import "highlight.js/styles/github-dark.css"

type Props = {
  role: "user" | "assistant"
  content: string
}

export default function ChatBubble({ role, content }: Props) {
  const isUser = role === "user"

  return (
    <div className={`flex w-full mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`
          max-w-[780px]
          px-[5px] py-[5px]         /* padding interne 5px */
          rounded-[20px]            /* bordure arrondie 20px */
          shadow-lg
          text-sm leading-relaxed
          ${isUser
            ? "bg-gradient-to-r from-indigo-500 to-blue-500 text-white"
            : "bg-[#1b2437] text-[#e0e6f3]"
          }
        `}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeHighlight]}
          className="prose prose-invert max-w-full break-words"
        >
          {normalizeMarkdown(content)}
        </ReactMarkdown>
      </div>
    </div>
  )
}

// Normalise le Markdown pour ajouter des sauts de ligne corrects
function normalizeMarkdown(text: string) {
  if (!text) return ""
  return text
    .replace(/\n\|/g, "\n\n|")       // Tables
    .replace(/\n- /g, "\n\n- ")       // Listes
    .replace(/\n#/g, "\n\n#")         // Titres
}