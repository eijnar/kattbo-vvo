export interface DropdownMenuProps {
    title: string;
    items: { name: string; href: string }[];
  }
  
  export interface User {
    name: string;
    email: string;
    imageUrl: string;
  }
  
  export interface ProfileMenuProps {
    user: User;
  }
  
  export interface NavItem {
    name: string;
    href: string;
    current: boolean;
    dropdown?: { name: string; href: string }[];
  }
  
  export interface NavLinksProps {
    navigation: NavItem[];
  }
  