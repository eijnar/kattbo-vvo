import React from 'react';
import LoginButton from '../components/auth/LoginButton';

const LoginPage: React.FC = () => {
  return (
    <div style={{ textAlign: 'center', padding: '50px' }}>
      <h2>Login</h2>
      <LoginButton />
    </div>
  );
};

export default LoginPage;
