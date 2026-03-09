import { useQuery } from "@tanstack/react-query"
import { getInvoices } from "../api/erp"

export const useInvoices = () =>
  useQuery({
    queryKey: ["invoices"],
    queryFn: getInvoices
  })