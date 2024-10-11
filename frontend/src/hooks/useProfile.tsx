import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { updateUserProfile } from '../services/api/userService';
import { UserProfile } from '../types/User';
import { useAuth0 } from '@auth0/auth0-react';
import config from '../auth_config.json'

export const useProfile = () => {
  const { userProfile, refreshUserProfile } = useContext(AuthContext);
  const { getAccessTokenSilently } = useAuth0(); 

  const modifyUserProfile = async (data: Partial<UserProfile>): Promise<UserProfile> => {
    if (!userProfile) throw new Error('User not authenticated');
    try {
      const token = await getAccessTokenSilently({
        authorizationParams: {
          audience: config.audience, // Replace with your Auth0 audience
        },
      });
      const updatedUser = await updateUserProfile(token, data);
      await refreshUserProfile();
      return updatedUser;
    } catch (error) {
      console.error('Error in modifyUserProfile:', error);
      throw error;
    }
  };

  return {
    userProfile,
    modifyUserProfile,
  };
};
