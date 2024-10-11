// src/components/common/Input.tsx

import React from 'react';

interface InputProps {
  label: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  type?: string;
  disabled?: boolean; // Add this line
}

const Input: React.FC<InputProps> = ({
  label,
  name,
  value,
  onChange,
  type = 'text',
  disabled = false, // Default to false
}) => (
  <div style={{ margin: '10px 0' }}>
    <label style={{ display: 'block', marginBottom: '5px' }}>
      {label}
    </label>
    <input
      name={name}
      value={value}
      onChange={onChange}
      type={type}
      disabled={disabled} // Pass the disabled prop to the input element
      style={{
        padding: '8px',
        width: '300px',
        backgroundColor: disabled ? '#f3f4f6' : 'white', // Optional: Visual cue for disabled state
        cursor: disabled ? 'not-allowed' : 'pointer', // Optional: Cursor change for disabled state
      }}
    />
  </div>
);

export default Input;