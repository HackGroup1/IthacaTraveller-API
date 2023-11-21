from flask import Flask, request, send_file
from db import Post, User
import json
import os

def success_response(body, code = 200):
    return json.dumps(body), code

def failure_response(message, code = 404):
    return json.dumps({"error": message}), code



def image_route(app):
    app.config['IMAGE_FOLDER_POST'] = os.path.join(os.path.dirname(__file__), 'images', 'posts')
    app.config['IMAGE_FOLDER_USER'] = os.path.join(os.path.dirname(__file__), 'images', 'users')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    def check_existance(folder_key, name):
        """
        Check if given image name exist with any allowed extensions
        Return path if found
        None is not
        """
        for extension in app.config['ALLOWED_EXTENSIONS']:
                image_path = os.path.join(app.config[folder_key], str(name) + "." + extension)
                if os.path.exists(image_path):
                    return image_path  
        return None

    def allowed_file(filename):
        """
        Checks if file has allowed extensions
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    #------------Post route-----------------------------------------------------
    @app.route('/api/images/posts/<int:post_id>/', methods=['POST'])
    def upload_post_image(post_id):
        """
        Takes uploaded image and store in IMAGE_FOLDER_POST
        """
        post = Post.query.filter_by(id=post_id).first()

        if post is None:
            return failure_response("post not found")

        if 'file' not in request.files:
            return failure_response("file keyword not provided", 400)
    
        file = request.files['file']

        if file is None:
            return failure_response("file not uploaded", 400)
        
        if not allowed_file(file.filename):
            return failure_response("file not supported", 400)
        
        check = check_existance('IMAGE_FOLDER_POST', post_id)

        while check is not None:
            os.remove(check)
            check = check_existance('IMAGE_FOLDER_POST', post_id)

        folder_path = app.config['IMAGE_FOLDER_POST']
        filename = os.path.join(folder_path, f"{post_id}.{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(filename)
        return success_response("images successfully saved at server", 201)


    @app.route('/api/images/posts/<int:post_id>/')
    def get_post_image(post_id):
       """
       Given post id, gets and returns image from IMAGE_FOLDER_POST
       """
       post = Post.query.filter_by(id=post_id).first()
       
       if post is None:
            return failure_response("post not found")
       
       check = check_existance('IMAGE_FOLDER_POST', post_id)
       if check is not None:
            return send_file(check, mimetype='image/jpeg')
       return failure_response("file not found")
    
    @app.route('/api/images/post/<int:post_id>/', methods=["DELETE"])
    def delete_post_image(post_id):
        """
        With given post_id, remove the image in IMAGE_FOLDER_POST
        """
        post = Post.query.filter_by(id=post_id).first()

        if post is None:
            return failure_response("post not found")
        
        check = check_existance('IMAGE_FOLDER_POST', post_id)

        if check is None: 
            return failure_response("image not found")
        
        while check is not None:
            os.remove(check)
            check = check_existance('IMAGE_FOLDER_POST', post_id)

        return success_response("image removed")
    
    #------------------------user route---------------------------------------
    @app.route('/api/images/user/<int:user_id>/', methods=['POST'])
    def upload_user_image(user_id):
        """
        Takes uploaded image and store in IMAGE_FOLDER_USER
        """
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            return failure_response("user not found")

        if 'file' not in request.files:
            return failure_response("file keyword not provided", 400)
    
        file = request.files['file']

        if file is None:
            return failure_response("file not uploaded", 400)
        
        if not allowed_file(file.filename):
            return failure_response("file not supported", 400)
        
        check = check_existance('IMAGE_FOLDER_USER', user_id)

        while check is not None:
            os.remove(check)
            check = check_existance('IMAGE_FOLDER_USER', user_id)

        folder_path = app.config['IMAGE_FOLDER_USER']
        filename = os.path.join(folder_path, f"{user_id}.{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(filename)
        return success_response("images successfully saved at server", 201)


    @app.route('/api/images/users/<int:user_id>/')
    def get_user_image(user_id):
       """
       With given post_id, gets and returns the image in IMAGE_FOLDER_USER
       """
       user = User.query.filter_by(id=user_id).first()
       
       if user is None:
            return failure_response("user not found")
       
       check = check_existance('IMAGE_FOLDER_USER', user_id)
       if check is not None:
            return send_file(check, mimetype='image/jpeg')
       return failure_response("file not found")
    
    @app.route('/api/images/user/<int:user_id>/', methods=["DELETE"])
    def delete_user_image(user_id):
        """
        With given post_id, remove the image in IMAGE_FOLDER_IMAGE
        """
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            return failure_response("user not found")
        
        check = check_existance('IMAGE_FOLDER_USER', user_id)

        if check is None: 
            return failure_response("image not found")
        
        while check is not None:
            os.remove(check)
            check = check_existance('IMAGE_FOLDER_USER', user_id)

        return success_response("image removed")
    

