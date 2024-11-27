// src/components/landing/LandingContent.tsx

import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import LoginButton from '../auth/LoginButton';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import { useContext } from 'react';
import TeamSelector from '../team/TeamSelector';
import CreateEventForm from '../event/EventCreate';

const LandingContent: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth0();
  const { userProfile } = useContext(AuthContext);


  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col px-4">
      <h1 className="text-4xl font-bold mb-4">Välkommen till Kättbo Viltvårdsområde</h1>
      <p className="text-lg mb-8">Ditt vilvårdsområde nära naturen</p>
      <p> <TeamSelector />
        </p>

      {isAuthenticated ? (
        <>
          {userProfile && (
            <div className="mb-4">
              <p className="text-gray-700">
                Hello, {userProfile.first_name || userProfile.email}!
              </p>
              <p> Skapa ett event: Skapa ett event:
              <CreateEventForm />
            </p>
            </div>
          )}
          <div className="mt-4">
            <Link
              to="/profile"
              className="text-blue-500 hover:underline text-md"
            >
              Go to Profile
            </Link>

           
          </div>
        </>
      ) : (
        <LoginButton />
      )}
    </div>
  );
};

export default LandingContent;
