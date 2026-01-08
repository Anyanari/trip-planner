import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  onClick, 
  type = 'button', 
  className = '', 
  disabled = false 
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`btn-primary ${className}`}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
