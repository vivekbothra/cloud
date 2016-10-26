from pymongo import MongoClient
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import gridfs
import sys
import mimetypes
import requests
#from PIL import Image
import base64
import os
import datetime
import pymongo
currentuser='fred'

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def firstpage():
     return render_template('login.html')
	
@app.route("/checking", methods=['GET','POST'])
def checking():
	username=request.args['username']
	password=request.args['password']
	from pymongo import MongoClient
	client = MongoClient('107.178.215.106:27017')
	db = client.myFirstMB
	cursor=db.users.find({"username": username,"password": password},no_cursor_timeout=True)
	
	return redirect(url_for('secondpage',username=username))
	

    
	

	
@app.route("/selectiononetime", methods=['GET'])
def secondpageonetime():
	if request.method == 'GET': 
		global currentuser
		currentuser=request.args['username']
		return render_template('selection.html')

	
@app.route("/selection", methods=['GET'])
def secondpage():
	if request.method == 'GET': 
		global currentuser
		currentuser=request.args['username']
		return render_template('selection.html')
		
@app.route("/selectedshown")
def thirdpage():	
	#if request.method == 'GET': 
		selection=request.args['selection']
		print selection
		if selection=='upload':
			return render_template('whattoupload.html')
		if selection=='setsubjectorpriority':
			return render_template('picornote.html')
		
@app.route("/extractpicornoteoption")
def extractpicornoteoption():	
		global picornote
		picornote=request.args['picornote']
		print picornote
		return render_template('whattodowithpicornote.html')

		
global picdata
picdata=[]
global time
time=[]
global counterarray
counterarray=[]
global notedata
notedata=[]
@app.route("/dowithpicornote")
def dowithpicornote():	
		global currentuser
		global picornote
		whattodoselection=request.args['whattodoselection']
		print picornote
		print whattodoselection
		if whattodoselection=='set':
			filename=request.args['filename']
			priority=request.args['priority']
			subject=request.args['subject']
			picornoteinner=request.args['picornoteinner']
			client = MongoClient('107.178.215.106:27017')
			db = client.myFirstMB
			db.fs.files.update_many({'user': currentuser,'type':picornoteinner,'filename':filename}, {'$set':{'priority': priority,'subject':subject}})
			
			print currentuser
			print picornoteinner
			print filename
			return 'updated'
		
		if whattodoselection=='sort':
			picornoteinner=request.args['picornoteinner']
			if picornoteinner=='asinglepicture':
				sort=request.args['sort']
				client = MongoClient('107.178.215.106:27017')
				db = client.myFirstMB
				#cursor=db.users.find()
				fs = gridfs.GridFS( db )
			
				global picdata
				global time
				global counterarray
				global counter
				counter=0
				del picdata[:]
				del time[:]
				del counterarray[:]
				for se in db.fs.files.find({ 'type': 'asinglepicture' }).sort([(sort, pymongo.DESCENDING)]):
					data=fs.get(se['_id']).read()
					time1=(se[sort])
				
					picdata.append("data:image/jpeg;base64," + base64.b64encode(data))
					time.append(time1)
				
					counterarray.append(counter)
					counter=counter+1
				
				return render_template('feed.html',picdata=picdata,time=time,counterarray=counterarray)
			if picornoteinner=='note':
				sort=request.args['sort']
				client = MongoClient('107.178.215.106:27017')
				db = client.myFirstMB
				#cursor=db.users.find()
				fs = gridfs.GridFS( db )
			
				global notedata
				global time
				global counterarray
				global counter
				counter=0
				del notedata[:]
				del time[:]
				del counterarray[:]
				for se in db.fs.files.find({ 'type': 'note' }).sort([(sort, pymongo.DESCENDING)]):
					data=fs.get(se['_id']).read()
					time1=(se[sort])
					
					notedata.append((data))
					time.append(time1)
				
					counterarray.append(counter)
					counter=counter+1
				
				return render_template('feednote.html',notedata=notedata,time=time,counterarray=counterarray)
				
				
				
		
@app.route("/extractinfo", methods=['GET','POST'])
def extractinfo():	
		print request.method 
		global filetoupload,selection,subject,priority,type,filename
		filetoupload=request.files['browse']
		filename=request.form.get('filename')
		print filetoupload
		print '----------------------------------------------------------------------------------------------------------------------'
		
		print 'som'
		subject=request.form.get('subject')
		print '3'
		selection=request.form.get('selection')
		print '3'
		priority=request.form.get('priority')
		print '3'
		print selection
		if selection=='note':
			type='note'
			global currentuser,filetoupload,selection,subject,priority,type,filename
	
			client = MongoClient('107.178.215.106:27017')
			db = client.myFirstMB
			db = MongoClient().myFirstMB
			fs = gridfs.GridFS( db )
		
			x=filetoupload.read()
			
			print sys.getsizeof(x)
			count= db.fs.files.find({"user": currentuser}).count()
			print count
			if count>=10:
				print 'too many notes submitted for this user'
				return 'too many notes submitted for this user'
			if sys.getsizeof(x)>=10000000:
				print 'note too big'
				return 'note too big'
			else:
				fileID = fs.put(  x,type=type,subject=subject,priority=priority,user=currentuser,filename=filename)
				print 'uploading note done' 
				return 'uploading note done'
			
		if selection=='asinglepicture':
			type='asinglepicture'
			global currentuser,filetoupload,selection,subject,priority,type,filename
	
			client = MongoClient('localhost:27017')
			db = client.myFirstMB
			db = MongoClient().myFirstMB
			fs = gridfs.GridFS( db )
		
			x=filetoupload.read()
			print filename
			print sys.getsizeof(x)
			count= db.fs.files.find({"user": currentuser}).count()
			print count
			if count>=10:
				print 'too many pics submitted for this user'
				return 'too many pics submitted for this user'
			if sys.getsizeof(x)>=10000000:
				print 'pic too big'
				return 'pic too big'
			else:
				fileID = fs.put(  x,type=type,subject=subject,priority=priority,user=currentuser,filename=filename)
				print 'uploading picture done' 
				return 'uploading picture done'
		
			
			

		
		



if __name__ == "__main__":

	start=datetime.datetime.now()
	
	end=datetime.datetime.now()
	print str(end-start)
	app.run(host= '0.0.0.0')
	





    
