# 🚀 Deployment Guide

## Backend Deployment (Heroku)

### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
cd backend
heroku create your-app-name-backend
```

### 4. Deploy Backend
```bash
git add .
git commit -m "Deploy backend"
git push heroku main
```

### 5. Set Environment Variables (Optional)
```bash
heroku config:set FLASK_ENV=production
```

## Frontend Deployment (Netlify)

### 1. Build Frontend
```bash
cd frontend
npm run build
```

### 2. Deploy to Netlify

#### Option A: Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod --dir=frontend/build
```

#### Option B: Netlify Web Interface
1. Go to [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Connect your GitHub repository
4. Set build settings:
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/build`
5. Add environment variable:
   - **REACT_APP_API_URL**: `https://your-backend-url.herokuapp.com`

### 3. Update API URL
After backend deployment, update the frontend API URL:
```bash
# In Netlify dashboard, go to Site settings > Environment variables
# Add: REACT_APP_API_URL = https://your-backend-url.herokuapp.com
```

## Alternative Backend Hosting

### Railway
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Select backend folder
4. Deploy automatically

### Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`

## Environment Variables

### Backend (.env)
```
FLASK_ENV=production
```

### Frontend (Netlify)
```
REACT_APP_API_URL=https://your-backend-url.herokuapp.com
```

## Testing Deployment

### Backend Health Check
```bash
curl https://your-backend-url.herokuapp.com/health
```

### Frontend Test
Visit your Netlify URL and test the search functionality.

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure Flask-CORS is properly configured
2. **Build Failures**: Check Node.js version compatibility
3. **API Timeouts**: Increase timeout settings in backend
4. **Scraping Issues**: Websites may block requests; implement retry logic

### Performance Optimization

1. **Caching**: Implement Redis for caching search results
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **CDN**: Use CloudFlare for static assets
4. **Database**: Add PostgreSQL for storing search history

## Monitoring

### Backend Monitoring
- Heroku Metrics
- Logs: `heroku logs --tail`
- Uptime monitoring with Pingdom

### Frontend Monitoring
- Netlify Analytics
- Error tracking with Sentry
- Performance monitoring with Lighthouse

## Security Considerations

1. **API Keys**: Store in environment variables
2. **Rate Limiting**: Implement request throttling
3. **Input Validation**: Sanitize all user inputs
4. **HTTPS**: Ensure all connections are encrypted
5. **CORS**: Configure proper CORS policies

## Scaling

### Backend Scaling
- Use Heroku Hobby plan for production
- Implement caching with Redis
- Use background jobs for heavy scraping

### Frontend Scaling
- Use Netlify Pro for advanced features
- Implement CDN for global performance
- Add service worker for offline functionality

