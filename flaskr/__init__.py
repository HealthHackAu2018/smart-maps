import os
import shutil
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, send_file
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class

from python_read_data import parse_multiple_pdfs


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/', methods=['GET', 'POST'])
    def index():
        
        # list to hold our uploaded image urls
        file_urls = []
        
        if request.method == 'POST':
            file_obj = request.files
            for f in file_obj:
                file = request.files.get(f)
                
                # save the file with to our pdfs folder
                filename = pdfs.save(
                    file,
                    name=file.filename    
                )
                # append image urls
                file_urls.append(pdfs.url(filename))
                
            return "uploading..."
        return render_template('index.html')

    @app.route('/api/process-pdf', methods=['POST'])
    def process():
        file = request.files.get('data')
        if file:
            path_to_file = f'instance/{file.filename}'
            file.save(path_to_file)
            output = process_pdf(path_to_file)
            if os.path.exists(path_to_file):
                os.remove(path_to_file)
            return jsonify({'response': output})

        return jsonify({'error': 'No PDF file provided'})

    @app.route('/results')
    def results():
        parse_multiple_pdfs('flaskr/uploads')
        shutil.rmtree('flaskr/uploads')
        return send_file('../output.csv', attachment_filename='output.csv')

    return app


app = create_app()
dropzone = Dropzone(app)

app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'application/pdf'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results' 

# Uploads settings
app.config['UPLOADED_PDFS_DEST'] = os.getcwd() + '/flaskr/uploads'
pdfs = UploadSet('pdfs', ['pdf'])
configure_uploads(app, pdfs)
patch_request_class(app)  # set maximum file size, default is 16MB
