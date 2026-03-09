import { useMutation } from "@tanstack/react-query"
import { askQuestion } from "../api/erp"

export const useAskQuestion = () => {
  return useMutation({
    mutationFn: askQuestion
  })
}