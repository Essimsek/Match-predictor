import { Link } from "@tanstack/react-router";
import IconSwitch from "./IconSwitch";

type NavbarProps = {
    onThemeChange: () => void;
    mode: "light" | "dark";
}

const Navbar = ({ onThemeChange, mode }: NavbarProps) => {
    return (
        <nav className="container flex flex-row justify-between items-center p-4 mx-auto">
            <div className="flex order-1">
                <IconSwitch onChange={onThemeChange} checked={mode == "dark"} />
            </div>
            <div className="w-14 h-6 flex rounded-xl justify-center items-center">
                <Link to="/" >Home</Link>
            </div>
        </nav>
    );
}

export default Navbar;
