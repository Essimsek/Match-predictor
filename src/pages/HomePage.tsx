import { Link } from "@tanstack/react-router";

const HomePage = () => {
  return (
    <div className="p-2">
        <h3>Welcome Home!</h3>
        <div className="inline-flex flex-col gap-3 mt-5">
         <Link className="bg-red-400" to="/standings">Standings</Link>
         <Link className="bg-red-400" to="/fixtures">Fixtures</Link>
        </div>
    </div>
  )
}

export default HomePage;
