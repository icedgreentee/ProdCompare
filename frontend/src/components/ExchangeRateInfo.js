import React from 'react';

const ExchangeRateInfo = ({ rate }) => {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <p className="text-sm font-medium text-blue-800">
            Current Exchange Rate: 1 INR = {rate.toFixed(4)} AUD
          </p>
          <p className="text-xs text-blue-600 mt-1">
            Indian prices are automatically converted to Australian Dollars
          </p>
        </div>
      </div>
    </div>
  );
};

export default ExchangeRateInfo;

