import React from 'react';

const ProductCard = ({ product, isCheapest }) => {
  const getStoreColor = (store) => {
    switch (store) {
      case 'Sephora AU':
        return 'border-sephora-pink bg-pink-50';
      case 'Sephora IN':
        return 'border-purple-500 bg-purple-50';
      case 'Nykaa':
        return 'border-nykaa-pink bg-pink-50';
      default:
        return 'border-gray-300 bg-gray-50';
    }
  };

  const getStoreLogo = (store) => {
    switch (store) {
      case 'Sephora AU':
        return '🛍️';
      case 'Sephora IN':
        return '🇮🇳';
      case 'Nykaa':
        return '💄';
      default:
        return '🏪';
    }
  };

  const formatPrice = (price, currency) => {
    if (currency === 'AUD') {
      return `$${price.toFixed(2)} AUD`;
    } else if (currency === 'INR') {
      return `₹${price.toLocaleString('en-IN')} INR`;
    }
    return `${price} ${currency}`;
  };

  // const getPriceDifference = () => {
  //   if (!product.converted_price) return null;
  //   
  //   const originalPrice = product.price;
  //   const convertedPrice = product.converted_price;
  //   const difference = Math.abs(originalPrice - convertedPrice);
  //   const percentage = ((difference / originalPrice) * 100).toFixed(1);
  //   
  //   return { difference, percentage };
  // };

  return (
    <div className={`relative border-2 rounded-2xl p-6 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${
      isCheapest 
        ? 'border-green-400 bg-gradient-to-br from-green-50 to-emerald-50 shadow-xl ring-2 ring-green-200' 
        : 'border-gray-200 bg-white hover:border-pink-300 hover:shadow-lg'
    }`}>
      {/* Cheapest Badge */}
      {isCheapest && (
        <div className="absolute -top-2 -right-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full">
          BEST DEAL
        </div>
      )}

      {/* Store Header */}
      <div className="flex items-center mb-4">
        <span className="text-2xl mr-2">{getStoreLogo(product.store)}</span>
        <h3 className="text-lg font-semibold text-gray-800">{product.store}</h3>
      </div>

      {/* Product Image */}
      {product.image && (
        <div className="mb-4">
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-32 object-cover rounded-lg"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      )}

      {/* Product Name */}
      <h4 className="text-sm font-medium text-gray-700 mb-3 line-clamp-2">
        {product.name}
      </h4>

      {/* Price Information */}
      <div className="space-y-2">
        <div className="text-2xl font-bold text-gray-900">
          {formatPrice(product.price, product.currency)}
        </div>
        
        {product.converted_price && (
          <div className="text-lg text-blue-600 font-medium">
            ≈ {formatPrice(product.converted_price, 'AUD')}
          </div>
        )}

        {/* Price difference info */}
        {product.converted_price && (
          <div className="text-sm text-gray-600">
            {product.currency === 'INR' && (
              <span>
                Converted from {product.currency} to AUD
              </span>
            )}
          </div>
        )}
      </div>

      {/* Stock Status */}
      <div className="mt-4">
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          product.in_stock 
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}>
          <span className={`w-2 h-2 rounded-full mr-1 ${
            product.in_stock ? 'bg-green-400' : 'bg-red-400'
          }`}></span>
          {product.in_stock ? 'In Stock' : 'Out of Stock'}
        </span>
      </div>

      {/* View Product Button */}
      <div className="mt-6">
        <a
          href={product.url}
          target="_blank"
          rel="noopener noreferrer"
          className={`w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white transition-colors duration-200 ${
            product.in_stock
              ? 'bg-blue-600 hover:bg-blue-700'
              : 'bg-gray-400 cursor-not-allowed'
          }`}
          disabled={!product.in_stock}
        >
          {product.in_stock ? 'View Product' : 'Out of Stock'}
          <svg className="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </a>
      </div>
    </div>
  );
};

export default ProductCard;
