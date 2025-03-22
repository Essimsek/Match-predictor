import { Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";

const Navbar = () => {
  const [mode, setMode] = useState<"light" | "dark">(localStorage.getItem('theme') === 'dark' ? 'dark' : 'light');
  
  useEffect(() => {
    const changeTheme = () => {
      if (mode === 'dark') {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      }
      else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    }
    changeTheme();
  }, [mode]);

  const handleChengeMode = () => {
    setMode((prevMode)  => prevMode === 'light' ? 'dark': 'light')
  }

  return (
    <nav className="container flex flex-row justify-between items-center p-7 mx-auto sticky top-0 z-10 bg-white dark:bg-gray-900 border-b dark:border-gray-700">
      <div className="flex order-1">
        <button
          onClick={handleChengeMode}
          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          {mode === 'dark' ? (
            <svg className="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
            </svg>
          ) : (
            <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          )}
        </button>
      </div>
      
      <div className="w-14 h-6 flex rounded-xl justify-center items-center">
        <Link to="/">
          <h2 className="text-2xl font-bold bg-clip-text p-4 text-transparent bg-gradient-to-r ml-5 from-blue-500 to-yellow-500">
            LigPulse
          </h2>
        </Link>
      </div>
    </nav>
  )
}

export default Navbar;
