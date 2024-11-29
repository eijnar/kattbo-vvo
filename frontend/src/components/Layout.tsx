import React from "react";
import { Outlet, useLocation } from "react-router-dom";
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
  CalendarDaysIcon,
  ChevronDownIcon,
  Cog8ToothIcon,
  DocumentIcon,
  PlusIcon,
} from "@heroicons/react/16/solid";
import {
  Cog6ToothIcon,
  HomeIcon,
  InboxIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
  SparklesIcon,
  TicketIcon,
  MapIcon,
} from "@heroicons/react/20/solid";
import UserProfileDropdown from "./navigation/UserProfileDropdown";
import { Heading } from "./catalyst/heading";
import { Badge } from "./catalyst/badge";

const Layout: React.FC = () => {
  const location = useLocation();
  const isMapFullscreen =
    location.pathname === "/map" || location.pathname.startsWith("/map/");

  return (
    <SidebarLayout
      isMapFullScreen={isMapFullscreen}
      navbar={
        <Navbar>
          <NavbarSpacer />
          <NavbarSection>
            <NavbarItem href="/search" aria-label="Search">
              <MagnifyingGlassIcon className="h-5 w-5" />
            </NavbarItem>
            <NavbarItem href="/inbox" aria-label="Inbox">
              <InboxIcon className="h-5 w-5" />
            </NavbarItem>
            <UserProfileDropdown />
          </NavbarSection>
        </Navbar>
      }
      sidebar={
        <Sidebar>
          <SidebarHeader>
            <Heading>Kättbo VVO</Heading>
          </SidebarHeader>
          <SidebarBody>
            <Dropdown>
              <DropdownButton as={SidebarItem} className="lg:mb-2.5">
                <Avatar square src="/images/logo.webp" />
                <SidebarLabel>Hemmalaget</SidebarLabel>
                <ChevronDownIcon className="h-5 w-5" />
              </DropdownButton>
              <DropdownMenu
                className="min-w-80 lg:min-w-64"
                anchor="bottom start"
              >
                <DropdownItem href="/teams/1/settings">
                  <Cog8ToothIcon className="h-5 w-5" />
                  <DropdownLabel>Settings</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem href="/teams/1">
                  <Avatar src="/tailwind-logo.svg" />
                  <DropdownLabel>Tailwind Labs</DropdownLabel>
                </DropdownItem>
                <DropdownItem href="/teams/2">
                  <Avatar initials="WC" className="bg-purple-500 text-white" />
                  <DropdownLabel>Workcation</DropdownLabel>
                </DropdownItem>
                <DropdownDivider />
                <DropdownItem href="/teams/create">
                  <PlusIcon className="h-5 w-5" />
                  <DropdownLabel>New team&hellip;</DropdownLabel>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>

            <SidebarSection>
              <SidebarItem href="/">
                <HomeIcon className="h-5 w-5" />
                <SidebarLabel>Hem</SidebarLabel>
              </SidebarItem>
              <SidebarItem href="/event">
                <CalendarDaysIcon className="h-5 w-5" />
                <SidebarLabel>Händelser</SidebarLabel>
              </SidebarItem>
              <SidebarItem href="/hunting_team">
                <TicketIcon className="h-5 w-5" />
                <SidebarLabel>Jakt</SidebarLabel>
              </SidebarItem>
              <SidebarItem href="/map">
                <MapIcon className="h-5 w-5" />
                <SidebarLabel>Karta</SidebarLabel>
              </SidebarItem>
              <SidebarItem href="/map">
                <DocumentIcon className="h-5 w-5" />
                <SidebarLabel>Dokument</SidebarLabel>
              </SidebarItem>
              <SidebarItem href="/settings">
                <Cog6ToothIcon className="h-5 w-5" />
                <SidebarLabel>Inställningar</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
            <SidebarSection className="max-lg:hidden">
              <SidebarHeading>Kommande händelser</SidebarHeading>
              <SidebarItem href="/events/1">
                10 nov.
                <Badge color="red">Älgjakt</Badge>
              </SidebarItem>
              <SidebarItem href="/events/2">11/11: Småvilt, hare</SidebarItem>
              <SidebarItem href="/events/3">13/11: Älgjakt</SidebarItem>
              <SidebarItem href="/events/4">We All Look The Same</SidebarItem>
            </SidebarSection>
            <SidebarSpacer />
            <SidebarSection>
              <SidebarItem href="/support">
                <QuestionMarkCircleIcon className="h-5 w-5" />
                <SidebarLabel>Support</SidebarLabel>
              </SidebarItem>
              <SidebarItem href="/changelog">
                <SparklesIcon className="h-5 w-5" />
                <SidebarLabel>Changelog</SidebarLabel>
              </SidebarItem>
            </SidebarSection>
          </SidebarBody>
          <SidebarFooter className="max-lg:hidden">
            <UserProfileDropdown />
          </SidebarFooter>
        </Sidebar>
      }
    >
      <Outlet />
    </SidebarLayout>
  );
};

export default Layout;
