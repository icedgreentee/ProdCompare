# 💄 Beauty Price Comparison

[![Netlify Status](https://api.netlify.com/api/v1/badges/your-badge-id/deploy-status)](https://app.netlify.com/sites/your-site-name/deploys)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=flat&logo=heroku&logoColor=white)](https://your-backend-url.herokuapp.com)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

A beautiful, modern web application that compares live beauty product prices across **Sephora Australia**, **Sephora India**, and **Nykaa**. Find the best deals with real-time currency conversion and smart product matching.

## ✨ Features

### 🛍️ **Multi-Store Comparison**
- Compare prices across Sephora Australia, Sephora India, and Nykaa
- Real-time price fetching with live stock status
- Smart product matching across all stores

### 💱 **Live Currency Conversion**
- Automatic INR to AUD conversion using live exchange rates
- Display both original and converted prices
- Real-time exchange rate updates

### 🎨 **Beautiful Modern UI**
- Responsive design with TailwindCSS
- Smooth animations and transitions
- Auto-suggestions with product thumbnails
- Best deal highlighting with visual indicators

### 🔍 **Smart Search**
- Auto-suggestions as you type
- Keyboard navigation support
- Debounced API calls for optimal performance
- Product image previews

### 📱 **Mobile-First Design**
- Fully responsive across all devices
- Touch-friendly interface
- Optimized for mobile shopping

## 🚀 Live Demo

**Frontend**: [https://your-netlify-url.netlify.app](https://your-netlify-url.netlify.app)  
**Backend API**: [https://your-backend-url.herokuapp.com](https://your-backend-url.herokuapp.com)

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Poppins Font** - Beautiful typography

### Backend
- **Flask** - Lightweight Python web framework
- **BeautifulSoup** - HTML parsing and scraping
- **Requests** - HTTP library for web requests
- **Flask-CORS** - Cross-origin resource sharing

### APIs & Services
- **ExchangeRate.host** - Live currency conversion
- **Netlify** - Frontend hosting and deployment
- **Heroku** - Backend hosting and deployment

## 📦 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm** or **yarn**

### 1. Clone the Repository
```bash
git clone https://github.com/icedgreentee/ProdCompare.git
cd ProdCompare
```

### 2. Install Dependencies
```bash
# Install all dependencies
npm run install-all

# Or install separately
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### 3. Start Development Servers
```bash
# Start both frontend and backend
npm run dev

# Or start separately
npm run start-backend  # Backend on http://localhost:5001
npm run start-frontend # Frontend on http://localhost:3001
```

### 4. Open Your Browser
Visit `http://localhost:3001` to see the application in action!

## 🔧 API Documentation

### Compare Products
```http
GET /compare?product=Rare%20Beauty%20Blush
```

**Response:**
```json
{
  "exchange_rate": 0.0183,
  "results": [
    {
      "store": "Sephora AU",
      "name": "Rare Beauty Soft Pinch Liquid Blush",
      "price": 39.00,
      "currency": "AUD",
      "url": "https://www.sephora.com.au/...",
      "image": "https://...",
      "in_stock": true
    },
    {
      "store": "Sephora IN",
      "name": "Rare Beauty Soft Pinch Liquid Blush",
      "price": 2999,
      "currency": "INR",
      "converted_price": 54.68,
      "url": "https://www.sephora.in/...",
      "image": "https://...",
      "in_stock": true
    }
  ],
  "cheapest": "Sephora AU",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Health Check
```http
GET /health
```

## 🎯 Usage Examples

### Popular Searches
- **Rare Beauty**: "Rare Beauty Soft Pinch Liquid Blush"
- **Fenty Beauty**: "Fenty Beauty Gloss Bomb"
- **Charlotte Tilbury**: "Charlotte Tilbury Pillow Talk"
- **MAC**: "MAC Ruby Woo"
- **NARS**: "NARS Orgasm"

### Search Tips
- Use specific product names for better results
- Include brand names for more accurate matching
- Try different variations if no results found

## 🚀 Deployment

### Frontend (Netlify)
1. Connect your GitHub repository to Netlify
2. Set build command: `cd frontend && npm run build`
3. Set publish directory: `frontend/build`
4. Add environment variable: `REACT_APP_API_URL=https://your-backend-url.herokuapp.com`

### Backend (Heroku)
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Deploy: `git push heroku main`
4. Set environment variables in Heroku dashboard

### Alternative Hosting
- **Railway**: Simple deployment with automatic scaling
- **Render**: Free tier available for small projects
- **Vercel**: Great for frontend deployment

## 🎨 Design System

### Colors
- **Primary Pink**: `#f6d1d1` - Soft accent color
- **Highlight Green**: `#e0f6e2` - Best deal indicator
- **Background**: `#fefefe` - Clean cream background
- **Text**: `#1a1a1a` - High contrast for readability

### Typography
- **Font Family**: Poppins (Google Fonts)
- **Sizes**: Large for prices, medium for names, small for details
- **Weights**: 300-700 for visual hierarchy

### Components
- **Cards**: Rounded corners with subtle shadows
- **Buttons**: Gradient backgrounds with hover effects
- **Inputs**: Clean borders with focus states
- **Animations**: 300ms ease-in-out transitions

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px (Stacked layout)
- **Tablet**: 768px - 1024px (2-column grid)
- **Desktop**: > 1024px (3-column layout)

### Mobile Features
- Touch-friendly buttons (44px minimum)
- Swipe gestures for navigation
- Optimized images and loading
- Offline-ready with service workers

## 🔒 Security & Privacy

- **CORS**: Properly configured for cross-origin requests
- **Input Validation**: All user inputs are sanitized
- **Rate Limiting**: Prevents API abuse
- **HTTPS**: All connections are encrypted
- **No Data Storage**: No personal data is stored

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📊 Performance

### Frontend Optimizations
- **Code Splitting**: Lazy loading for better performance
- **Image Optimization**: WebP format with fallbacks
- **Caching**: Service worker for offline functionality
- **Bundle Size**: Optimized with tree shaking

### Backend Optimizations
- **Caching**: Redis for search result caching
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Error Handling**: Graceful degradation for failed requests
- **Monitoring**: Health checks and performance metrics

## 🐛 Troubleshooting

### Common Issues

**CORS Errors**
```bash
# Ensure Flask-CORS is properly configured
pip install Flask-CORS
```

**Build Failures**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API Timeouts**
- Check your internet connection
- Verify the backend is running
- Check browser console for errors

### Getting Help
- 📖 Check the [Documentation](docs/)
- 🐛 Report bugs in [Issues](https://github.com/icedgreentee/ProdCompare/issues)
- 💬 Join our [Discussions](https://github.com/icedgreentee/ProdCompare/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sephora** - For providing access to product data
- **Nykaa** - For their comprehensive beauty catalog
- **ExchangeRate.host** - For reliable currency conversion
- **TailwindCSS** - For the beautiful design system
- **React** - For the amazing frontend framework

## ⚠️ Disclaimer

This application is for **educational and personal use only**. Please respect the terms of service of the websites being scraped. Consider using official APIs when available.

---

<div align="center">

**Made with ❤️ for beauty enthusiasts**

[⭐ Star this repo](https://github.com/icedgreentee/ProdCompare) • [🐛 Report Bug](https://github.com/icedgreentee/ProdCompare/issues) • [💡 Request Feature](https://github.com/icedgreentee/ProdCompare/issues)

</div>

