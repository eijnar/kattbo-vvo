import { useAuth0 } from '@auth0/auth0-react';

interface Auth {
  user: any; 
  isAuthenticated: boolean;
  isLoading: boolean;
  auth0_id: string | undefined;
  getAccessTokenSilently: () => Promise<string>;
}

export const useAuth = (): Auth => {
  const { user, isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();

  const auth0_id = user?.sub;

  return {
    user,
    isAuthenticated,
    isLoading,
    auth0_id,
    getAccessTokenSilently,
  };
};
