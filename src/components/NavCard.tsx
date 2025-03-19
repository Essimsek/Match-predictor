import  { Link } from "@tanstack/react-router";

const NavCard = ({ icon, to, text, description }: {
  icon: React.ReactNode,
  to: string,
  text: string,
  description?: string
}) => {
  return (
    <Link to={to}>
      <div className="flex flex-col justify-center items-center gap-3 w-[300px] p-6 h-fit border-2 border-gray-400 rounded-2xl hover:border-gray-700 transition-colors duration-200 dark:border-gray-700 dark:hover:border-blue-400 group">
        <div className="p-3 bg-blue-50/50 dark:bg-gray-700 rounded-full group-hover:bg-blue-100 dark:group-hover:bg-gray-600 transition-colors">
          {icon}
        </div>
        <div className="text-center">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">{text}</h3>
          {description && (
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
              {description}
            </p>
          )}
        </div>
      </div>
    </Link>
  )
}

export default NavCard;