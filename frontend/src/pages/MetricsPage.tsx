import { useInvoices } from "../hooks/useInvoices"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts"

export default function MetricsPage() {

  const { data, isLoading } = useInvoices()

  if (isLoading)
    return <div className="p-10 text-[#9aa4b2]">Loading metrics...</div>

  const totalRevenue = data?.reduce((s, i) => s + i.amount, 0) ?? 0
  const totalMargin = data?.reduce((s, i) => s + i.margin, 0) ?? 0

const chartData =
  data
    ?.slice() // clone pour ne pas muter
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map((i) => ({
      date: i.date,
      revenue: i.amount
    })) ?? []

  return (

    <div className="p-10">

      <h1 className="text-3xl font-semibold mb-8">
        ERP Metrics
      </h1>

      <div className="grid md:grid-cols-3 gap-6 mb-10">

        <MetricCard title="Revenue" value={`${totalRevenue} €`} />
        <MetricCard title="Margin" value={`${totalMargin} €`} />
        <MetricCard title="Invoices" value={`${data?.length ?? 0}`} />

      </div>

      <div className="bg-[#121a2b] border border-[#243047] rounded-xl p-6 h-[420px]">

        <ResponsiveContainer width="100%" height="100%">

          <LineChart data={chartData}>

            <XAxis dataKey="date" stroke="#6b7280" />
            <YAxis stroke="#6b7280" />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#7c83ff"
              strokeWidth={3}
              dot={false}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  )
}

function MetricCard({ title, value }: any) {

  return (

    <div className="bg-[#121a2b] border border-[#243047] rounded-xl p-6">

      <p className="text-sm text-[#9aa4b2]">
        {title}
      </p>

      <p className="text-3xl font-semibold mt-2">
        {value}
      </p>

    </div>

  )
}