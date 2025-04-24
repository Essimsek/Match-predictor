import api from "../api/api";
import { useQuery } from "@tanstack/react-query";

type Standings = {
    team: string;
    points: number;
    logo: string;
    position: string;
}

const TeamCard = ({ team, points, position, logo }: Standings) => { 
    return (
        <div className="flex flex-row flex-nowrap justify-center items-center bg-white dark:bg-gray-800 
                    rounded-lg shadow-lg p-4 m-2 w-1/3 gap-2 *
                    hover:bg-blue-50/50 dark:hover:bg-transparent text-gray-800 dark:text-gray-200
                    border-2 border-gray-200 dark:border-gray-600 transition-colors dark:hover:border-blue-400 hover:border-blue-400">
            <img src={logo} alt={`${team} logo`} className="w-8 h-8 rounded-full" />
            <p className="">{position}-)</p>
            <h2>{team}</h2>
            <p>{points}</p>
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
        <div className="min-h-screen p-5 container mx-auto flex flex-col justify-center items-center gap-0.5">
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
    );
}

export default StandingsPage;
