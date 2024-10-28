// src/components/apiKeys/CreateApiKey.tsx

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth0';
import {
  createApiKey,
  fetchApiKeys,
  revokeApiKey,
} from '../../services/api/apiKeyService';
import Spinner from '../common/Spinner';
import ErrorMessage from '../common/ErrorMessage';
import { ApiKeyResponse, ApiKey } from '../../types/ApiKey';

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
  const [expires_in, setExpiration] = useState<string>('30d');
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [keysLoading, setKeysLoading] = useState<boolean>(false);

  const handlePermissionChange = (permission: string) => {
    setSelectedPermissions((prev) =>
      prev.includes(permission)
        ? prev.filter((perm) => perm !== permission)
        : [...prev, permission]
    );
  };

  const fetchAndSetApiKeys = async (token: string) => {
    setKeysLoading(true);
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
      }
    };

    initialize();
  }, [auth0_id, isAuthenticated, getAccessTokenSilently]);

  const handleCreateApiKey = async () => {
    if (selectedPermissions.length === 0) {
      setError('Please select at least one permission.');
      return;
    }
  
    if (!expires_in.match(/^\d+[d]$/)) {
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
        expires_in
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
    setKeysLoading(true);
    try {
      const token = await getAccessTokenSilently();
      await revokeApiKey(token, apiKeyId);
      // Remove the revoked API key from the state
      setApiKeys((prevKeys) => prevKeys.filter((key) => key.id !== apiKeyId));
    } catch (err: any) {
      console.error('Error revoking API key:', err);
      setError('Failed to revoke API key.');
    } finally {
      setKeysLoading(false);
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

      {apiKeys.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4">Your API Keys</h3>
          {keysLoading ? (
            <div className="flex justify-center items-center">
              <Spinner size="md" color="text-blue-500" />
            </div>
          ) : (
            <table className="min-w-full bg-white">
              <thead>
                <tr>
                  <th className="py-2 px-4 bg-gray-200 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="py-2 px-4 bg-gray-200 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Permissions
                  </th>
                  <th className="py-2 px-4 bg-gray-200 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Created At
                  </th>
                  <th className="py-2 px-4 bg-gray-200 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Expires At
                  </th>
                  <th className="py-2 px-4 bg-gray-200"></th>
                </tr>
              </thead>
              <tbody>
                {apiKeys.map((key) => (
                  <tr key={key.id} className="border-b hover:bg-gray-50">
                    <td className="py-2 px-4">{key.id}</td>
                    <td className="py-2 px-4">
                      {key.permissions.join(', ')}
                    </td>
                    <td className="py-2 px-4">
                      {new Date(key.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-2 px-4">
                      {key.expires_in
                        ? new Date(key.expires_in).toLocaleDateString()
                        : 'Never'}
                    </td>
                    <td className="py-2 px-4">
                      <button
                        onClick={() => handleRevokeApiKey(key.id)}
                        className="bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-2 rounded"
                      >
                        Revoke
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {apiKey ? (
        <div className="p-4 bg-green-100 text-green-800 rounded">
          <p>Your API Key:</p>
          <div className="mt-2 flex items-center">
            <code className="flex-1 p-2 bg-gray-200 rounded">{apiKey}</code>
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
        <>
          <h3 className="text-xl font-semibold mb-4">Create a New API Key</h3>
          <div className="mb-4">
            <p className="mb-2">Select Permissions:</p>
            <div className="mb-4">
              <h4 className="font-semibold">Users:</h4>
              {availablePermissions
                .filter((perm) => perm.name.startsWith('users:'))
                .map((permission) => (
                  <label key={permission.name} className="flex items-center mb-2">
                    <input
                      type="checkbox"
                      className="form-checkbox h-5 w-5 text-blue-600"
                      checked={selectedPermissions.includes(permission.name)}
                      onChange={() => handlePermissionChange(permission.name)}
                    />
                    <span className="ml-2">
                      <strong>{permission.name}</strong>: {permission.description}
                    </span>
                  </label>
                ))}
            </div>
            <div className="mb-4">
              <h4 className="font-semibold">Orders:</h4>
              {availablePermissions
                .filter((perm) => perm.name.startsWith('orders:'))
                .map((permission) => (
                  <label key={permission.name} className="flex items-center mb-2">
                    <input
                      type="checkbox"
                      className="form-checkbox h-5 w-5 text-blue-600"
                      checked={selectedPermissions.includes(permission.name)}
                      onChange={() => handlePermissionChange(permission.name)}
                    />
                    <span className="ml-2">
                      <strong>{permission.name}</strong>: {permission.description}
                    </span>
                  </label>
                ))}
            </div>
            {/* Add more categories as needed */}
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Expiration (e.g., "30d" for 30 days):
            </label>
            <input
              type="text"
              value={expires_in}
              onChange={(e) => setExpiration(e.target.value)}
              className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="30d"
            />
          </div>
          <button
            onClick={handleCreateApiKey}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded disabled:opacity-50"
            disabled={isLoading || selectedPermissions.length === 0}
          >
            {isLoading ? <Spinner size="sm" color="text-white" /> : 'Create API Key'}
          </button>
        </>
      )}
    </div>
  );
};

export default CreateApiKey;
