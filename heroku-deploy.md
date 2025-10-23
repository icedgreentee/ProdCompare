# 🟣 Heroku Deployment Guide

## Prerequisites:
- Complete Heroku login: `heroku login`
- Press any key when prompted to open browser
- Complete authentication in browser

## Deploy Steps:

```bash
# 1. Create Heroku app
heroku create beauty-price-backend

# 2. Navigate to backend directory
cd backend

# 3. Add Heroku remote
heroku git:remote -a beauty-price-backend

# 4. Deploy
git add .
git commit -m "Deploy backend to Heroku"
git push heroku main

# 5. Check logs
heroku logs --tail
```

## Environment Variables (Optional):
```bash
heroku config:set FLASK_ENV=production
```

## Your app will be available at:
`https://beauty-price-backend.herokuapp.com`
