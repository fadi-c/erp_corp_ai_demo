import { useState, useEffect } from "react"
import { api } from "../api/client"
import { ChevronLeft, ChevronRight } from "lucide-react"

type Invoice = {
  id: number
  date: string
  customer: string
  amount: number
  margin: number
  description?: string
}

export default function MetricsPage() {
  const [data, setData] = useState<Invoice[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(20)
  const [totalPages, setTotalPages] = useState<number>(1)

  const fetchInvoices = async (page: number, pageSize: number) => {
    setIsLoading(true)
    try {
      const response = await api.get("/invoices", {
        params: { page, page_size: pageSize }
      })

      const invoices: Invoice[] = Array.isArray(response.data.results)
        ? response.data.results
        : []

      setData(invoices)
      setTotalPages(response.data.num_pages ?? 1)
    } catch (err) {
      console.error("Failed to fetch invoices", err)
      setData([])
      setTotalPages(1)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchInvoices(page, pageSize)
  }, [page, pageSize])

  const handlePrev = () => setPage((p) => Math.max(1, p - 1))
  const handleNext = () => setPage((p) => Math.min(totalPages, p + 1))

  return (
    <div className="p-6 md:p-10 bg-[#0f172a] min-h-screen text-white">
            <div className="text-center mt-40" style={{paddingTop:20}}>
              <h1 className="text-4xl font-semibold mb-3 text-white">
                Invoices
              </h1>
            </div>   

      {isLoading ? (
        <div className="p-6 text-[#9aa4b2]">Loading invoices...</div>
      ) : (
        <>
          <div className="overflow-x-auto rounded-xl border border-[#243047]">
            <table className="min-w-full divide-y divide-[#243047]">
              <thead className="bg-[#121a2b]">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-[#9aa4b2]">ID</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-[#9aa4b2]">Date</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-[#9aa4b2]">Customer</th>
                  <th className="px-6 py-3 text-right text-sm font-semibold text-[#9aa4b2]">Amount (€)</th>
                  <th className="px-6 py-3 text-right text-sm font-semibold text-[#9aa4b2]">Margin (€)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#243047] bg-[#0f172a]">
                {data.map((invoice) => (
                  <tr key={invoice.id} className="hover:bg-[#121a2b] transition-colors">
                    <td className="px-6 py-4 text-sm">{invoice.id}</td>
                    <td className="px-6 py-4 text-sm">{invoice.date}</td>
                    <td className="px-6 py-4 text-sm">{invoice.description ?? invoice.customer}</td>
                    <td className="px-6 py-4 text-sm text-right">{invoice.amount.toFixed(2)}</td>
                    <td className="px-6 py-4 text-sm text-right">{invoice.margin.toFixed(2)}</td>
                  </tr>
                ))}
                {data.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-6 py-4 text-center text-[#9aa4b2]">
                      No invoices found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex justify-between items-center mt-4">
            <button
              onClick={handlePrev}
              disabled={page === 1}
              className="flex items-center gap-2 px-4 py-2 bg-[#121a2b] text-[#9aa4b2] rounded-xl disabled:opacity-50 hover:bg-[#243047] transition"
            >
              <ChevronLeft size={18} /> Prev
            </button>

            <span className="text-sm text-[#9aa4b2]">
              Page {page} of {totalPages}
            </span>

            <button
              onClick={handleNext}
              disabled={page === totalPages}
              className="flex items-center gap-2 px-4 py-2 bg-[#121a2b] text-[#9aa4b2] rounded-xl disabled:opacity-50 hover:bg-[#243047] transition"
            >
              Next <ChevronRight size={18} />
            </button>
          </div>
        </>
      )}
    </div>
  )
}