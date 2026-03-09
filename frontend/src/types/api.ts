export interface QuestionRequest {
  question: string
}

export interface QuestionResponse {
  answer: string
  sources: number[]
}

export interface Invoice {
  id: number
  amount: number
  margin: number
  date: string
  description: string
}