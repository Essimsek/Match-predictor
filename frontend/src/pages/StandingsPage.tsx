import api from "../api/api";
import { useQuery } from "@tanstack/react-query";

type Standings = {
    team: string;
    points: number;
    logo: string;
    position: string;
}

const TeamCard = ({ team, points, position, logo }: Standings) => {
    const teamPosition = parseInt(position);
    let borderClass = "border-l-gray-100/50"
    if (teamPosition == 1) borderClass ="border-l-blue-500"
    else if (teamPosition == 2) borderClass ="border-l-[#FA7B17]"
    else if (teamPosition == 3) borderClass ="border-l-[#34A853]"
    else if (teamPosition == 4) borderClass ="border-l-[#24C1E0]"
    else if (19 - teamPosition < 4) borderClass = "border-l-red-500" // last 4 team's border color should be red
    return (
        <div className={`flex items-center justify-between p-4 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50 
                       border-b border-b-gray-100 transition-colors border-l-[3px] ${borderClass}`}>
            <div className="flex items-center gap-4 w-full">
                <span className="text-gray-500 dark:text-gray-400 font-medium w-8 text-center">
                    {position}
                </span>
                
                <div className="flex items-center gap-4 flex-1">
                    <img 
                        src={logo} 
                        alt={`${team} logo`} 
                        className="w-4 h-4 object-contain"
                    />
                    <h3 className="font-medium text-gray-800 dark:text-gray-200">
                        {team}
                    </h3>
                </div>
                
                <div className="flex items-center gap-2">
                    <span className="text-gray-600 dark:text-gray-400">PTS</span>
                    <span className="font-semibold text-blue-600 dark:text-blue-400">
                        {points}
                    </span>
                </div>
            </div>
        </div>
    )
}

const StandingsPage = () => {
    const { isPending, error, data: standings } = useQuery<Standings[]>({
        queryKey: ['standingsData'],
        queryFn: async () => {
            const response = await api.get<Standings[]>("/standings");
            return response.data;
        },
    });
    
    if (isPending) return <h1 className="dark:text-white text-blue-500">Loading...</h1>;
    
    if (error) return <h1 className="dark:text-white text-blue-500">Error: {error.message}</h1>;

    return (
        <div className="min-h-screen p-5 container mx-auto">
        <h1 className="text-3xl font-semibold text-center mb-8 text-gray-800 dark:text-gray-100 
                    relative pb-2
                    after:content-[''] after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 
                    after:w-20 after:h-1 after:bg-gradient-to-r after:from-blue-400 after:to-transparent 
                    after:rounded-full">
            League Standings
        </h1>
            <div className="max-w-4xl mx-auto rounded-xl overflow-hidden shadow-lg 
                           bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800">
                <div className="px-4 py-3 bg-gray-100 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700">
                    <div className="flex items-center gap-4 text-sm font-semibold text-gray-600 dark:text-gray-400">
                        <span className="w-8 text-center">#</span>
                        <span className="flex-1">Team</span>
                        <span className="w-24 text-right">Points</span>
                    </div>
                </div>
                <div>
                    {standings.map((standing) => (
                        <TeamCard
                            key={standing.position}
                            team={standing.team}
                            points={standing.points}
                            logo={standing.logo}
                            position={standing.position}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default StandingsPage;
