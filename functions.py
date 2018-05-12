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

