import React from "react";
import NavigationLink from "../common/NavigationLink";

const NavbarCenter: React.FC = () => {
  return (
    <div className="flex-1 flex justify-center space-x-6">
      <NavigationLink to="/users">Användare</NavigationLink>
      <NavigationLink to="/projects">Kalender</NavigationLink>
      <NavigationLink to="/settings">Kartor</NavigationLink>
      <NavigationLink to="/documents">Dokument</NavigationLink>
      <NavigationLink to="/hunting_year">Jakt</NavigationLink>
    </div>
  );
};

export default NavbarCenter;
