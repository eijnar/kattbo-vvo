// src/components/common/Button.tsx

import React from 'react';

interface ButtonProps {
  onClick?: () => void;
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  className?: string; // Allow custom Tailwind classes
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  onClick,
  children,
  type = 'button',
  className = '',
  disabled = false,
}) => (
  <button
    type={type}
    onClick={onClick}
    className={`px-4 py-2 bg-secondary text-black rounded hover:bg-secondary-hover focus:outline-none focus:ring-2 focus:ring-blue-300 transition duration-300 ease-in-out ${className}`}
    disabled={disabled}
  >
    {children}
  </button>
);

export default Button;