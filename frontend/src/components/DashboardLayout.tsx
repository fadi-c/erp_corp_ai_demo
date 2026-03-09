import { Outlet, Link, useLocation } from "react-router-dom"
import { MessageSquare, BarChart3, Github, ExternalLink } from "lucide-react"

const EXTERNAL_GRAFANA = import.meta.env.VITE_GRAFANA_URL
const EXTERNAL_GITHUB = import.meta.env.VITE_GITHUB_URL

type NavItem = {
  to: string
  label: string
  icon: React.ComponentType<{ size?: number }>
  credentials?: string
  external?: boolean
}

export default function DashboardLayout() {
  const location = useLocation()

  const nav: NavItem[] = [
    { to: EXTERNAL_GITHUB, label: "GitHub", icon: Github, external: true },
    { to: "/", label: "Chat with AI", icon: MessageSquare },
    { to: "/metrics", label: "ERP Datas", icon: BarChart3 },
    { to: EXTERNAL_GRAFANA, label: "Grafana", icon: ExternalLink, credentials: "user: demo  pass: demo", external: true },
  ]

  return (
    <div className="flex flex-col h-screen bg-[#0f172a] text-white relative">
      {/* Navbar flottante */}
      <header className="fixed top-0 left-0 w-full bg-[#0a101f] shadow-md z-50 pointer-events-auto">
        <nav className="container mx-auto flex flex-wrap justify-center md:justify-center items-center gap-4 py-4 px-6">
          {nav.map((item) => {
            const isActive = !item.external && location.pathname === item.to
            const Icon = item.icon

            return item.external ? (
              <a
                key={item.label}
                href={item.to}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-200 hover:bg-[#121a2b] hover:text-indigo-400"
              >
                <Icon size={20} className="text-indigo-300" />
                <span className="text-indigo-200 font-medium text-sm">{item.label}</span>
              </a>
            ) : (
              <Link
                key={item.label}
                to={item.to}
                className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-200 text-sm font-medium ${
                  isActive ? "bg-indigo-500 text-white shadow-md scale-105" : "text-indigo-200 hover:text-indigo-400 hover:bg-[#121a2b]"
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>
      </header>

      {/* Main content qui défile sous la navbar */}
      <main className="flex-1 flex flex-col overflow-hidden relative pt-20 p-6 md:p-12">
        {/* Outlet scrollable */}
        <div className="flex-1 overflow-auto">
          <Outlet />
        </div>
      </main>
    </div>
  )
}