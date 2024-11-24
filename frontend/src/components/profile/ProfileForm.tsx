// src/components/profile/ProfileForm.tsx

import React, { useState, useEffect } from 'react';
import { useProfile } from '../../hooks/useProfile';
import Spinner from '../common/Spinner';
import LoadingOverlay from '../common/LoadingOverlay';
import Input from '../common/Input';
import Button from '../common/Button';
// Removed useLoading since we'll manage loading locally

const ProfileForm: React.FC = () => {
  const { userProfile, modifyUserProfile } = useProfile();
  // Removed globalLoading and setLoading
  const [updateData, setUpdateData] = useState({
    first_name: '',
    last_name: '',
    phone_number: '',
  });
  const [updateStatus, setUpdateStatus] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isFetching, setIsFetching] = useState<boolean>(true); // Local loading state for initial data fetch

  useEffect(() => {
    if (userProfile) {
      setUpdateData({
        first_name: userProfile.first_name ?? '',
        last_name: userProfile.last_name ?? '',
        phone_number: userProfile.phone_number ?? '',
      });
      setIsFetching(false); // Data has been fetched
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

    try {
      await modifyUserProfile(updateData);
      setUpdateStatus('Profile updated successfully.');
    } catch (error: any) {
      console.error(error);
      setUpdateStatus(`Failed to update profile: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Optionally, show a full-screen spinner during the initial data fetch
  if (isFetching) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white shadow-md rounded relative">
      {/* Wrap the specific div with LoadingOverlay */}
      <LoadingOverlay isLoading={isSubmitting}>
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
            disabled={isSubmitting}
          />
          <Input
            label="Last Name:"
            name="last_name"
            value={updateData.last_name}
            onChange={handleInputChange}
            disabled={isSubmitting}
          />
          <Input
            label="Phone Number:"
            name="phone_number"
            value={updateData.phone_number}
            onChange={handleInputChange}
            disabled={isSubmitting}
          />
          <Button type="submit" disabled={isSubmitting} className="w-full">
            {isSubmitting ? <Spinner size="sm" color="text-white" /> : 'Update Profile'}
          </Button>
        </form>
      </LoadingOverlay>
    </div>
  );
};

export default ProfileForm;
