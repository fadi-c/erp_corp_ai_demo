// FILE: ./frontend/src/components/DashboardLayout.tsx
import { Outlet, Link, useLocation } from "react-router-dom"
import { MessageSquare, BarChart3, Github, ExternalLink } from "lucide-react"

const EXTERNAL_GRAFANA = import.meta.env.VITE_GRAFANA_URL
const EXTERNAL_GITHUB = import.meta.env.VITE_GITHUB_URL

type NavItem = {
  to: string
  label: string
  icon: React.ComponentType<{ size?: number }>
  external?: boolean
}

export default function DashboardLayout() {
  const location = useLocation()

  const nav: NavItem[] = [
    { to: "/", label: " Chat with AI", icon: MessageSquare, external: false },
    { to: "/metrics", label: " ERP Datas", icon: BarChart3, external: false },
    { to: EXTERNAL_GRAFANA, label: " Grafana", icon: ExternalLink, external: true },
    { to: EXTERNAL_GITHUB, label: " GitHub", icon: Github, external: true }
  ]

  return (
    <div className="flex h-screen bg-[#0f172a] text-white">

      <aside
        style={{ minWidth: "185px" }}
        className="flex flex-col w-96 md:w-[420px] bg-[#0a101f] shadow-lg rounded-tr-3xl rounded-br-3xl overflow-hidden h-screen"
      >
        {/* Navigation */}
        <nav className="flex flex-col justify-center mt-6 gap-6 flex-1 overflow-auto px-6">
          {nav.map((item) => {
            const isActive = !item.external && location.pathname === item.to
            const Icon = item.icon

            return item.external ? (
              <a
                key={item.label}
                href={item.to}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-4 pl-4 pr-6 py-4 rounded-3xl transition-all duration-200 hover:bg-[#121a2b] hover:text-indigo-400"
              >
                <Icon size={22} className="text-indigo-300 transition-colors" />
                <span className="font-medium text-indigo-200">{item.label}</span>
              </a>
            ) : (
              <Link
                key={item.label}
                to={item.to}
                className={`flex items-center gap-4 pl-4 pr-6 py-4 rounded-3xl transition-all duration-200 ${isActive
                    ? "bg-indigo-500 text-white shadow-md scale-105"
                    : "text-indigo-200 hover:text-indigo-400 hover:bg-[#121a2b]"
                  }`}
              >
                <Icon size={22} />
                <span className="font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>
      </aside>
      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden px-12 py-8">
        <Outlet />
      </main>

    </div>
  )
}