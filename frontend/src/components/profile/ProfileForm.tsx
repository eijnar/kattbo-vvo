// src/components/profile/ProfileForm.tsx

import React, { useState, useEffect } from "react";
import { useProfile } from "../../hooks/useProfile";
import Spinner from "../common/Spinner";
import LoadingOverlay from "../common/LoadingOverlay";
import { Button } from "../catalyst/button";
import { Divider } from "../catalyst/divider";
import {
  Field,
  FieldGroup,
  Fieldset,
  Label,
} from "../catalyst/fieldset";
import { Input } from "../catalyst/input";
import { Subheading } from "../catalyst/heading";

const ProfileForm: React.FC = () => {
  const { userProfile, modifyUserProfile } = useProfile();
  // Removed globalLoading and setLoading
  const [updateData, setUpdateData] = useState({
    first_name: "",
    last_name: "",
    phone_number: "",
    email: "",
  });
  const [updateStatus, setUpdateStatus] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isFetching, setIsFetching] = useState<boolean>(true); // Local loading state for initial data fetch

  useEffect(() => {
    if (userProfile) {
      setUpdateData({
        first_name: userProfile.first_name ?? "",
        last_name: userProfile.last_name ?? "",
        phone_number: userProfile.phone_number ?? "",
        email: userProfile.email ?? "",
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
      setUpdateStatus("Profile updated successfully.");
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
    <div>
      {/* Wrap the specific div with LoadingOverlay */}
      <LoadingOverlay isLoading={isSubmitting}>
        {updateStatus && (
          <p
            className={`mb-4 ${
              updateStatus.startsWith("Failed")
                ? "text-red-500"
                : "text-green-500"
            }`}
          >
            {updateStatus}
          </p>
        )}

        <form onSubmit={handleFormSubmit}>
          <Fieldset>
            <FieldGroup>
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 sm:gap-4">
                <Field>
                  <Label>Förnamn</Label>
                  <Input
                    name="first_name"
                    value={updateData.first_name}
                    onChange={handleInputChange}
                    disabled={isSubmitting}
                  />
                </Field>
                <Field>
                  <Label>Efternamn</Label>
                  <Input
                    name="last_name"
                    value={updateData.last_name}
                    onChange={handleInputChange}
                    disabled={isSubmitting}
                  />
                </Field>
              </div>
              <Divider />
              <Subheading>Kommunikation</Subheading>
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-3 sm:gap-2">
                <Field>
                  <Label>E-post</Label>
                  <Input
                    name="email"
                    value={updateData.email}
                    onChange={handleInputChange}
                    disabled={isSubmitting}
                  />
                </Field>
                <Field>
                  <Label>Telefonnummer</Label>
                  <Input
                    name="phone_number"
                    value={updateData.phone_number}
                    onChange={handleInputChange}
                    disabled={isSubmitting}
                  />
                </Field>

                <Field>
                  <Label>Telegram</Label>
                  <Input
                    name="phone_number"
                    value={updateData.phone_number}
                    onChange={handleInputChange}
                    disabled={isSubmitting}
                  />
                </Field>
              </div>
            </FieldGroup>
            <div className="pt-8">
              <Button color="green" type="submit" disabled={isSubmitting}>
                {isSubmitting ? (
                  <Spinner size="sm" color="text-white" />
                ) : (
                  "Update Profile"
                )}
              </Button>
            </div>
          </Fieldset>
        </form>
      </LoadingOverlay>
    </div>
  );
};

export default ProfileForm;
