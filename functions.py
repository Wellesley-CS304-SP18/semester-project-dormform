'''
CS304 Final Project: Dorm Form
Midori Yang, Lauren Futami and Brenda Ji
functions.py
'''

# These functions do most of the work to query and update the
# room review database.

import sys
import MySQLdb
import dbconn2

# ================================================================
def getRoomNums(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT roomID from room')
    return curs.fetchall()

def newReview(conn, user, roomID, review, overallRating, flooring):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    defaultType = 'single' # change later
    curs.execute('INSERT INTO review (reviewID, username, roomID, review, overallRating, flooring) VALUES (NULL, %s, %s, %s, %s, %s)', [user, roomID, review, overallRating, flooring])

def updateReview(conn, user, roomID, review, overallRating, flooring):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    defaultType = 'single' # change later
    print ("UPDATE REVIEW FUNCTION: " + review)
    curs.execute('UPDATE review SET review=%s, overallRating=%s, flooring=%s WHERE roomID=%s', [review, overallRating, flooring, roomID])

def checkFirstReview(conn, user, roomID):
    print 'we here CHECK FIRST REVIEW'
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT * FROM review WHERE username=%s and roomID=%s',[user, roomID])
    results = curs.fetchall()
    return results

def getRoomReviews(conn, roomID):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT * FROM review WHERE roomID=%s',[roomID])
	return curs.fetchall()

def getUserRoomReviews(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT * FROM review WHERE username=%s',[username])
    return curs.fetchall()

def getReshall(buildingID):
    buildings = {'BAT':'Bates', 'BEB':'Beebe', 'CAZ':'Cazenove', 'CER':'Cervantes',
    'CLA':'Claflin', 'DOW':'Dower', 'FRE':'Freeman', 'FHC':'French House', 'HEM':'Hemlock',
    'LAK':'Lake House', 'MCA':'McAfee', 'MUN':'Munger', 'POM':'Pomeroy', 'SEV':'Severance',
    'SHA':'Shafer', 'STO':'Stone', 'DAV':'Davis', 'TCE':'Tower Court East', 'TCW':'Tower Court West'}
    reshall = buildings[buildingID]
    return reshall

def getReview(conn, roomID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT review FROM review WHERE roomID = %s',[roomID])
    return curs.fetchall()

# gets the average rating for the room
def updateAverageRating(conn, roomID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('update room set avgRating=(select avg(overallRating) from review where roomID=%s) where roomID=%s',[roomID, roomID])

# get the reviewID for the file upload
def getReviewID(conn, username, roomID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select reviewID from review where username=%s and roomID=%s',[username, roomID])
    return curs.fetchone()

# inserts the picture filename into the database
def insertPicName(conn, filename, reviewID, roomID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('insert into picture values(null,%s,%s,%s)',[filename,reviewID,roomID])

# get all pictures for a specific review
def getPicsForReviews(conn, roomID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select reviewID,pictureFile from picture where roomID=%s',[roomID])
    return curs.fetchall()

# get pathname of pictures to display for each room on the home page if the room has pictures
def getPicsForThumbnails(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select room.roomID,pictureFile from room inner join picture on room.roomID=picture.roomID')
    results = curs.fetchall()
    picData = {}
    for result in results:
        picData[result['roomID']] = 'static/images/' + result['pictureFile']
    return picData
