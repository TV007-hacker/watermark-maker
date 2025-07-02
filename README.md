# Tanay's Watermark Tool

A web-based PDF watermarking tool that adds diagonal text watermarks to PDF files with customizable opacity and colors.

![Watermark Tool Screenshot](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Tanay's+Watermark+Tool)

## ✨ Features

- 📄 Upload PDF files (up to 16MB)
- 🔤 Add custom diagonal watermarks from bottom-left to top-right
- 🎨 Adjustable opacity (10% to 100%)
- 🌈 Color picker with preset options
- 💾 Download with format: `watermark_text_original_filename.pdf`
- 📱 Responsive design with dark theme
- ⚡ Fast processing with immediate download

## 🚀 Live Demo

[Try the tool here](https://your-deployed-url.com) (Add your deployment URL here)

## 🔧 Quick Start

### Option 1: Run Locally
```bash
git clone https://github.com/yourusername/watermark-tool.git
cd watermark-tool
pip install flask gunicorn PyPDF2 reportlab werkzeug
python app.py
```

Visit `http://localhost:5000`

### Option 2: Deploy to Cloud (Free)
Click one of these buttons to deploy instantly:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Deployment Instructions

### Railway (Recommended - Free with Autoscaling)

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up
2. **Connect GitHub**: Link your GitHub account to Railway
3. **Push Code**: Push this project to a GitHub repository
4. **Deploy**: 
   - Click "New Project" on Railway
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect and deploy your Flask app

### Render (Alternative Free Option)

1. **Create Render Account**: Sign up at [render.com](https://render.com)
2. **New Web Service**: Click "New +" → "Web Service"
3. **Connect Repository**: Link your GitHub repo
4. **Settings**:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt` (auto-detected)
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`

### Fly.io (Another Alternative)

1. **Install Fly CLI**: Follow instructions at [fly.io](https://fly.io/docs/getting-started/installing-flyctl/)
2. **Login**: `flyctl auth login`
3. **Launch**: `flyctl launch` (in project directory)
4. **Deploy**: `flyctl deploy`

## Free Tier Limits

- **Railway**: 500 hours/month (enough for 24/7), $5 credit monthly
- **Render**: 750 hours/month free
- **Fly.io**: 160 hours/month free, but can run 24/7 with minimal usage

## Local Development

```bash
pip install flask gunicorn PyPDF2 reportlab werkzeug
python app.py
```

Visit `http://localhost:5000`

## File Structure

- `app.py` - Main Flask application
- `main.py` - Entry point for deployment
- `templates/index.html` - Web interface
- `static/style.css` - Custom styling
- `uploads/` - Temporary file storage
- `output/` - Processed files storage