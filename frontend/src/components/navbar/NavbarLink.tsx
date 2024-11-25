// src/components/NavLink.tsx
import { Link, LinkProps } from 'react-router-dom';

interface NavLinkProps extends LinkProps {
  children: React.ReactNode;
  className?: string;
}

export const NavLink: React.FC<NavLinkProps> = ({ children, className, ...props }) => {
  return (
    <Link {...props} className={className}>
      {children}
    </Link>
  );
};