import React, { useEffect } from "react";
import { NavLink } from "react-router-dom";
import LogoutButton from "../auth/LogoutButton";

interface DropdownMenuProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  dropdownRef: React.RefObject<HTMLDivElement>;
}

const DropdownMenu: React.FC<DropdownMenuProps> = ({ isOpen, setIsOpen, dropdownRef }) => {
  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen, dropdownRef, setIsOpen]);

  if (!isOpen) return null;

  return (
    <div className="absolute right-0 mt-2 w-48 bg-white text-black rounded-md shadow-lg py-1 z-50">
      <NavLink
        to="/profile"
        className="block px-4 py-2 text-sm hover:bg-gray-100"
        onClick={() => setIsOpen(false)}
      >
        Profil
      </NavLink>

      <NavLink
        to="/create-api-key"
        className="block px-4 py-2 text-sm hover:bg-gray-100"
        onClick={() => setIsOpen(false)}
      >
        API nycklar
      </NavLink>
      <div className="border-t border-gray-200"></div>
      <LogoutButton className="w-full text-left text-sm hover:bg-gray-100 px-4 py-2" />
    </div>
  );
};

export default DropdownMenu;

