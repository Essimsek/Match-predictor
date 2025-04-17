// get the standings data from api
import axios from "axios";
import { useEffect, useState } from "react";

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
                const response = await axios.get<Standings[]>("http://localhost:3000/api/standings");
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
                <h1 key={index}>{standing.team}</h1>
            ))}
        </div>
    );
}

export default StandingsPage;
