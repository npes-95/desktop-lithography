import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/nicholassmith/Documents/Work/UNAAAY/YEAR5/TDP5'
ALLOWED_EXTENSIONS = set(['bmp', 'ai', 'eps', 'pdf', 'svg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def main():

    # get relevant info from user
    templateData = {'exposureTime' : '10','iterations': '50','substrateDiameter': '100'}

    # TODO file name isnt showing up, fix this
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('main2.html', templateData = templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
