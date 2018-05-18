'''
CS304 Final Project: Dorm Form
Midori Yang, Lauren Futami and Brenda Ji
app.py
'''

#!/usr/local/bin/python2.7

import os, sys, random
import imghdr # for image upload
import MySQLdb
import dbconn2
import functions
import sys 
from flask import Flask, render_template, make_response, request, redirect, url_for, session, send_from_directory, flash, jsonify
from werkzeug import secure_filename # for image upload
from flask_cas import CAS 


app = Flask(__name__)
# app.secret_key = 'your secret here'
app.secret_key = 'rosebud'

# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

CAS(app)
app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_AFTER_LOGIN'] = 'logged_in'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
# app.config['CAS_AFTER_LOGOUT'] = 'http://cs.wellesley.edu:1942/'
app.config['CAS_AFTER_LOGOUT'] = 'https://cs.wellesley.edu:1946/scott'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/logged_in/')
def logged_in():
    # flash('successfully logged in!')
    return redirect( url_for('home') )

@app.route('/logout/')
def logged_out():
    # flash('successfully logged out!')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    print 'Session keys: ',session.keys()
    for k in session.keys():
        print k,' => ',session[k]
    if '_CAS_TOKEN' in session:
        token = session['_CAS_TOKEN']
    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        print 'CAS_attributes: '
        for k in attribs:
            print '\t',k,' => ',attribs[k]
    if 'CAS_USERNAME' in session:
        is_logged_in = True
        username = session['CAS_USERNAME']
        conn = dbconn2.connect(DSN)
        functions.checkUser(conn, username)
        print('CAS_USERNAME is: ',username)

        #display all the rooms on the home page
        if request.method=='GET':
            conn = dbconn2.connect(DSN)
            roomsData = functions.getRoomIDs(conn)
            picData = functions.getPicsForThumbnails(conn)
            print picData
            return render_template('home.html', roomsData = roomsData, picData = picData, username = username)
    else:
        is_logged_in = False
        username = None
        print('CAS_USERNAME is not in the session')
        return render_template('login.html')

@app.route('/sortRooms/', methods=['GET'])
def sortRooms():
    try: 
        #display all the rooms that match the query on the home page
        username = session['CAS_USERNAME']
        print "sortRoomS: Username: " + username
        if username is not None: 
            if request.method=='GET':
                #query may have one or more arguments, must account for variable number of arguments
                query = 'SELECT roomID FROM room WHERE'
                #add corresponding column name for every query field
                for key in request.args.keys():
                    if not request.args[key] == '':
                        query = query + ' {}=%s AND'.format(key);
                query = query[:-4] #slice off the last AND
                #take out any empty arguments from the query parameters
                args = [x for x in request.args.values() if x!='']
                conn = dbconn2.connect(DSN)
                curs = conn.cursor(MySQLdb.cursors.DictCursor)
                curs.execute(query, args)
                results = curs.fetchall()
                picData = functions.getPicsForThumbnails(conn)
                #add the url and pathname with which to build the thumbnails for each room
                for result in results:
                    result['url'] = url_for('room',roomID=result['roomID'])
                    if result['roomID'] in picData:
                        result['image'] = picData[result['roomID']]
                return jsonify(results);
    except KeyError: 
        flash("No userid; please login first.")
        return render_template('login.html')

@app.route('/setAJAXRoomNums/', methods=["GET", "POST"])
def setAJAXRoomNums():
    conn = dbconn2.connect(DSN)
    building = request.args.keys()[0]
    roomNums = functions.getRoomNums(conn, building);
    return jsonify(roomNums);

@app.route('/newReview/', methods=["GET", "POST"])
def newReview():
    try: 
        username = session['CAS_USERNAME']
        print "newReview username: " + username
        if username is not None:
            conn = dbconn2.connect(DSN)
            roomIDs = functions.getRoomIDs(conn);
            reshalls = functions.getUniqueReshalls(conn);
            roomNums = range(1,10)
            if request.method == "GET":
                return render_template('reviewForm.html', roomIDs = roomIDs, reshalls=reshalls)
            else: # POST
                building = request.form['reshalls']
                roomNum = request.form['roomNums']
                print "BUILDING AND ROOM NUM: " + str(building) + str(roomNum)
                flooring = request.form['flooring']
                review = request.form['review']
                rating = request.form['overallRating']

                if (building == "none") or (roomNum == "none"): 
                    flash("Please choose a residence hall and a room number.")
                    return render_template('reviewForm.html', roomIDs = roomIDs, reshalls=reshalls)
                else: 
                    chosenRoomID = functions.getReshallID(building) + roomNum
                    print chosenRoomID
                    firstReview = functions.checkFirstReview(conn, username, chosenRoomID)

                    # Leave a new review
                    if len(firstReview) == 0:
                        
                        try:
                            # inserts new review for the room and updates the average rating
                            functions.newReview(conn, username, chosenRoomID, review, rating, flooring)
                            functions.updateAverageRating(conn, chosenRoomID)

                            reviewID = functions.getReviewID(conn,username,chosenRoomID)
                            f = request.files['pic']
                            
                            mime_type = imghdr.what(f.stream)

                            if mime_type != 'jpeg':
                                raise Exception('Not a JPEG')
                            filename = secure_filename(str(reviewID['reviewID'])+str(username)+'.jpeg')
                            pathname = 'static/images/'+filename
                            f.save(pathname)

                            functions.insertPicName(conn,filename,reviewID['reviewID'],chosenRoomID)
                            flash('Upload successful')
                            flash("Thanks for your review!")

                        except Exception as err:
                            flash('Upload failed {why}'.format(why=err))
                        # END FILE UPLOAD

                    else:
                        flash("You have already reviewed this room. Please choose another room to review.")

                    return render_template('reviewForm.html', roomIDs=roomIDs, reshalls=reshalls)
    except KeyError: # if there's no username found yet, logins not implemented yet
        flash("No userid; please login first.")
        return render_template('login.html')

@app.route('/room/<roomID>', methods=["GET", "POST"])
def room(roomID):
    try:
        username = session['CAS_USERNAME']
        print "newReview username: " + username
        if username is not None:
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
    except KeyError: # if there's no username found yet, logins not implemented yet
        flash("No userid; please login first.")
        return render_template('login.html')

# Displays reviews that a user has already made
@app.route('/reviewedRooms/', methods=["GET", "POST"])
def reviewedRooms():
    try: 
        username = session['CAS_USERNAME']
        print "reviewedRooms username: " + username
        if username is not None:
            conn = dbconn2.connect(DSN)
            reviews = functions.getUserRoomReviews(conn, username)
            # print reshall
            roomNums = [];
            return render_template('reviewedRooms.html', reviews=reviews, username=username)
    except KeyError: # if there's no username found yet
        flash("No userid; please login first.")
        return render_template('login.html')

# Displays form for a review on a specific room that the user has already made
@app.route('/editRoom/<roomID>', methods=["GET", "POST"])
def editRoom(roomID):
    try: 
        username = session['CAS_USERNAME']
        print "editRoom username: " + username
        if username is not None:
            conn = dbconn2.connect(DSN)
            building = functions.getReshall(roomID[:3])
            roomNum = roomID[3:] # the roomIDs are not inputted by the user, but selected from a drop down list or from a URL
            review = functions.getReview(conn, roomID, username)
            reviewText = review[0]['review']
            reviewID = review[0]['reviewID']
            roomIDs = functions.getRoomIDs(conn)
            picture = functions.getUserPic(conn, username, reviewID)
            if request.method == "GET":
                print("get method!")
                return render_template("editForm.html", roomID=roomID, building=building, roomNum=roomNum, userreview=reviewText, picture=picture)

            else: # POST
                if request.form['submit'] == 'Delete Photo':
                    functions.deletePicture(conn, picture['pictureFile'])
                    flash("Your photo has sucessfully been deleted")
                    picture = None
                    return render_template("editForm.html", roomID=roomID, building=building, roomNum=roomNum, userreview=reviewText, picture=picture)
                elif request.form['submit'] == 'Update Review':
                    flooring = request.form['flooring']
                    review = request.form['review']
                    rating = request.form['overallRating']
                    try:
                        # inserts new review for the room and updates the average rating
                        functions.newReview(conn, username, roomID, review, rating, flooring)
                        functions.updateAverageRating(conn, roomID)

                        reviewID = functions.getReviewID(conn,username,roomID)
                        f = request.files['pic']
                            
                        mime_type = imghdr.what(f.stream)

                        if mime_type != 'jpeg':
                            raise Exception('Not a JPEG')
                        filename = secure_filename(str(reviewID['reviewID'])+str(username)+'.jpeg')
                        pathname = 'static/images/'+filename
                        f.save(pathname)

                        functions.insertPicName(conn,filename,reviewID['reviewID'],roomID)
                        flash('Upload successful')
                        functions.updateReview(conn, username, roomID, review, rating, flooring)
                        flash('Thanks for your review! The database has been updated.')

                    except Exception as err:
                            flash('Upload failed {why}'.format(why=err))
                    
                    return redirect(url_for('reviewedRooms', roomIDs=roomIDs))
    except KeyError: # if there's no username found yet
        flash("No userid; please login first.")
        return render_template('login.html')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = 1946 #os.getuid()

    DSN = dbconn2.read_cnf()
    DSN['db'] = 'bji_db'
    app.debug = True
    app.run('0.0.0.0',port)

