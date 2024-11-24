// src/components/apiKeys/CreateApiKey.tsx

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth0';
import {
  createApiKey,
  fetchApiKeys,
  revokeApiKey,
} from '../../services/api/apiKeyService';
import Spinner from '../common/Spinner';
import LoadingOverlay from '../common/LoadingOverlay';
import ErrorMessage from '../common/ErrorMessage';
import { ApiKeyResponse, ApiKey } from '../../types/ApiKey';
import ApiKeyList from './ApiKeyList';
import CreateApiKeyForm from './CreateApiKeyForm';

interface Permission {
  name: string;
  description: string;
}

const availablePermissions: Permission[] = [
  // Users permissions
  { name: 'users:read', description: 'Read user data' },
  { name: 'users:write', description: 'Modify user data' },
  { name: 'users:delete', description: 'Delete user data' },
  // Orders permissions
  { name: 'orders:read', description: 'Read order data' },
  { name: 'orders:write', description: 'Modify order data' },
  { name: 'orders:delete', description: 'Delete order data' },
  // Add more permissions as needed
];

const CreateApiKey: React.FC = () => {
  const {
    auth0_id,
    isAuthenticated,
    isLoading: authLoading,
    getAccessTokenSilently,
  } = useAuth();
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [copySuccess, setCopySuccess] = useState<string | null>(null);
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);
  const [expiresIn, setExpiresIn] = useState<string>('30d');
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [keysLoading, setKeysLoading] = useState<boolean>(false);
  const [revokingKeyId, setRevokingKeyId] = useState<string | null>(null);

  const handlePermissionChange = (permission: string) => {
    setSelectedPermissions((prev) =>
      prev.includes(permission)
        ? prev.filter((perm) => perm !== permission)
        : [...prev, permission]
    );
  };

  const fetchAndSetApiKeys = async (token: string) => {
    setKeysLoading(true);
    setError(null);
    try {
      const keys = await fetchApiKeys(token);
      setApiKeys(keys);
    } catch (err: any) {
      console.error('Error fetching API keys:', err);
      setError('Failed to fetch API keys.');
    } finally {
      setKeysLoading(false);
    }
  };

  useEffect(() => {
    const initialize = async () => {
      if (!auth0_id || !isAuthenticated) return;
      try {
        const token = await getAccessTokenSilently();
        await fetchAndSetApiKeys(token);
      } catch (err) {
        console.error('Error initializing API keys:', err);
        setError('Failed to initialize API keys.');
      }
    };

    initialize();
  }, [auth0_id, isAuthenticated, getAccessTokenSilently]);

  const handleCreateApiKey = async () => {
    if (selectedPermissions.length === 0) {
      setError('Please select at least one permission.');
      return;
    }

    if (!/^\d+d$/.test(expiresIn)) {
      setError('Invalid expiration format. Use format like "30d".');
      return;
    }

    setIsLoading(true);
    setError(null);
    setApiKey(null);
    setCopySuccess(null);

    try {
      const token = await getAccessTokenSilently();
      console.log('Access Token:', token);

      const response: ApiKeyResponse = await createApiKey(
        token,
        selectedPermissions,
        expiresIn
      );
      setApiKey(response.api_key);
      // Refresh the API keys list
      await fetchAndSetApiKeys(token);
    } catch (err: any) {
      console.error('Error creating API key:', err);
      setError(err.response?.data?.message || 'Failed to create API key.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    if (apiKey) {
      navigator.clipboard.writeText(apiKey);
      setCopySuccess('Copied to clipboard!');
      setTimeout(() => setCopySuccess(null), 2000);
    }
  };

  const handleRevokeApiKey = async (apiKeyId: string) => {
    setRevokingKeyId(apiKeyId);
    setError(null);
    try {
      const token = await getAccessTokenSilently();
      await revokeApiKey(token, apiKeyId);
      setApiKeys((prevKeys) => prevKeys.filter((key) => key.id !== apiKeyId));
    } catch (err: any) {
      console.error('Error revoking API key:', err);
      setError('Failed to revoke API key.');
    } finally {
      setRevokingKeyId(null);
    }
  };

  if (authLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <div className="text-center mt-8">Please log in to manage API keys.</div>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-8 p-4 bg-white shadow-md rounded">
      <h2 className="text-2xl font-semibold mb-4">Manage API Keys</h2>
      {error && <ErrorMessage message={error} />}

      <div className="mb-8">
        <h3 className="text-xl font-semibold mb-4">Your API Keys</h3>
        <ApiKeyList
          apiKeys={apiKeys}
          onRevoke={handleRevokeApiKey}
          isLoading={keysLoading}
          error={error}
          revokingKeyId={revokingKeyId}
        />
      </div>

      {apiKey ? (
        <div className="p-4 bg-green-100 text-green-800 rounded">
          <p>Your API Key:</p>
          <div className="mt-2 flex items-center">
            <code className="flex-1 p-2 bg-gray-200 rounded break-all">{apiKey}</code>
            <button
              onClick={handleCopy}
              className="ml-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-1 px-2 rounded"
            >
              Copy
            </button>
          </div>
          {copySuccess && (
            <p className="mt-2 text-sm text-green-700">{copySuccess}</p>
          )}
          <p className="mt-2 text-sm text-gray-600">
            Please store it securely. You won't be able to view it again.
          </p>
        </div>
      ) : (
        <LoadingOverlay isLoading={isLoading}>
          <CreateApiKeyForm
            availablePermissions={availablePermissions}
            selectedPermissions={selectedPermissions}
            onPermissionChange={handlePermissionChange}
            expiresIn={expiresIn}
            onExpiresInChange={setExpiresIn}
            onSubmit={handleCreateApiKey}
            isLoading={isLoading}
            isSubmitDisabled={selectedPermissions.length === 0}
          />
        </LoadingOverlay>
      )}
    </div>
  );
};

export default CreateApiKey;