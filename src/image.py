from app import failure_response, success_response
from flask import Flask, request, send_file
import os

def image_route(app):
    app.config['IMAGE_FOLDER_POST'] = os.path.join(os.path.dirname(__file__), 'images', 'posts')
    app.config['IMAGE_FOLDER_USER'] = os.path.join(os.path.dirname(__file__), 'images', 'users')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/api/images/posts/<int:post_id>/', methods=['POST'])
    def upload(post_id):
        if 'file' not in request.files:
            return failure_response("file not uploaded", 400)
    
        file = request.files['file']

        if file is None:
            return failure_response("file not uploaded", 400)
        
        if not allowed_file(file.filename):
            return failure_response("file not supported", 400)

        folder_path = app.config['IMAGE_FOLDER_POST']
        filename = os.path.join(folder_path, f"{post_id}.{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(filename)
        return success_response("images successfully saved at " + filename, 201)


    @app.route('/api/images/posts/<int:post_id>/')
    def get_image(post_id):
        # Retrieve the image file path
        image_path = os.path.join(app.config['IMAGE_FOLDER_POST'], post_id)
        
        if os.path.exists(image_path):
            return send_file(image_path, mimetype='image/jpeg')
        else:
            return failure_response("file not found")
