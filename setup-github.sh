#!/bin/bash

echo "🚀 Setting up GitHub repository for Beauty Price Comparison..."

# Initialize git repository
echo "📁 Initializing git repository..."
git init

# Add remote origin
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/icedgreentee/ProdCompare.git

# Add all files
echo "📦 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🎉 Initial commit: Beauty Price Comparison App

✨ Features:
- Compare prices across Sephora AU, Sephora IN, and Nykaa
- Live currency conversion (INR to AUD)
- Modern React frontend with TailwindCSS
- Flask backend with web scraping
- Responsive design with beautiful UI
- Auto-suggestions and smart search
- Best deal highlighting

🛠 Tech Stack:
- Frontend: React + TailwindCSS + Axios
- Backend: Flask + BeautifulSoup + Requests
- Deployment: Netlify (frontend) + Heroku (backend)

🚀 Ready for deployment!"

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🔗 Repository: https://github.com/icedgreentee/ProdCompare"
echo ""
echo "📋 Next steps:"
echo "1. Deploy backend to Heroku"
echo "2. Deploy frontend to Netlify"
echo "3. Update environment variables"
echo "4. Test the live application"
echo ""
echo "🎉 Your beauty price comparison app is now on GitHub!"
