import PageHeader from "../components/PageHeader";
import { useQuery } from "@tanstack/react-query";
import FixtureList, {FixturesType} from "../components/FixturesList";
import api from "../api/api";


const FixturesPage = () => {
    const { isPending, error, data: fixtures } = useQuery<FixturesType[]>({
        queryKey: ['FixturesData'],
        queryFn: async () => {
            const response = await api.get<FixturesType[]>("/fixtures")
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
            <PageHeader title="League Fixtures" />
            <FixtureList fixtures={fixtures}/>
        </div>
    );
}

export default FixturesPage;
