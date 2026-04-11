import Link from 'next/link';

interface ToolCardProps {
  icon: string;
  title: string;
  description: string;
  href: string;
}

export default function ToolCard({ icon, title, description, href }: ToolCardProps) {
  return (
    <div className="p-6 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 hover:border-blue-400 dark:hover:border-blue-600 transition-all hover:shadow-lg flex flex-col">
      <div className="text-5xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-6 flex-grow">
        {description}
      </p>
      <Link
        href={href}
        className="inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium text-sm w-full"
      >
        Open Tool
      </Link>
    </div>
  );
}
