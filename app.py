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

from flask import Flask, render_template, make_response, request, redirect, url_for, session, send_from_directory, flash, jsonify
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
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT roomID FROM room')
        roomsData = curs.fetchall()
        return render_template('home.html', roomsData = roomsData)

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
            if len(firstReview) == 0: # Leave a new review
                functions.newReview(conn, username, chosenRoomID, review, rating, flooring)
                flash("Thanks for your review!")
            else: # Need to edit a review --> not sure how to do this yet.
                # oldReview = functions.getOldReview(conn, username, roomID)
                # prevReview = oldReview['review']
                # return(conn, roomID)
                flash("You have already reviewed this room. Please choose another room to review.")
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
        return render_template('room.html',roomID=roomID,reviews=reviews)

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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()

    DSN = dbconn2.read_cnf()
    DSN['db'] = 'bji_db'
    app.debug = True
    app.run('0.0.0.0',port)
    #app.debug = True
    #app.run('0.0.0.0',os.getuid()+1)
