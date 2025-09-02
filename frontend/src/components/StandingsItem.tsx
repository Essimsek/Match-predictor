export type Standings = {
    team: string;
    points: number;
    logo: string;
    position: string;
}

const StandingsItem = ({ team, points, position, logo }: Standings) => {
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

export default StandingsItem;
