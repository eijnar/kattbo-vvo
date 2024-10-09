import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import Button from '../common/Button';

interface LogoutButtonProps {
  className?: string;
}

const LogoutButton: React.FC<LogoutButtonProps> = ({ className }) => {
  const { logout } = useAuth0();

  return (
    <Button onClick={() => logout({ logoutParams: { returnTo: window.location.origin}})} className={className}>
      Log Out
    </Button>
  );
};

export default LogoutButton;