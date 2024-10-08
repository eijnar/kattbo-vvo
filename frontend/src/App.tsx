import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import config from './auth_config.json';

const App: React.FC = () => {
  const {
    loginWithRedirect,
    logout,
    isAuthenticated,
    getAccessTokenSilently,
    isLoading,
    error,
  } = useAuth0();

  const [userData, setUserData] = useState<any>(null);

  // Function to fetch user data from the backend
  const fetchUserData = async () => {
    try {
      // Get the access token from Auth0
      const accessToken = await getAccessTokenSilently({
        authorizationParams: {
          audience: config.audience,
        },
      });

      // Make a request to your backend API
      const response = await fetch('http://localhost:8000/v1/users/current', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Error fetching user data: ${response.statusText}`);
      }

      const data = await response.json();
      setUserData(data);
    } catch (err) {
      console.error(err);
    }
  };

  // useEffect to fetch user data when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchUserData();
    } else {
      setUserData(null);
    }
  }, [isAuthenticated]);

  const handleRegister = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'signup',
        audience: config.audience,
      },
    });
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Authentication Error: {error.message}</div>;
  }

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column', // Changed to column to stack elements vertically
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      {!isAuthenticated ? (
        <div>
          <button onClick={() => loginWithRedirect()}>Log in</button>
          <button onClick={handleRegister}>Register</button>
        </div>
      ) : (
        <>
          <h2>You are logged in!</h2>
          {userData ? (
            <div>
              <h3>User Data from Backend:</h3>
              <pre>{JSON.stringify(userData, null, 2)}</pre>
            </div>
          ) : (
            <p>Loading user data...</p>
          )}
          <button
            onClick={() =>
              logout({ logoutParams: { returnTo: window.location.origin } })
            }
          >
            Log out
          </button>
        </>
      )}
    </div>
  );
};

export default App;