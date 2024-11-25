import React from "react";
import { NavLink } from "react-router-dom";

const NavbarLeft: React.FC = () => {
  return (
    <div className="flex-none">
      <NavLink to="/" className="text-xl font-bold">
        Kättbo VVO
      </NavLink>
    </div>
  );
};

export default NavbarLeft;
