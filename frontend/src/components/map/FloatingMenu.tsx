// src/components/map/FloatingMenu.tsx
import { MagnifyingGlassIcon, MinusIcon, PlusIcon, Square3Stack3DIcon } from '@heroicons/react/16/solid';
import React from 'react';

const FloatingMenu: React.FC<any> = ({

}) => {
  return (
    <div className="absolute top-4 right-4 flex flex-col space-y-2 z-10">
      {/* Search Button */}
      <button
        className="p-3 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none"
        aria-label="Search"
      >
        <MagnifyingGlassIcon className="text-gray-700 dark:text-gray-200" />
      </button>

      {/* Add Marker Button */}
      <button
        className="p-3 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none"
        aria-label="Add Marker"
      >
        <PlusIcon className="text-gray-700 dark:text-gray-200" />
      </button>

      {/* Zoom In Button */}
      <button
        className="p-3 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none"
        aria-label="Zoom In"
      >
        <PlusIcon className="text-gray-700 dark:text-gray-200" />
      </button>

      {/* Zoom Out Button */}
      <button
        className="p-3 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none"
        aria-label="Zoom Out"
      >
        <MinusIcon className="text-gray-700 dark:text-gray-200" />
      </button>

      {/* Toggle Layers Button */}
      <button
        className="p-3 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none"
        aria-label="Toggle Layers"
      >
        <Square3Stack3DIcon className="text-gray-700 dark:text-gray-200" />
      </button>

    </div>
  );
};

export default FloatingMenu;
