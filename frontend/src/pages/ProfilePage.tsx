import React from 'react';
import ProfileForm from '../components/profile/ProfileForm';

const ProfilePage: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Your Profile</h2>
      <ProfileForm />
    </div>
  );
};

export default ProfilePage;
