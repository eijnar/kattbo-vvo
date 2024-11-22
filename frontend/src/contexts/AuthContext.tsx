import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { fetchUserProfile } from '../services/api/userService';
import { UserProfile } from '../types/User';
import config from '../config';

interface AuthContextProps {
  userProfile: UserProfile | null;
  refreshUserProfile: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextProps>({
  userProfile: null,
  refreshUserProfile: async () => {},
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);

  const refreshUserProfile = async () => {
    try {
      const token = await getAccessTokenSilently({
        authorizationParams: {
          audience: config.auth.audience,
        },
      });
      const profile = await fetchUserProfile(token);
      setUserProfile(profile);
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      setUserProfile(null);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      refreshUserProfile();
    } else {
      setUserProfile(null);
    }
  }, [isAuthenticated]);

  return (
    <AuthContext.Provider value={{ userProfile, refreshUserProfile }}>
      {children}
    </AuthContext.Provider>
  );
};
