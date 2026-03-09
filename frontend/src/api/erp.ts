import { api } from "./client"
import { QuestionRequest, QuestionResponse, Invoice } from "../types/api"

export const askQuestion = async (
  payload: QuestionRequest
): Promise<QuestionResponse> => {
  const { data } = await api.post<QuestionResponse>("/question", payload)
  return data
}

export const getInvoices = async (): Promise<Invoice[]> => {
  const { data } = await api.get<Invoice[]>("/invoices")
  return data
}