import { Link } from "@tanstack/react-router";

const NavCard = ( {icon, to, text}: {
  icon: React.ReactNode,
  to: string,
  text:  string,
} ) => {
  return (
    <Link to={to}>
    <div className="flex flex-col justify-center items-center gap-3 w-[300px] p-4 h-fit border-2 border-amber-100 rounded-2xl hover:border-blue-200 transition-colors duration-200 dark:border-gray-700 dark:hover:border-blue-400">
      {icon}
      {text}
    </div>
  </Link>
  )
}

const HomePage = () => {
  return (
    <div className="h-screen">
        <div className="flex flex-col gap-3 mt-14 w-full justify-center items-center">
          <div className="p-4 rounded-lg">
            <h1 className="text-5xl md:text-6xl font-bold bg-clip-text text-center text-transparent bg-gradient-to-r from-blue-600 to-purple-500">
              Football Tracker
            </h1>
          </div>
          <div className="flex flex-row flex-wrap gap-3 mt-14 items-center justify-center">

            <NavCard 
              to="/standings" 
              text="Standings"
              icon={
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              }
            />
            <NavCard 
              to="/fixtures" 
              text="fixtures"
              icon={
                <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              }
            />
            {/* predictions card */}
          </div>
        </div>
    </div>
  )
}

export default HomePage;
