from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory)
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random

import dbconn2

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


@app.route('/')
def lookup():
    return render_template('home.html')

# This route processes the form; it's not intended for users
# @app.route('/search/', methods=['GET','POST'])
# def search():
#     #requests the inputs
#     if request.method == 'POST':
#     	title = request.form[('search-title')]
#     	conn = dbconn2.connect(DSN)
#     	movie = searchTitle(conn,title)
#     	if movie != None:
#         	tt = movie['tt']
#         	return redirect(url_for('update',tt = tt))
#     	flash("Movie does not exist.")
#     return render_template('search.html')
#
# @app.route('/select/', methods=['GET','POST'])
# def select():
#     conn = dbconn2.connect(DSN)
#     if request.method == 'POST':
#     	tt = request.form[('menu-tt')]
#         return redirect(url_for('update',tt = tt))
#     movies = getIncomplete(conn)
#     return render_template('select.html', movies = movies)
#
# @app.route('/update/<tt>', methods=['GET','POST'])
# def update(tt):
# 	conn = dbconn2.connect(DSN)
# 	movie = checkTT(conn, tt)
# 	#getting the right information
# 	tt = movie['tt']
# 	title = movie['title']
# 	release = movie['release']
# 	director = movie['director']
# 	addedby = movie['addedby']
# 	if request.method == 'POST':
# 		if request.form['submit'] == 'update':
# 			title = request.form[('movie-title')]
# 			tt = request.form[('movie-tt')]
# 			release = request.form[('movie-release')]
# 			director = request.form[('movie-director')]
# 			addedby = request.form[('movie-addedby')]
# 			desc = updateDB(conn, title, tt, release, director, addedby)
# 			flash(desc)
# 			return render_template('update.html', title = title, tt = tt, release = release, director = director, addedby = addedby, desc = desc)
#
# 		if request.form['submit'] == 'delete':
# 			desc = delete(conn,title)
# 			flash(desc)
# 			return render_template('home.html')
# 	return render_template('update.html', title = title, tt = tt, release = release, director = director, addedby = addedby, desc = '')




if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    DSN = dbconn2.read_cnf()
    DSN['db'] = 'dormform_db'
    app.debug = True
    app.run('0.0.0.0',port)
