import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/nicholassmith/Documents/Work/UNAAAY/YEAR5/TDP5'
ALLOWED_EXTENSIONS = set(['bmp', 'ai', 'eps', 'pdf', 'svg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# defaults
templateData = {'exposureTime' : '10','iterations': '50','substrateDiameter': '100'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def main():
    

    if request.method == "POST":

        fileUploaded = 'file' in request.files

        # check if user is uploading a file
        if not fileUploaded:

            # make sure the user has actually changed the settings
            settingsChanged = request.form.get('exp_time', None)

            if not settingsChanged:
                flash('No file selected.', 'danger')
                return redirect(request.url)

            templateData['exposureTime'] = request.form['exp_time']
            templateData['iterations'] = request.form['iterations']
            templateData['substrateDiameter'] = request.form['substrate_diam']

            flash('Settings saved.', 'success')

            
            return redirect(request.url)

        else: 
        
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
