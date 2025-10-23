# 🎨 Render Deployment Guide

Render offers a generous free tier and easy GitHub integration.

## Quick Deploy Steps:

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository: `icedgreentee/ProdCompare`**
5. **Configure:**
   - **Name**: `beauty-price-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. **Deploy!**

## Environment Variables:
- `FLASK_ENV=production`

## Benefits:
- ✅ Free tier (750 hours/month)
- ✅ Automatic SSL
- ✅ Easy GitHub integration
- ✅ Built-in monitoring

Your app will be available at: `https://beauty-price-backend.onrender.com`
