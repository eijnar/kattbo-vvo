import React from 'react';
import ListUsers from '../components/users/ListUsers';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  return (
    <div>
      <ListUsers />
      <Link
      to="/create-api-key">Create api key</Link>
    </div>
  );
};

export default LandingPage;
