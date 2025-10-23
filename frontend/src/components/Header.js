import React, { useState } from 'react';

const Header = () => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-pink-400 to-rose-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">B</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">BeautyPriceCompare</h1>
              <p className="text-sm text-gray-600">
                Find the best deal across Sephora AU, Sephora IN & Nykaa
              </p>
            </div>
          </div>

          {/* Info Tooltip */}
          <div className="relative">
            <button
              onMouseEnter={() => setShowTooltip(true)}
              onMouseLeave={() => setShowTooltip(false)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Information about pricing"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
              </svg>
            </button>
            
            {showTooltip && (
              <div className="absolute right-0 top-full mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 p-4 z-50">
                <div className="text-sm text-gray-700">
                  <p className="font-medium mb-2">💡 How it works:</p>
                  <ul className="space-y-1 text-xs">
                    <li>• Prices fetched live from official stores</li>
                    <li>• Exchange rates update hourly</li>
                    <li>• Best deals highlighted automatically</li>
                    <li>• All prices converted to AUD for easy comparison</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

