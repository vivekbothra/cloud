from pymongo import MongoClient
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import gridfs
import os
import mimetypes
import requests
from PIL import Image
import base64
import os
import datetime

currentuser='fred'

app = Flask(__name__)
def get_db():
    from pymongo import MongoClient
    client = MongoClient('107.178.215.106:27017')
    db = client.myFirstMB
    return db

def add_users(db):
    db.users.insert({"user_id" : "user1","comment" : "LOL"})
    db.users.insert({"user_id" : "user2","comment" : "LOL"})
    db.users.insert({"user_id" : "user3","comment" : "LOL"})
    db.users.insert({"user_id" : "user4","comment" : "LOL"})
    db.users.insert({"user_id" : "user5","comment" : "LOL"})
    
def get_users(db):
    return db.users.find_one()

	
	
	


	
	


	
@app.route("/", methods=['GET','POST'])
def firstpage():
	return render_template('login.html')
	
@app.route("/selectiononetime", methods=['GET'])
def secondpageonetime():
	if request.method == 'GET': 
		global currentuser
		currentuser=request.args['username']
		return render_template('selection.html')

	
@app.route("/selection", methods=['GET'])
def secondpage():
	if request.method == 'GET': 
		return render_template('selection.html')
		
@app.route("/selectedshown")
def thirdpage():	
	#if request.method == 'GET': 
		selection=request.args['selection']
		print selection
		if selection=='upload':
			return render_template('upload.html')
		if selection=='deletemypics':
			return render_template('delete.html')
		if selection=='seeotherspics':
			return render_template('seeotherspics.html')
			
			
@app.route("/doupload", methods=['GET'])
def fifthpage():
	global currentuser
	filetoupload=request.args['browse']
	comment=request.args['comment']
	client = MongoClient('107.178.215.106:27017')
	filesize =os.path.getsize( filetoupload )
	print 'file size is'+ str(filesize)
	if filesize>100000:
		print 'filesize exceeded'
		return redirect(url_for('secondpage'))
	
	db = client.myFirstMB
	count=db.fs.files.find({"owner": currentuser}).count()
	print 'count is '+str(count)
	if count<=10:
		db = MongoClient().myFirstMB
		fs = gridfs.GridFS( db )
		modifiedcomment=str(currentuser)+':'+comment
		fileID = fs.put( open( filetoupload),filename=filetoupload,comment=modifiedcomment,owner=currentuser)
		print 'uploading done'
		return redirect(url_for('secondpage'))
	else:
		print 'user quota exceeded'
		return redirect(url_for('secondpage'))
		
		
@app.route("/deletemypics")
def deletemypics():
	global currentuser
	filetodelete=request.args['filetodelete']
	db = MongoClient().myFirstMB
	fs = gridfs.GridFS( db )
	for grid_out in fs.find({"filename": filetodelete,"owner": currentuser},no_cursor_timeout=True):
		fs.delete(grid_out._id)

	print 'pictures deleted'
	return redirect(url_for('secondpage'))
	#return render_template('feed.html',data=images)
	
@app.route("/seeothersimage", methods=['GET'])
def seeothersimage():	
	#if request.method == 'GET': 
		global username
		username=request.args['username']
		global filename
		filename=request.args['filename']
		db = MongoClient().myFirstMB
		fs = gridfs.GridFS( db )
		for grid_out in fs.find({"filename": filename,"owner": username},no_cursor_timeout=True):
			data = fs.get(grid_out._id).read()
			cur=db.fs.files.find({"filename": filename,"owner": username},{"comment":1,"_id":0})
			for comment in cur:
				print(comment)
				break
		picdata = "data:image/jpeg;base64," + base64.b64encode(data)
		
		return render_template('feed.html',data=picdata,comment=comment)

@app.route("/updatecomment", methods=['GET'])
def updatecomment():
	global username
	global filename
	yourcomment=request.args['yourcomment']
	
	db = MongoClient().myFirstMB
	fs = gridfs.GridFS( db )
	cur=db.fs.files.find({"filename": filename,"owner": username},{"comment":1,"_id":0})
	for comment in cur:
			previouscomment=str(comment)
			break
	newcomment=previouscomment+str(username)+':'+str(yourcomment)
	print newcomment
	db.fs.files.update({"filename":filename,"owner":username},{"comment":newcomment})
	return 'comment added'
if __name__ == "__main__":

	start=datetime.datetime.now()
	db = get_db() 
   # add_users(db)
	add_users(db)
	grid_fs = gridfs.GridFS( db )	
	end=datetime.datetime.now()
	print str(end-start)
	app.run()

















