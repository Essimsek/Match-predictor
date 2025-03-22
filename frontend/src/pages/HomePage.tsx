import NavCard from "../components/NavCard";

const HomePage = () => {
  return (
    <div className="h-screen p-5">
        <div className="flex flex-col gap-3 mt-14 w-full justify-center items-center">
          <div className="p-4 rounded-lg">
            <h1 className="text-5xl md:text-6xl font-bold p-3 bg-clip-text text-center text-transparent bg-gradient-to-r from-blue-600 to-purple-500">
              Trendyol Super League Match Predictor
            </h1>
          </div>
          <p className="mt-4 text-gray-600 dark:text-gray-400 text-center max-w-2xl mx-auto">
          Keep your finger on the pulse of Super League! Live scores, current standings and smart match predictions 
          follow the season closely.
          </p>
          <div className="flex flex-row flex-wrap gap-3 mt-14 items-center justify-center">
            <NavCard 
              to="/standings"  
              text="Standings"
              icon={
                <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              }
              description="Check out the current standings"
            />
            <NavCard 
              to="/fixtures" 
              text="Fixtures"
              icon={
                <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              }
              description="Check out the upcoming matches"
            />
            {/* predictions card */}
          </div>
          <p className="mt-12 text-sm text-gray-500 text-center dark:text-gray-400">
            Data updated in real-time • Let the AI predict the results for you
          </p>
        </div>
    </div>
  )
}

export default HomePage;
