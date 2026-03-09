import { useState, useRef, useEffect } from "react"
import { useAskQuestion } from "../hooks/useAskQuestion"
import ChatBubble from "../components/ChatBubble"
import { ArrowUp, Loader2 } from "lucide-react"
import { motion } from "framer-motion"

type Message = {
  role: "user" | "assistant"
  content: string
  isLoading?: boolean
}

export default function PromptPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const askMutation = useAskQuestion()

  const ask = async () => {
    if (!input.trim()) return

    const question = input
    setMessages((m) => [...m, { role: "user", content: question }])
    setInput("")

    setMessages((m) => [...m, { role: "assistant", content: "", isLoading: true }])

    try {
      const res = await askMutation.mutateAsync({ question })

      setMessages((m) => {
        const newMessages = [...m]
        const lastIndex = newMessages.findIndex(
          (msg) => msg.role === "assistant" && msg.isLoading
        )
        if (lastIndex !== -1) {
          newMessages[lastIndex] = { role: "assistant", content: res.answer }
        }
        return newMessages
      })
    } catch {
      setMessages((m) => {
        const newMessages = [...m]
        const lastIndex = newMessages.findIndex(
          (msg) => msg.role === "assistant" && msg.isLoading
        )
        if (lastIndex !== -1) {
          newMessages[lastIndex] = { role: "assistant", content: "Error contacting ERP AI." }
        }
        return newMessages
      })
    }
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="flex flex-col h-screen bg-[#0f1629] text-white">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 md:px-10 py-6">
        <div className="max-w-5xl mx-auto w-full">
          {messages.length === 0 && (
            <div className="text-center mt-40" style={{paddingTop:20}}>
              <h1 className="text-4xl font-semibold mb-3 text-white">
                ERP AI Assistant
              </h1>
              <p className="text-gray-400 text-lg">
                Ask anything about your ERP data.
              </p>
            </div>
          )}

          {messages.map((m, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
            >
              <ChatBubble {...m} />
            </motion.div>
          ))}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input Form */}
      <div className="p-4 md:p-6">
        <div className="max-w-5xl mx-auto flex items-center gap-3 mb-[10px]">
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                ask()
              }
            }}
            placeholder="Ask ERP AI..."
            className="
              flex-1
              min-h-[48px]
              max-h-[160px]
              resize-none
              px-4
              py-3
              rounded-3xl
              bg-[#0f1729]
              text-white
              placeholder:text-[#9aa4b2]
              outline-none
              text-base
              leading-relaxed
            "
          />
          <button
            onClick={ask}
            disabled={askMutation.isPending || !input.trim()}
            className="
              flex items-center justify-center w-12 h-12 rounded-full
              bg-indigo-600
              text-white
              border border-gray-700
              shadow-md
              transition-all duration-150 ease-in-out
              hover:bg-indigo-500
              hover:scale-105
              hover:shadow-lg
              disabled:opacity-50
              disabled:cursor-not-allowed
            "
          >
            {askMutation.isPending ? (
              <Loader2 className="animate-spin text-white" size={24} />
            ) : (
              <ArrowUp size={23} className="text-white" />
            )}
          </button>
        </div>
      </div>
    </div>
  )
}