import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "../auth/LoginButton";
import UserDropdown from "./UserDropdown";

const NavbarRight: React.FC = () => {
  const { isAuthenticated } = useAuth0();

  return <div className="flex-none">{isAuthenticated ? <UserDropdown /> : <LoginButton />}</div>;
};

export default NavbarRight;
