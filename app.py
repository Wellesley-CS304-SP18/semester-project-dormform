'''
CS304 Final Project: Dorm Form
Midori Yang, Lauren Futami and Brenda Ji
home.py
'''

#!/usr/local/bin/python2.7

import os, sys, random
import imghdr # for image upload
import MySQLdb
import dbconn2
import functions
from math import ceil
import json


from flask import Flask, render_template, make_response, request, redirect, url_for, session, send_from_directory, flash, jsonify
from werkzeug import secure_filename # for image upload
app = Flask(__name__)

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])


# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/', methods=['GET', 'POST'])
def home():
    #display all the rooms on the home page
    if request.method=='GET':
        conn = dbconn2.connect(DSN)
        dormData = functions.getDorms(conn) #get dict of dorm building names
        roomsData = functions.getDataForThumbnails(conn, functions.getRoomIDs(conn)) #get tuple of dicts of each room and corresponding url and images
        roomsDataJSON = json.dumps(roomsData)
        return render_template('home.html', dormData = dormData,
                                            numPages = ceil(len(roomsData)/float(12)),
                                            roomsData = roomsDataJSON,
                                            )

#AJAX route to return results for search query
@app.route('/searchRooms/', methods=['GET'])
def searchRooms():
    #display all the rooms that match the query on the home page
    if request.method=='GET':
        #query may have one or more arguments, must account for variable number of arguments
        #list of form field names
        allowed = 'building avgRating'.split()
        #check if request args are safe
        for key in request.args:
            if key not in allowed:
                print 'oh no'
        else:
            query = 'SELECT roomID FROM room WHERE '
            str=[]
            for key in request.args:
                if not request.args[key] == '':
                    if key=='avgRating':
                        #handle possibility of decimal ratings
                        str.append('ROUND({},0)=%s'.format(key))
                    else:
                        str.append('{}=%s'.format(key))
            query = query + ' AND '.join(str)
            #take out any empty arguments from the query parameters
            args = [x for x in request.args.values() if x!='']
            print 'original query: ', query
            conn = dbconn2.connect(DSN)
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute(query, args)
            results = curs.fetchall()
            roomsData = functions.getDataForThumbnails(conn, results)
            return jsonify(roomsData);

@app.route('/newReview/', methods=["GET", "POST"])
def newReview():
    conn = dbconn2.connect(DSN)
    username = 'bji'
    roomIDs = functions.getRoomNums(conn);
    if username is not None:
        if request.method == "GET":
            return render_template('reviewForm.html', roomIDs = roomIDs)
        else: # POST
            chosenRoomID = request.form['roomIDs']
            flooring = request.form['flooring']
            review = request.form['review']
            rating = request.form['overallRating']
            firstReview = functions.checkFirstReview(conn, username, chosenRoomID)

            # Leave a new review
            if len(firstReview) == 0:
                # inserts new review for the room and updates the average rating
                functions.newReview(conn, username, chosenRoomID, review, rating, flooring)
                functions.updateAverageRating(conn, chosenRoomID)
                flash("Thanks for your review!")
            else:
                flash("You have already reviewed this room. Please choose another room to review.")

            # FILE UPLOAD
            print "about to do file upload"
            print "current working directory #1: " + os.getcwd()
            print "trying to get the reviewID..."
            reviewID = functions.getReviewID(conn,username,chosenRoomID)
            # reviewID = str(reviewID['reviewID'])
            # print "reviewID: " + reviewID
            # print "reviewID dict: " + reviewID['reviewID']
            print "reviewID"
            print reviewID
            print "reviewID['reviewID']"
            print reviewID['reviewID']
            print "end of reviewID attempt..."
            try:
                f = request.files['pic']
                mime_type = imghdr.what(f.stream)


                if mime_type != 'jpeg':
                    raise Exception('Not a JPEG')

                filename = secure_filename(str(reviewID['reviewID'])+str(username)+'.jpeg')
                pathname = 'static/images/'+filename
                f.save(pathname)

                functions.insertPicName(conn,filename,reviewID['reviewID'],chosenRoomID)
                flash('Upload successful')
                # return render_template('form.html',
                #                    src=url_for('pic',fname=filename),
                #                    nm=nm)

            except Exception as err:
                flash('Upload failed {why}'.format(why=err))
                # return render_template('form.html',src='',nm='')
            # END FILE UPLOAD


            return render_template('reviewForm.html', roomIDs=roomIDs)
    else: # if there's no username found yet, logins not implemented yet
        flash("No userid; please login first.")
        return render_template('login.html')

@app.route('/room/<roomID>', methods=["GET", "POST"])
def room(roomID):
    conn = dbconn2.connect(DSN)
    # if GET
    # just post all of the reviews for DAV265
    if request.method == "GET":
        reviews = functions.getRoomReviews(conn, roomID)
        pictures = functions.getPicsForReviews(conn, roomID)
        return render_template('room.html',roomID=roomID,reviews=reviews,pictures=pictures)

    # if POST
    # find the reviews for the room and display them
    else:
    	reviews = functions.getRoomReviews(conn, roomID)
    	return render_template('room.html',roomID=roomID,reviews=reviews)

# Displays reviews that a user has already made
@app.route('/reviewedRooms/', methods=["GET", "POST"])
def reviewedRooms():
    conn = dbconn2.connect(DSN)
    # username = request.cookies.get('username')
    username = 'bji'
    print username
    if username is not None:
        reviews = functions.getUserRoomReviews(conn, username)
        return render_template('reviewedRooms.html', reviews=reviews, username=username)
    else: # if there's no username found yet
        flash("No userid; please login first.")
        return render_template('login.html')

# Displays form for a review on a specific room that the user has already made
@app.route('/editRoom/<roomID>', methods=["GET", "POST"])
def editRoom(roomID):
    conn = dbconn2.connect(DSN)
    # username = request.cookies.get('username')
    username = 'bji'
    print username
    building = functions.getReshall(roomID[:3])
    roomNum = roomID[3:6]
    review = functions.getReview(conn, roomID)
    review = review[0]['review']
    roomIDs = functions.getRoomNums(conn);
    if username is not None:
        if request.method == "GET":
            print("get method!")
            return render_template("editForm.html", roomID=roomID, building=building, roomNum=roomNum, userreview=review)

        else: # POST
            print("post method!")
            flooring = request.form['flooring']
            review = request.form['review']
            rating = request.form['overallRating']
            print flooring
            print review
            print rating
            functions.updateReview(conn, username, roomID, review, rating, flooring)
            flash('Thanks for your review! The database has been updated.')
            return redirect(url_for('reviewedRooms', roomIDs=roomIDs))
    else: # if there's no username found yet
        flash("No userid; please login first.")
        return render_template('login.html')

#!/usr/local/bin/python2.7




#
# # for image upload
# @app.route('/upload', methods=["GET", "POST"])
# def file_upload():
#     if request.method == 'GET':
#         return render_template('form.html',src='',nm='')
#     else:
#         try:
#             nm = int(request.form['nm']) # may throw error
#             f = request.files['pic']
#             mime_type = imghdr.what(f.stream)
#             if mime_type != 'jpeg':
#                 raise Exception('Not a JPEG')
#             filename = secure_filename(str(nm)+'.jpeg')
#
#             basedir = os.path.abspath(os.path.dirname(_file_))
#             file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
#
#             pathname = 'images/'+filename
#             f.save(pathname)
#             flash('Upload successful')
#             return render_template('form.html',
#                                    src=url_for('pic',fname=filename),
#                                    nm=nm)
#
#         except Exception as err:
#             flash('Upload failed {why}'.format(why=err))
#             return render_template('form.html',src='',nm='')
#
# @app.route('/pic/<fname>')
# def pic(fname):
#     f = secure_filename(fname)
#     return send_from_directory('images',f)



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
    app.run('0.0.0.0',8001)
    #app.debug = True
    #app.run('0.0.0.0',os.getuid()+1)
