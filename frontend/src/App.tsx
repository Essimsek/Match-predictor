import { Outlet } from "@tanstack/react-router"
import Navbar from "./components/Navbar"
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {

  return (
    <QueryClientProvider client={queryClient}>
      <div className="bg-white dark:bg-gray-900 transition-colors duration-300">
        <Navbar />
        <Outlet />
      </div>
    </QueryClientProvider>
  )
}

export default App
