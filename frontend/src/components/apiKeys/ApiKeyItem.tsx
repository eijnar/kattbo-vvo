// src/components/apiKeys/ApiKeyItem.tsx

import React from 'react';
import Spinner from '../common/Spinner';
import { ApiKey } from '../../types/ApiKey';

interface ApiKeyItemProps {
  apiKey: ApiKey;
  onRevoke: (apiKeyId: string) => void;
  isRevoking: boolean;
}

const ApiKeyItem: React.FC<ApiKeyItemProps> = ({ apiKey, onRevoke, isRevoking }) => {
  return (
    <tr className="border-b hover:bg-gray-50">
      <td className="py-2 px-4">{apiKey.id}</td>
      <td className="py-2 px-4">{apiKey.permissions.join(', ')}</td>
      <td className="py-2 px-4">
        {new Date(apiKey.created_at).toLocaleDateString()}
      </td>
      <td className="py-2 px-4">
        {apiKey.expires_in
          ? new Date(apiKey.expires_in).toLocaleDateString()
          : 'Never'}
      </td>
      <td className="py-2 px-4">
        <button
          onClick={() => onRevoke(apiKey.id)}
          className="bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-2 rounded"
          disabled={isRevoking}
        >
          {isRevoking ? <Spinner size="sm" color="text-white" /> : 'Revoke'}
        </button>
      </td>
    </tr>
  );
};

export default ApiKeyItem;
