// src/components/landing/LandingContent.tsx

import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import LoginButton from '../auth/LoginButton';
import LogoutButton from '../auth/LogoutButton';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import { useContext } from 'react';

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
    <div className="flex flex-col items-center justify-center h-screen text-center px-4 bg-lime-200">
      <h1 className="text-4xl font-bold mb-4">Welcome to Kattbo VVO</h1>
      <p className="text-lg mb-8">Your platform for managing profiles securely.</p>

      {isAuthenticated ? (
        <>
          {userProfile && (
            <div className="mb-4">
              <p className="text-gray-700">
                Hello, {userProfile.first_name || userProfile.email}!
              </p>
            </div>
          )}
          <LogoutButton />
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
