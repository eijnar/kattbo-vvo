import React from 'react';
import ProfileForm from '../components/profile/ProfileForm';
import LogoutButton from '../components/auth/LogoutButton';

const ProfilePage: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Your Profile</h2>
      <ProfileForm />
      <LogoutButton />
    </div>
  );
};

export default ProfilePage;
