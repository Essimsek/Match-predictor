import { useEffect, useState } from "react";
import api from "../api/api";

type Standings = {
    team: string;
    points: number;
    logo: string;
    position: string;
}

const StandingsPage = () => {
    const [standings, setStandings] = useState<Standings[]>([]);
    useEffect(() => {
        const fetchStandings = async () => {
            try {
                const response = await api.get<Standings[]>("/standings");
                setStandings(response.data);
            }
            catch (error) {
                console.error("Error fetching standings data:", error);
            }
        }
        fetchStandings();
    }, []);
    return (
        <div className="h-screen p-5">
            {standings.map((standing, index) => (
                <h1 className="dark:text-white text-blue-500" key={index}>{standing.team}</h1>
            ))}
        </div>
    );
}

export default StandingsPage;
