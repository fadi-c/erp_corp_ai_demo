import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import rehypeHighlight from "rehype-highlight"
import "highlight.js/styles/github-dark.css"

type Props = {
  role: "user" | "assistant"
  content: string
  isLoading?: boolean
}

export default function ChatBubble({ role, content, isLoading }: Props) {
  const isUser = role === "user"

  return (
    <div className={`flex w-full mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`
          max-w-[780px]
          px-[10px] py-[8px]
          rounded-[20px]
          shadow-lg
          text-sm leading-relaxed
          ${isUser
            ? "bg-gradient-to-r from-indigo-500 to-blue-500 text-white"
            : "bg-[#1b2437] text-[#e0e6f3]"
          }
        `}
      >
        {isLoading && !isUser ? (
          <div className="flex gap-2 items-center justify-start h-6">
            <span className="bg-indigo-400 w-2.5 h-2.5 rounded-full animate-bounce"></span>
            <span className="bg-indigo-400 w-2.5 h-2.5 rounded-full animate-bounce-delay-150"></span>
            <span className="bg-indigo-400 w-2.5 h-2.5 rounded-full animate-bounce-delay-300"></span>
          </div>
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeHighlight]}
            className="prose prose-invert max-w-full break-words"
          >
            {normalizeMarkdown(content)}
          </ReactMarkdown>
        )}
      </div>
    </div>
  )
}

function normalizeMarkdown(text: string) {
  if (!text) return ""
  return text
    .replace(/\n\|/g, "\n\n|")       // Tables
    .replace(/\n- /g, "\n\n- ")       // Listes
    .replace(/\n#/g, "\n\n#")         // Titres
}