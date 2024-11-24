// src/components/apiKeys/ApiKeyList.tsx

import React from 'react';
import ApiKeyItem from './ApiKeyItem';
import Spinner from '../common/Spinner';
import ErrorMessage from '../common/ErrorMessage';
import { ApiKey } from '../../types/ApiKey';

interface ApiKeyListProps {
  apiKeys: ApiKey[];
  onRevoke: (apiKeyId: string) => void;
  isLoading: boolean;
  error: string | null;
  revokingKeyId: string | null;
}

const ApiKeyList: React.FC<ApiKeyListProps> = ({
  apiKeys,
  onRevoke,
  isLoading,
  error,
  revokingKeyId,
}) => {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center">
        <Spinner size="md" color="text-blue-500" />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (apiKeys.length === 0) {
    return <div>No API keys found.</div>;
  }

  return (
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
          <ApiKeyItem
            key={key.id}
            apiKey={key}
            onRevoke={onRevoke}
            isRevoking={revokingKeyId === key.id}
          />
        ))}
      </tbody>
    </table>
  );
};

export default ApiKeyList;