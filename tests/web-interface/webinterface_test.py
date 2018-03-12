import os
from flask import Flask, render_template, request, redirect, url_for, flash
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

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        file = request.files['file']

        print(file.filename)

        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            #this is where we want to pass the file to the DMD/processing functions

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('New photomask ({}) added!'.format(filename), 'success')
            return redirect(request.url)

        else:
            flash('Incompatible file format. Please try again.', 'danger')
            return redirect(request.url)

    return render_template('main2.html', templateData = templateData)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=80, debug=True)
