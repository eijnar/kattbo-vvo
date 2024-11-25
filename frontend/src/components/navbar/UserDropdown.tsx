import React, { useState, useRef } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import DropdownMenu from "./DropdownMenu";

const UserDropdown: React.FC = () => {
  const { user } = useAuth0();
  const [dropdownOpen, setDropdownOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const toggleDropdown = () => setDropdownOpen((prev) => !prev);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={toggleDropdown}
        className="flex items-center space-x-2 focus:outline-none"
      >
        {/* User Avatar */}
        <img
          src={user?.picture}
          alt={user?.name}
          className="w-8 h-8 rounded-full"
        />
        {/* User Name */}
        <span>{user?.name}</span>
        {/* Dropdown Icon */}
        <svg
          className="w-4 h-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Dropdown Menu */}
      <DropdownMenu
        isOpen={dropdownOpen}
        setIsOpen={setDropdownOpen}
        dropdownRef={dropdownRef}
      />
    </div>
  );
};

export default UserDropdown;
