import os
import logging
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
import PyPDF2
import io
import tempfile
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_diagonal_watermark(input_pdf_path, output_pdf_path, watermark_text, opacity=0.2, color_rgb=(0.7, 0.7, 0.7)):
    """Add diagonal watermark to PDF file."""
    try:
        # Read the input PDF
        with open(input_pdf_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            # Process each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                
                # Get page dimensions
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # Create watermark
                watermark_buffer = io.BytesIO()
                watermark_canvas = canvas.Canvas(watermark_buffer, pagesize=(page_width, page_height))
                
                # Set watermark properties with custom color and opacity
                watermark_canvas.setFillColorRGB(color_rgb[0], color_rgb[1], color_rgb[2])
                watermark_canvas.setFillAlpha(opacity)
                
                # Calculate font size to cover most of the page
                import math
                diagonal_length = math.sqrt(page_width**2 + page_height**2)
                
                # Make font size large enough to span most of the diagonal
                font_size = diagonal_length / len(watermark_text) * 1.2
                
                # Ensure minimum and maximum font sizes
                min_font_size = min(page_width, page_height) / 12
                max_font_size = min(page_width, page_height) / 2
                font_size = max(min_font_size, min(font_size, max_font_size))
                
                watermark_canvas.setFont("Helvetica-Bold", font_size)
                
                # Calculate angle for diagonal from bottom-left to top-right
                angle = math.degrees(math.atan(page_height / page_width))
                
                # Position text to start from bottom-left area and extend to top-right
                # Calculate the center position for the diagonal
                x_center = page_width / 2
                y_center = page_height / 2
                
                # Save graphics state and apply transformation
                watermark_canvas.saveState()
                watermark_canvas.translate(x_center, y_center)
                watermark_canvas.rotate(angle)
                
                # Draw the text centered on the diagonal
                text_width = watermark_canvas.stringWidth(watermark_text, "Helvetica-Bold", font_size)
                watermark_canvas.drawString(-text_width/2, -font_size/2, watermark_text)
                
                # Restore graphics state
                watermark_canvas.restoreState()
                watermark_canvas.save()
                
                # Create watermark PDF page
                watermark_buffer.seek(0)
                watermark_pdf = PyPDF2.PdfReader(watermark_buffer)
                watermark_page = watermark_pdf.pages[0]
                
                # Merge watermark with original page
                page.merge_page(watermark_page)
                pdf_writer.add_page(page)
            
            # Write the output PDF
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                
        return True
        
    except Exception as e:
        app.logger.error(f"Error adding watermark: {str(e)}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route for file upload and processing."""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'pdf_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['pdf_file']
        watermark_text = request.form.get('watermark_text', '').strip()
        opacity = float(request.form.get('opacity', '0.2'))
        color = request.form.get('color', '#b3b3b3')
        
        # Convert hex color to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        
        color_rgb = hex_to_rgb(color)
        
        # Validate inputs
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not watermark_text:
            flash('Please enter watermark text', 'error')
            return redirect(request.url)
        
        if file.filename and not allowed_file(file.filename):
            flash('Please upload a PDF file', 'error')
            return redirect(request.url)
        
        try:
            # Generate unique filename
            unique_id = str(uuid.uuid4())
            original_filename = secure_filename(file.filename or "document.pdf")
            input_filename = f"{unique_id}_{original_filename}"
            
            # Create output filename as "watermark_text_original_filename"
            base_name, ext = os.path.splitext(original_filename)
            safe_watermark = "".join(c for c in watermark_text if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_watermark = safe_watermark.replace(' ', '_')[:50]  # Limit length and replace spaces
            output_filename = f"{safe_watermark}_{base_name}{ext}"
            
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # Save uploaded file
            file.save(input_path)
            app.logger.info(f"File saved: {input_path}")
            
            # Add watermark
            if add_diagonal_watermark(input_path, output_path, watermark_text, opacity, color_rgb):
                # Clean up input file
                try:
                    os.remove(input_path)
                except:
                    pass
                
                flash('Watermark added successfully!', 'success')
                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=output_filename,
                    mimetype='application/pdf'
                )
            else:
                flash('Error processing PDF file. Please try again.', 'error')
                # Clean up files
                try:
                    os.remove(input_path)
                    if os.path.exists(output_path):
                        os.remove(output_path)
                except:
                    pass
                
        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}")
            flash('An error occurred while processing the file. Please try again.', 'error')
    
    return render_template('index.html')

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    app.logger.error(f"Internal error: {str(e)}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

@app.route("/ping")
def ping():
    return "pong", 200
