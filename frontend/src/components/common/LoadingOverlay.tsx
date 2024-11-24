// src/components/common/LoadingOverlay.tsx

import React, {ReactNode} from 'react';
import Spinner from './Spinner';

interface LoadingOverlayProps {
  isLoading: boolean;
  children: ReactNode;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ isLoading, children }) => {
  return (
    <div className="relative">
      {children}
      {isLoading && (
        <div className="absolute inset-0 flex justify-center items-center bg-white bg-opacity-75">
          <Spinner size="lg" color="text-blue-500" />
        </div>
      )}
    </div>
  );
};

export default LoadingOverlay;
