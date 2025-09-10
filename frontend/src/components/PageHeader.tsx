
const PageHeader = ({title}: {title: string}) => {
    return (
        <h1 className="text-3xl font-semibold text-center mb-8 text-gray-800 dark:text-gray-100 
                    relative pb-2
                    after:content-[''] after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 
                    after:w-20 after:h-1 after:bg-gradient-to-r after:from-blue-400 after:to-transparent 
                    after:rounded-full">
            {title}
        </h1>
    );
}

export default PageHeader;
