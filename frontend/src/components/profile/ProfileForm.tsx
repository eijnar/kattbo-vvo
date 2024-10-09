// src/components/profile/ProfileForm.tsx

import React, { useState, useEffect } from 'react';
import { useProfile } from '../../hooks/useProfile';
import Spinner from '../common/Spinner';
import LoadingOverlay from '../common/LoadingOverlay';
import Input from '../common/Input';
import Button from '../common/Button';
import useLoading from '../../hooks/useLoading';

const ProfileForm: React.FC = () => {
  const { userProfile, modifyUserProfile } = useProfile();
  const { isLoading: globalLoading, setLoading } = useLoading();
  const [updateData, setUpdateData] = useState({
    first_name: '',
    last_name: '',
    phone_number: '',
  });
  const [updateStatus, setUpdateStatus] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  useEffect(() => {
    if (userProfile) {
      setUpdateData({
        first_name: userProfile.first_name ?? '',
        last_name: userProfile.last_name ?? '',
        phone_number: userProfile.phone_number ?? '',
      });
    }
  }, [userProfile]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUpdateData({
      ...updateData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setUpdateStatus(null);
    setIsSubmitting(true);
    setLoading(true); // Start global loading

    try {
      await modifyUserProfile(updateData);
      setUpdateStatus('Profile updated successfully.');
    } catch (error: any) {
      console.error(error);
      setUpdateStatus(`Failed to update profile: ${error.message}`);
    } finally {
      setIsSubmitting(false);
      setLoading(false); // Stop global loading
    }
  };

  if (globalLoading && !isSubmitting) {
    // Optionally, you can show a separate overlay for initial data fetching
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }

  return (
    <>
      <LoadingOverlay isLoading={isSubmitting || globalLoading} />
      <div className="max-w-md mx-auto mt-8 p-6 bg- shadow-md rounded">
        <h3 className="text-2xl mb-4">Update Your Profile</h3>
        {updateStatus && (
          <p
            className={`mb-4 ${
              updateStatus.startsWith('Failed') ? 'text-red-500' : 'text-green-500'
            }`}
          >
            {updateStatus}
          </p>
        )}
        <form onSubmit={handleFormSubmit}>
          <Input
            label="First Name:"
            name="first_name"
            value={updateData.first_name}
            onChange={handleInputChange}
            disabled={isSubmitting || globalLoading}
          />
          <Input
            label="Last Name:"
            name="last_name"
            value={updateData.last_name}
            onChange={handleInputChange}
            disabled={isSubmitting || globalLoading}
          />
          <Input
            label="Phone Number:"
            name="phone_number"
            value={updateData.phone_number}
            onChange={handleInputChange}
            disabled={isSubmitting || globalLoading}
          />
          <Button type="submit" disabled={isSubmitting || globalLoading} className="w-full">
            {isSubmitting ? <Spinner size="sm" color="text-white" /> : 'Update Profile'}
          </Button>
        </form>
      </div>
    </>
  );
};

export default ProfileForm;