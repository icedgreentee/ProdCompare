import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 py-8 mt-16">
      <div className="container mx-auto px-4">
        <div className="text-center">
          <div className="mb-4">
            <div className="flex items-center justify-center mb-2">
              <div className="w-8 h-8 bg-gradient-to-br from-pink-400 to-rose-500 rounded-lg flex items-center justify-center mr-2">
                <span className="text-white font-bold text-sm">B</span>
              </div>
              <span className="text-lg font-semibold text-gray-700">BeautyPriceCompare</span>
            </div>
          </div>
          
          <div className="text-sm text-gray-500 space-y-1">
            <p>Data sourced from Sephora and Nykaa public listings</p>
            <p>For personal use only • Prices updated in real-time</p>
            <p className="mt-2">
              Made with ❤️ for beauty enthusiasts
            </p>
          </div>
          
          <div className="mt-4 flex justify-center space-x-6">
            <button 
              className="text-gray-400 hover:text-gray-600 transition-colors text-sm cursor-pointer"
            >
              About
            </button>
            <button 
              className="text-gray-400 hover:text-gray-600 transition-colors text-sm cursor-pointer"
            >
              Privacy
            </button>
            <a 
              href="https://github.com/icedgreentee/ProdCompare" 
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-gray-600 transition-colors text-sm"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

