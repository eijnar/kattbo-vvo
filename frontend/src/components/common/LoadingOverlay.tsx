import React from 'react';
import Spinner from './Spinner';

interface LoadingOverlayProps {
  isLoading: boolean;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ isLoading }) => {
  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50">
      <Spinner size="lg" color="text-white" />
      <span className="sr-only">Loading...</span>
    </div>
  );
};

export default LoadingOverlay;
