#!/usr/local/bin/python2.7

from flask import (Flask, render_template, make_response, request,
                   redirect, url_for,
                   session, flash, send_from_directory)
from werkzeug import secure_filename
app = Flask(__name__)

import os
import imghdr

app.secret_key = 'rosebud'

@app.route('/upload', methods=["GET", "POST"])
def file_upload():
    if request.method == 'GET':
        return render_template('form.html',src='',nm='')
    else:
        try:
            nm = int(request.form['nm']) # may throw error
            f = request.files['pic']
            mime_type = imghdr.what(f.stream)
            if mime_type != 'jpeg':
                raise Exception('Not a JPEG')
            filename = secure_filename(str(nm)+'.jpeg')
            pathname = 'images/'+filename
            f.save(pathname)
            flash('Upload successful')
            return render_template('form.html',
                                   src=url_for('pic',fname=filename),
                                   nm=nm)

        except Exception as err:
            flash('Upload failed {why}'.format(why=err))
            return render_template('form.html',src='',nm='')

@app.route('/pic/<fname>')
def pic(fname):
    f = secure_filename(fname)
    return send_from_directory('images',f)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',os.getuid())
