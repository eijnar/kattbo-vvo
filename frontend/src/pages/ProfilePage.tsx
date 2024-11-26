import React from 'react';
import ProfileForm from '../components/profile/ProfileForm';
import { Subheading, Heading } from '../components/catalyst/heading';
import { Divider } from '../components/catalyst/divider';
import { Text } from '../components/catalyst/text';

const ProfilePage: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <Heading>Profilinställningar</Heading>
      <Subheading className='pt-8'>Användarinformation</Subheading>
            <Text>
              Håll dessa inställningar uppdaterade så vi kan nå dig med den
              informationen du önskar.
            </Text>
      <Divider soft className='my-5' />
      <ProfileForm />
    </div>
  );
};

export default ProfilePage;
