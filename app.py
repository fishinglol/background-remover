from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return 'OK', 200

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        file = request.files["file"]
        if file.filename == '':
            return 'No file selected', 400
        if file:
            input_image = Image.open(file.stream)
            
            # Resize large images to save memory
            max_size = 1024
            if input_image.width > max_size or input_image.height > max_size:
                input_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            output_imge = remove(input_image, post_process_mask=True)
            img_io = BytesIO()
            output_imge.save(img_io,'PNG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='_rmbg.png')
        
    return render_template('index.html')
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
