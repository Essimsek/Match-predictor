import api from "../api/api";
import { useQuery } from "@tanstack/react-query";
import StandingsItem, {Standings} from "../components/StandingsItem";
import PageHeader from "../components/PageHeader";

const StandingsPage = () => {
    const { isPending, error, data: standings } = useQuery<Standings[]>({
        queryKey: ['standingsData'],
        queryFn: async () => {
            const response = await api.get<Standings[]>("/standings");
            return response.data;
        },
    });
    
    if (isPending) return (
        <div className="flex justify-center items-center min-h-[120px] w-full">
            <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-blue-500 dark:border-white mr-4"></div>
            <span className="text-blue-500 dark:text-white text-lg font-semibold">Loading...</span>
        </div>
    );
    
    if (error) return <h1 className="dark:text-white text-blue-500">Error: {error.message}</h1>;

    return (
        <div className="min-h-screen p-5 container mx-auto">
            <PageHeader title="League Standings" />
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
                        <StandingsItem
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
