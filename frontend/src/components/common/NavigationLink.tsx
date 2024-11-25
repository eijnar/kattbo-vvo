import React from "react";
import { NavLink } from "react-router-dom";

interface NavigationLinkProps {
  to: string;
  children: React.ReactNode;
}

const NavigationLink: React.FC<NavigationLinkProps> = ({ to, children }) => {
  return (
    <NavLink
      to={to}
      className="px-4 py-2 text-sm hover:bg-gray-100 hover:text-black rounded"
    >
      {children}
    </NavLink>
  );
};

export default NavigationLink;
