# Tanay's Watermark Tool - Project Documentation

## Overview
A Flask web application for adding diagonal text watermarks to PDF files. Features include custom text watermarks, adjustable opacity, color selection, and automatic file naming with format: `watermark_text_original_filename.pdf`.

## User Preferences
- Tool heading should be "Tanay's Watermark Tool"
- Watermark positioning: diagonal from bottom-left to top-right corner
- Watermark should be large enough to cover the page while remaining readable
- File naming format: `watermark_text_original_filename.pdf`
- Remove preview functionality - users don't need to see watermark preview
- Include opacity and color customization options

## Project Architecture
- **Flask Backend**: Handles file uploads, PDF processing, and watermark generation
- **ReportLab**: PDF manipulation and watermark creation
- **PyPDF2**: PDF reading and page merging
- **Bootstrap Dark Theme**: UI styling with Replit-themed CSS
- **File Structure**:
  - `app.py` - Main Flask application with watermarking logic
  - `main.py` - Entry point for deployment
  - `templates/index.html` - Web interface
  - `static/style.css` - Custom styling
  - `uploads/` - Temporary file storage
  - `output/` - Processed files storage

## Recent Changes
- **2025-07-02**: Added deployment configuration files (Procfile, railway.json, .gitignore, LICENSE)
- **2025-07-02**: Updated README.md with comprehensive setup instructions
- **2025-07-02**: Prepared for GitHub repository creation
- **2025-06-13**: Implemented opacity and color controls
- **2025-06-13**: Updated filename format to user's specification
- **2025-06-13**: Removed preview section from interface
- **2025-06-13**: Increased watermark font size for better page coverage

## Deployment Ready For
- Railway (recommended for free autoscaling)
- Render (alternative free option)
- Fly.io (another free alternative)
- GitHub repository with proper documentation

## Current Status
Ready for GitHub repository creation and deployment to free hosting platforms with autoscaling capabilities.