from flask import Flask, request, send_file
import json
import os

def success_response(body, code = 200):
    return json.dumps(body), code

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code

def image_route(app):
    app.config['IMAGE_FOLDER_POST'] = "/usr/app/images/posts"
    app.config['IMAGE_FOLDER_USER'] = "/usr/app/images/users"
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
        return success_response("images successfully saved at server", 201)


    @app.route('/api/images/posts/<int:post_id>/')
    def get_image(post_id):
        # Retrieve the image file path
        
        for extension in app.config['ALLOWED_EXTENSIONS']:
            image_path = os.path.join(app.config['IMAGE_FOLDER_POST'], str(post_id) + "." + extension)

            if os.path.exists(image_path):
                return send_file(image_path, mimetype='image/jpeg')

        return failure_response("file not found")
