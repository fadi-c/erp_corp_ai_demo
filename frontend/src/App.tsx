import { BrowserRouter, Routes, Route } from "react-router-dom"
import DashboardLayout from "./components/DashboardLayout"
import PromptPage from "./pages/PromptPage"
import MetricsPage from "./pages/MetricsPage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<PromptPage />} />
          <Route path="/metrics" element={<MetricsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}