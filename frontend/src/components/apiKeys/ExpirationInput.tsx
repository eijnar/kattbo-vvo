// src/components/apiKeys/ExpirationInput.tsx

import React from 'react';

interface ExpirationInputProps {
  expiresIn: string;
  onChange: (value: string) => void;
}

const ExpirationInput: React.FC<ExpirationInputProps> = ({ expiresIn, onChange }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Expiration (e.g., "30d" for 30 days):
      </label>
      <input
        type="text"
        value={expiresIn}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        placeholder="30d"
      />
    </div>
  );
};

export default ExpirationInput;
