import os
from flask import Flask, request, jsonify
from python_pdf_parser.smart_pdf_parser import process_pdf


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

    return app