import FixtureCard from "../components/FixtureCard";

export type FixturesType = {
  away: string;
  away_logo: string;
  home: string;
  home_logo: string;
  id: string;
  status: string;
  value: string;
};

type FixturesListProps = {
  fixtures: FixturesType[];
};

function FixturesList({ fixtures }: FixturesListProps) {
  return (
    <div className="grid gap-4">
      {fixtures.map((fixture) => (
        <FixtureCard key={fixture.id} fixture={fixture} />
      ))}
    </div>
  );
}

export default FixturesList;
