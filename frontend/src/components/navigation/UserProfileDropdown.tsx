import { useAuth0 } from "@auth0/auth0-react";
import React, { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import Spinner from "../common/Spinner";
import { SidebarItem } from "../catalyst/sidebar";
import { Avatar } from "../catalyst/avatar";
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
  DropdownItem,
  DropdownLabel,
  DropdownMenu,
} from "../catalyst/dropdown";
import {
  ArrowRightStartOnRectangleIcon,
  ChevronUpIcon,
  Cog8ToothIcon,
  LightBulbIcon,
  UserIcon,
  KeyIcon
} from "@heroicons/react/16/solid";
import LoginButton from "../auth/LoginButton";

const UserProfileDropdown: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth0();
  const { userProfile } = useContext(AuthContext);

  if (!isAuthenticated || !userProfile) {
    return <LoginButton />;
  }
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }
  return (
    <Dropdown>
      <DropdownButton as={SidebarItem}>
        <span className="flex min-w-0 items-center gap-3">
          <Avatar
            src="/images/landing_page_bg.jpg"
            className="size-10"
            square
            alt=""
          />
          <span className="min-w-0">
            <span className="block truncate text-sm font-medium text-zinc-950 dark:text-white">
              {userProfile.first_name}
            </span>
            <span className="block truncate text-xs font-normal text-zinc-500 dark:text-zinc-400">
              {userProfile.email}
            </span>
          </span>
        </span>
        <ChevronUpIcon className="h-5 w-5" />
      </DropdownButton>
      <DropdownMenu className="min-w-64" anchor="top start">
        <DropdownItem href="/profile">
          <UserIcon className="h-5 w-5" />
          <DropdownLabel>Min profil</DropdownLabel>
        </DropdownItem>
        <DropdownItem href="/settings">
          <Cog8ToothIcon className="h-5 w-5" />
          <DropdownLabel>Inställningar</DropdownLabel>
        </DropdownItem>
        <DropdownDivider />
        <DropdownItem href="/api-keys">
          <KeyIcon className="h-5 w-5" />
          <DropdownLabel>Hantera API nycklar</DropdownLabel>
        </DropdownItem>
        <DropdownItem href="/share-feedback">
          <LightBulbIcon className="h-5 w-5" />
          <DropdownLabel>Skicka feedback</DropdownLabel>
        </DropdownItem>
        <DropdownDivider />
        <DropdownItem href="/logout">
          <ArrowRightStartOnRectangleIcon className="h-5 w-5" />
          <DropdownLabel>Logga ut</DropdownLabel>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};

export default UserProfileDropdown;
