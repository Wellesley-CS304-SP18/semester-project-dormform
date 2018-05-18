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
# Adds a new user into the database if they haven't been added already 
def checkUser(conn, user):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from student where username=%s', [user])
    results = curs.fetchall()
    if len(results) == 0: 
        curs.execute('INSERT INTO student(username, password) VALUES (%s, "password")', [user])

# gets all the roomIDs in the database so far
def getRoomIDs(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT roomID from room')
    return curs.fetchall()

# get the reviewID for the file upload
def getRoomNums(conn, building):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT roomNum from room WHERE building = %s', [building])
    return curs.fetchall()

# gets the picture unique to given user's review
def getUserPic(conn, user, reviewID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT username, pictureFile, r.reviewID from review as r join picture as p on r.reviewID = p.reviewID where username = %s and r.reviewID = %s', [user, reviewID])
    return curs.fetchone()

# adds a new review for a specif room by a user 
def newReview(conn, user, roomID, review, overallRating, flooring):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    defaultType = 'single' # change later
    curs.execute('INSERT INTO review (reviewID, username, roomID, review, overallRating, flooring) VALUES (NULL, %s, %s, %s, %s, %s)', [user, roomID, review, overallRating, flooring])

# updates review from the edit form 
def updateReview(conn, user, roomID, review, overallRating, flooring):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    defaultType = 'single' # change later
    print ("UPDATE REVIEW FUNCTION: " + review)
    curs.execute('UPDATE review SET review=%s, overallRating=%s, flooring=%s WHERE roomID=%s', [review, overallRating, flooring, roomID])

# checks wheter or not this is the first review a user has written about a room
def checkFirstReview(conn, user, roomID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT * FROM review WHERE username=%s and roomID=%s',[user, roomID])
    results = curs.fetchall()
    return results

# gets reviews unique to a room 
def getRoomReviews(conn, roomID):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT * FROM review WHERE roomID=%s',[roomID])
	return curs.fetchall()

# gets reviews unique to user
def getUserRoomReviews(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT * FROM review WHERE username=%s',[username])
    return curs.fetchall()

# gets full name of residence hall based on residence hall 3-letter code
def getReshall(buildingID):
    buildings = {'BAT':'Bates', 'BEB':'Beebe', 'CAZ':'Cazenove', 'CER':'Cervantes',
    'CLA':'Claflin', 'DOW':'Dower', 'FRE':'Freeman', 'FHC':'French House', 'HEM':'Hemlock',
    'LAK':'Lake House', 'MCA':'McAfee', 'MUN':'Munger', 'POM':'Pomeroy', 'SEV':'Severance',
    'SHA':'Shafer', 'STO':'Stone', 'DAV':'Davis', 'TCE':'Tower Court East', 'TCW':'Tower Court West'}
    reshall = buildings[buildingID]
    return reshall

# gets residence hall 3-letter code based on residence hall
def getReshallID(buildingID):
    buildings = {'Bates':'BAT', 'Beebe':'BEB', 'Cazenove':'CAZ', 'Cervantes':'CER',
    'Claflin':'CLA', 'Dower':'DOW', 'Freeman':'FRE', 'French House':'FHC', 'Hemlock':'HEM',
    'Lake House':'LAK', 'McAfee':'MCA', 'Munger':'MUN', 'Pomeroy':'POM', 'Severance':'SEV',
    'Shafer':'SHA', 'Stone':'STO', 'Davis':'DAV', 'Tower Court East':'TCE', 'Tower Court West':'TCW'}
    reshall = buildings[buildingID]
    return reshall

# gets all the reshalls in the database so far 
def getUniqueReshalls(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT distinct(building) FROM room');
    return curs.fetchall()

# deletes a photo based on pictureFile 
def deletePicture(conn, picFile):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('DELETE from picture where pictureFile = %s',[picFile]);

# gets a review based on username and roomID
def getReview(conn, roomID, user):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('SELECT * FROM review WHERE roomID = %s and username = %s',[roomID, user])
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
