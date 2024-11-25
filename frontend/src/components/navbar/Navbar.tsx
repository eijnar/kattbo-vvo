import React from "react";
import NavbarLeft from "./NavbarLeft";
import NavbarCenter from "./NavbarCenter";
import NavbarRight from "./NavbarRight";

const Navbar: React.FC = () => {
  return (
    <nav className="bg-primary text-white px-4 py-3 flex justify-between items-center">
      <NavbarLeft />
      <NavbarCenter />
      <NavbarRight />
    </nav>
  );
};

export default Navbar;
