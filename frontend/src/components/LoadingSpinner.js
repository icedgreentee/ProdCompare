import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p className="mt-4 text-gray-600 font-medium">Searching for products...</p>
      <p className="mt-2 text-sm text-gray-500">This may take a few moments</p>
    </div>
  );
};

export default LoadingSpinner;

