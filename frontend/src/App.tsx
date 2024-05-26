import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import config from './auth_config.json';

const App: React.FC = () => {
  const { loginWithRedirect, logout, isAuthenticated } = useAuth0();

  const handleRegister = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'signup',
        audience: config.audience
      }
    });
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      {!isAuthenticated ? (
        <div>
          <button onClick={() => loginWithRedirect()}>Log in</button>
          <button onClick={handleRegister}>Register</button>
        </div>
      ) : (
        <>
          <h2>You are logged in!</h2>
        <button onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>Log out</button>
        </>
      )}
    </div>
  );
};

export default App;
