import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  fullWidth?: boolean;
}

const Input: React.FC<InputProps> = ({
  className = '',
  fullWidth = false,
  ...props
}) => {
  return (
    <input
      className={`px-4 py-2 border border-gray-300 rounded-md text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
        fullWidth ? 'w-full' : ''
      } ${className}`}
      {...props}
    />
  );
};

export default Input;
