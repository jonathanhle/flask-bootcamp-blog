import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):
    # flask has it's own method for .filename for dealing with uploads: 
    # https: // stackoverflow.com/questions/46136478/flask-upload-how-to-get-file-name
    filename = pic_upload.filename
    
    # "mypicture . jpg" ==> split on . and get the jpg
    ext_type = filename.split('.')[-1]

    # "username.jpg"
    storage_filename = str(username) + '.' + ext_type
    
    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)

    output_size = (200, 200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
    

