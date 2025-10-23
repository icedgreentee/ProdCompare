import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import ProductCard from './components/ProductCard';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import ExchangeRateInfo from './components/ExchangeRateInfo';
import ComparisonSummary from './components/ComparisonSummary';
import Footer from './components/Footer';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.herokuapp.com';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [exchangeRate, setExchangeRate] = useState(null);

  const handleSearch = async (productName) => {
    if (!productName.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/compare`, {
        params: { product: productName }
      });

      setResults(response.data);
      setExchangeRate(response.data.exchange_rate);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch product data');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    if (searchTerm) {
      handleSearch(searchTerm);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-rose-50">
      <Header />
      
      <div className="pt-24">
        <div className="container mx-auto px-4 py-8">

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto mb-8">
          <SearchBar
            onSearch={handleSearch}
            loading={loading}
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
          />
        </div>

        {/* Exchange Rate Info */}
        {exchangeRate && (
          <div className="max-w-2xl mx-auto mb-6">
            <ExchangeRateInfo rate={exchangeRate} />
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center">
            <LoadingSpinner />
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="max-w-2xl mx-auto">
            <ErrorMessage message={error} onRetry={handleRefresh} />
          </div>
        )}

        {/* Results */}
        {results && !loading && !error && (
          <div className="space-y-8">
            {/* Comparison Summary */}
            <div className="max-w-4xl mx-auto">
              <ComparisonSummary results={results} exchangeRate={exchangeRate} />
            </div>

            {/* Product Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {results.results.map((product, index) => (
                <ProductCard
                  key={index}
                  product={product}
                  isCheapest={product.store === results.cheapest}
                />
              ))}
            </div>

            {/* Refresh Button */}
            <div className="text-center">
              <button
                onClick={handleRefresh}
                className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white font-semibold py-3 px-8 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                🔄 Refresh Prices
              </button>
            </div>
          </div>
        )}
        </div>
      </div>
      
      <Footer />
    </div>
  );
}

export default App;
