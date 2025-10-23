import React from 'react';

const ComparisonSummary = ({ results, exchangeRate }) => {
  if (!results || !results.cheapest) return null;

  const cheapestProduct = results.results.find(p => p.store === results.cheapest);
  const otherProducts = results.results.filter(p => p.store !== results.cheapest);
  
  if (!cheapestProduct || otherProducts.length === 0) return null;

  const cheapestPrice = cheapestProduct.currency === 'AUD' 
    ? cheapestProduct.price 
    : cheapestProduct.converted_price;

  const calculateSavings = (otherProduct) => {
    const otherPrice = otherProduct.currency === 'AUD' 
      ? otherProduct.price 
      : otherProduct.converted_price;
    
    const difference = otherPrice - cheapestPrice;
    const percentage = ((difference / otherPrice) * 100).toFixed(1);
    
    return { difference, percentage };
  };

  const maxSavings = otherProducts.reduce((max, product) => {
    const savings = calculateSavings(product);
    return savings.difference > max.difference ? savings : max;
  }, { difference: 0, percentage: 0 });

  return (
    <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-200 shadow-lg">
      {/* Main Summary */}
      <div className="text-center mb-6">
        <div className="flex items-center justify-center mb-3">
          <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mr-3">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">Best Deal Found!</h3>
        </div>
        
        <div className="text-3xl font-bold text-green-600 mb-2">
          {results.cheapest}
        </div>
        
        <div className="text-lg text-gray-700 mb-4">
          Save up to <span className="font-bold text-green-600">${maxSavings.difference.toFixed(2)} AUD</span> 
          <span className="text-gray-500"> (~{maxSavings.percentage}% cheaper)</span>
        </div>
      </div>

      {/* Price Comparison Chart */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-800 mb-4 text-center">Price Comparison</h4>
        <div className="space-y-3">
          {results.results.map((product, index) => {
            const price = product.currency === 'AUD' ? product.price : product.converted_price;
            const isCheapest = product.store === results.cheapest;
            const savings = isCheapest ? 0 : calculateSavings(product);
            
            return (
              <div key={index} className="flex items-center">
                <div className="w-24 text-sm font-medium text-gray-700">
                  {product.store}
                </div>
                <div className="flex-1 mx-4">
                  <div className="relative">
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className={`h-3 rounded-full transition-all duration-500 ${
                          isCheapest 
                            ? 'bg-gradient-to-r from-green-400 to-green-500' 
                            : 'bg-gradient-to-r from-pink-400 to-rose-400'
                        }`}
                        style={{ width: `${Math.max(20, (price / Math.max(...results.results.map(p => p.currency === 'AUD' ? p.price : p.converted_price))) * 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
                <div className="w-20 text-right">
                  <div className={`text-sm font-bold ${isCheapest ? 'text-green-600' : 'text-gray-700'}`}>
                    ${price.toFixed(2)}
                  </div>
                  {!isCheapest && (
                    <div className="text-xs text-red-500">
                      +${savings.difference.toFixed(2)}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Exchange Rate Info */}
      <div className="text-center text-sm text-gray-600 bg-white/50 rounded-lg p-3">
        <div className="flex items-center justify-center">
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Exchange rate: 1 INR = {exchangeRate.toFixed(4)} AUD
        </div>
        <div className="text-xs text-gray-500 mt-1">
          Updated: {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default ComparisonSummary;

