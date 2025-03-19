import { Outlet } from "@tanstack/react-router"
import Navbar from "./components/Navbar"

function App() {

  return (
    <div className="bg-white dark:bg-gray-900 transition-colors duration-300">
      <Navbar />
      <Outlet />
    </div>
  )
}

export default App