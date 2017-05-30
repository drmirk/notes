'''
currently this file manager is used in the ckeditor
to browse and upload images. this stores files in "static" folder.
'''
from __init__ import *
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            funcNum = request.args.get('CKEditorFuncNum')
            fileUrl = 'static/media/' + filename
            print(fileUrl)
            return render_template('file_browser.html', \
                close_window=True, funcNum=funcNum, fileUrl=fileUrl)

    return render_template('file_browser.html')
