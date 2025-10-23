#!/bin/bash

echo "🚀 Deploying Beauty Price Comparison App to Netlify..."

# Build the frontend
echo "📦 Building frontend..."
cd frontend
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful!"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

# Go back to root
cd ..

echo "🎉 Ready for Netlify deployment!"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repo to Netlify"
echo "3. Set build command: cd frontend && npm run build"
echo "4. Set publish directory: frontend/build"
echo "5. Add environment variable: REACT_APP_API_URL=https://your-backend-url.herokuapp.com"
echo ""
echo "For backend deployment:"
echo "1. Deploy Flask backend to Heroku/Railway/Render"
echo "2. Update REACT_APP_API_URL with your backend URL"

