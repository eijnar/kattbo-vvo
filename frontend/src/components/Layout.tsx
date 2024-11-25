import React from "react";
import { Outlet } from "react-router-dom";
import { SidebarLayout } from "./catalyst/sidebar-layout";
import { Avatar } from "./catalyst/avatar";
import {
  Dropdown,
  DropdownButton,
  DropdownDivider,
  DropdownItem,
  DropdownLabel,
  DropdownMenu,
} from "./catalyst/dropdown";
import {
  Navbar,
  NavbarItem,
  NavbarSection,
  NavbarSpacer,
} from "./catalyst/navbar";
import {
  Sidebar,
  SidebarBody,
  SidebarFooter,
  SidebarHeader,
  SidebarHeading,
  SidebarItem,
  SidebarLabel,
  SidebarSection,
  SidebarSpacer,
} from "./catalyst/sidebar";
import {
  ArrowRightStartOnRectangleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  Cog8ToothIcon,
  LightBulbIcon,
  PlusIcon,
  ShieldCheckIcon,
  UserIcon,
} from "@heroicons/react/16/solid";
import {
  Cog6ToothIcon,
  HomeIcon,
  InboxIcon,
  MagnifyingGlassIcon,
  MegaphoneIcon,
  QuestionMarkCircleIcon,
  SparklesIcon,
  Square2StackIcon,
  TicketIcon,
} from "@heroicons/react/20/solid";
import { Link } from "react-router-dom";

const Layout: React.FC = () => {
  return (
    <SidebarLayout
      navbar={
        <Navbar>
          <NavbarSpacer />
          <NavbarSection>
            <NavbarItem as={Link} to="/search" aria-label="Search">
              <MagnifyingGlassIcon className="h-5 w-5" />
            </NavbarItem>
            <NavbarItem as={Link} to="/inbox" aria-label="Inbox">
              <InboxIcon className="h-5 w-5" />
            </NavbarItem>
            <Dropdown>
              <DropdownButton as={NavbarItem} as={Link} to="#">
                <Avatar src="/profile-photo.jpg" square />
              </DropdownButton>
              <DropdownMenu className="min-w-64" anchor="bottom end">
                <DropdownItem as={Link} to="/my-profile">
                  <UserIcon className="h-5 w-5" />
                  <DropdownLabel>My profile</DropdownLabel>
                </DropdownItem>
                <DropdownItem as={Link} to="/settings">
                  <Cog8ToothIcon className="h-5 w-5" />
                  <DropdownLabel>Settings</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem as={Link} to="/privacy-policy">
                  <ShieldCheckIcon className="h-5 w-5" />
                  <DropdownLabel>Privacy policy</DropdownLabel>
                </DropdownItem>
                <DropdownItem as={Link} to="/share-feedback">
                  <LightBulbIcon className="h-5 w-5" />
                  <DropdownLabel>Share feedback</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem as={Link} to="/logout">
                  <ArrowRightStartOnRectangleIcon className="h-5 w-5" />
                  <DropdownLabel>Sign out</DropdownLabel>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </NavbarSection>
        </Navbar>
      }
      sidebar={
        <Sidebar>
          <SidebarHeader>
            <Dropdown>
              <DropdownButton
                as={SidebarItem}
                className="lg:mb-2.5"
              >
                <Avatar src="/public/logo.svg" />
                <SidebarLabel>Kättbo VVO</SidebarLabel>
                <ChevronDownIcon className="h-5 w-5" />
              </DropdownButton>
              <DropdownMenu
                className="min-w-80 lg:min-w-64"
                anchor="bottom start"
              >
                <DropdownItem as={Link} to="/teams/1/settings">
                  <Cog8ToothIcon className="h-5 w-5" />
                  <DropdownLabel>Settings</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem as={Link} to="/teams/1">
                  <Avatar src="/tailwind-logo.svg" />
                  <DropdownLabel>Tailwind Labs</DropdownLabel>
                </DropdownItem>
                <DropdownItem as={Link} to="/teams/2">
                  <Avatar initials="WC" className="bg-purple-500 text-white" />
                  <DropdownLabel>Workcation</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem as={Link} to="/teams/create">
                  <PlusIcon className="h-5 w-5" />
                  <DropdownLabel>New team&hellip;</DropdownLabel>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
            <SidebarSection className="max-lg:hidden">
              <SidebarItem as={Link} to="/search">
                <MagnifyingGlassIcon className="h-5 w-5" />
                <SidebarLabel>Search</SidebarLabel>
              </SidebarItem>
              <SidebarItem as={Link} to="/inbox">
                <InboxIcon className="h-5 w-5" />
                <SidebarLabel>Inbox</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
          </SidebarHeader>
          <SidebarBody>
            <SidebarSection>
              <SidebarItem as={Link} to="/">
                <HomeIcon className="h-5 w-5" />
                <SidebarLabel>Home</SidebarLabel>
              </SidebarItem>
              <SidebarItem as={Link} to="/events">
                <Square2StackIcon className="h-5 w-5" />
                <SidebarLabel>Events</SidebarLabel>
              </SidebarItem>
              <SidebarItem as={Link} to="/orders">
                <TicketIcon className="h-5 w-5" />
                <SidebarLabel>Orders</SidebarLabel>
              </SidebarItem>
              <SidebarItem as={Link} to="/settings">
                <Cog6ToothIcon className="h-5 w-5" />
                <SidebarLabel>Settings</SidebarLabel>
              </SidebarItem>
              <SidebarItem as={Link} to="/broadcasts">
                <MegaphoneIcon className="h-5 w-5" />
                <SidebarLabel>Broadcasts</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
            <SidebarSection className="max-lg:hidden">
              <SidebarHeading>Upcoming Events</SidebarHeading>
              <SidebarItem as={Link} to="/events/1">
                Bear Hug: Live in Concert
              </SidebarItem>
              <SidebarItem as={Link} to="/events/2">
                Viking People
              </SidebarItem>
              <SidebarItem as={Link} to="/events/3">
                Six Fingers — DJ Set
              </SidebarItem>
              <SidebarItem as={Link} to="/events/4">
                We All Look The Same
              </SidebarItem>
            </SidebarSection>
            <SidebarSpacer />
            <SidebarSection>
              <SidebarItem as={Link} to="/support">
                <QuestionMarkCircleIcon className="h-5 w-5" />
                <SidebarLabel>Support</SidebarLabel>
              </SidebarItem>
              <SidebarItem as={Link} to="/changelog">
                <SparklesIcon className="h-5 w-5" />
                <SidebarLabel>Changelog</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
          </SidebarBody>
          <SidebarFooter className="max-lg:hidden">
            <Dropdown>
              <DropdownButton as={SidebarItem} as={Link} to="#">
                <span className="flex min-w-0 items-center gap-3">
                  <Avatar
                    src="/images/landing_page_bg.jpg"
                    className="size-10"
                    square
                    alt=""
                  />
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium text-zinc-950 dark:text-white">
                      Erica
                    </span>
                    <span className="block truncate text-xs font-normal text-zinc-500 dark:text-zinc-400">
                      erica@example.com
                    </span>
                  </span>
                </span>
                <ChevronUpIcon className="h-5 w-5" />
              </DropdownButton>
              <DropdownMenu className="min-w-64" anchor="top start">
                <DropdownItem as={Link} to="/my-profile">
                  <UserIcon className="h-5 w-5" />
                  <DropdownLabel>My profile</DropdownLabel>
                </DropdownItem>
                <DropdownItem as={Link} to="/settings">
                  <Cog8ToothIcon className="h-5 w-5" />
                  <DropdownLabel>Settings</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem as={Link} to="/privacy-policy">
                  <ShieldCheckIcon className="h-5 w-5" />
                  <DropdownLabel>Privacy policy</DropdownLabel>
                </DropdownItem>
                <DropdownItem as={Link} to="/share-feedback">
                  <LightBulbIcon className="h-5 w-5" />
                  <DropdownLabel>Share feedback</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem as={Link} to="/logout">
                  <ArrowRightStartOnRectangleIcon className="h-5 w-5" />
                  <DropdownLabel>Sign out</DropdownLabel>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </SidebarFooter>
        </Sidebar>
      }
    >
      <Outlet />
    </SidebarLayout>
  );
};

export default Layout;
