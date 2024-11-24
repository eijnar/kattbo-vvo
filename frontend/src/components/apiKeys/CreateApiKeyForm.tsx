// src/components/apiKeys/CreateApiKeyForm.tsx

import React from 'react';
import PermissionsSelector from './PermissionsSelector';
import ExpirationInput from './ExpirationInput';
import Spinner from '../common/Spinner';

interface Permission {
  name: string;
  description: string;
}

interface CreateApiKeyFormProps {
  availablePermissions: Permission[];
  selectedPermissions: string[];
  onPermissionChange: (permission: string) => void;
  expiresIn: string;
  onExpiresInChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
  isSubmitDisabled: boolean;
}

const CreateApiKeyForm: React.FC<CreateApiKeyFormProps> = ({
  availablePermissions,
  selectedPermissions,
  onPermissionChange,
  expiresIn,
  onExpiresInChange,
  onSubmit,
  isLoading,
  isSubmitDisabled,
}) => {
  return (
    <>
      <h3 className="text-xl font-semibold mb-4">Create a New API Key</h3>
      <PermissionsSelector
        availablePermissions={availablePermissions}
        selectedPermissions={selectedPermissions}
        onChange={onPermissionChange}
      />
      <ExpirationInput expiresIn={expiresIn} onChange={onExpiresInChange} />
      <button
        onClick={onSubmit}
        className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded disabled:opacity-50 flex justify-center items-center"
        disabled={isLoading || isSubmitDisabled}
      >
        {isLoading ? <Spinner size="sm" color="text-white" /> : 'Create API Key'}
      </button>
    </>
  );
};

export default CreateApiKeyForm;
