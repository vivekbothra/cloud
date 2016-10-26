

import os
import csv 
import psycopg2
import datetime
import random 
import redis



'''
-------------------------------------------------------------Connection to Redis and Database------------------
'''
# Making connection to redis
print 'Connecting to Redis '
mrred = redis.StrictRedis(host='mycachecluster.5l7n3d.0001.usw2.cache.amazonaws.com', port=6379	,db=0)

if mrred:
	print 'Connection made to redis'

print '----------'
print 'Connecting to database'
conn_string  = "host='tejvirsagguinstance.ckp6xozlyslu.us-west-2.rds.amazonaws.com' dbname='template1' user='postgres' password='tejvirsaggu01'"
conn = psycopg2.connect(conn_string)
	
if conn:
	print 'Connection made to DB'
cur = conn.cursor()

'''
-----------------------------------------------------------END of Block------------------------------------------------------------
'''



'''
---------------------------------------------Users file reading and table creation block--------------------------------
'''
print 'file opened'
users = open('f2.csv','rb')
users_reader = csv.reader(users)


cur.execute("DROP TABLE table_user;")
cur.execute("CREATE TABLE table_user(index serial PRIMARY KEY,username varchar, password varchar);")
print 'Table dropped and created'
for use in users_reader:
	cur.execute("INSERT INTO table_user(username,password) VALUES(%s,%s)",(use[0],use[1]))
print 'Username file updated'

conn.commit()
'''
--------------------------------------------------------------END of Block----------------------------------------------------------
'''



'''
---------------------------------------------Dataset table creation and file reading block------------------------------
'''

time_start = datetime.datetime.now()

print 'Starting dataset table creation'
fileread = open('UNPrecip(4).csv','rb')
file_reader = csv.reader(fileread)

# Using the drop table command we are letting the program to create table for the first time.
cur.execute("DROP TABLE user_table")




#Creating table according to the number of attributes there are in the file. 
cur.execute("""CREATE TABLE new_user_table(index serial PRIMARY KEY,atime varchar,latitude varchar,longtitude varchar,depth varchar,mag varchar,
	magType varchar,nst varchar,gap varchar,dmin varchar,rms varchar,net varchar,id varchar,updated varchar,place varchar,type varchar,horizontalError varchar, depthError varchar, magError varchar,
    magNst varchar, status varchar, locationSource varchar, magSource varchar)""")
print 'Table created'


line = 0
for table_attr in file_reader:
	if line == 0:
		line = 1
	else:		 
		cur.executemany("""INSERT INTO new_user_table (country,station_name,WMO_station_number,unit,jan,
			feb,mar,apr,may,june ,july,aug, sept,oct,nov,dec) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
			[(table_attr[0],table_attr[1],table_attr[2],table_attr[3],table_attr[4],table_attr[5],table_attr[6],table_attr[7],
			table_attr[8],table_attr[9],table_attr[10],table_attr[11],table_attr[12],table_attr[13],table_attr[14],table_attr[15],table_attr[16]
			,table_attr[17],table_attr[18],table_attr[19],table_attr[20])
			]
		)


time_end = datetime.datetime.now()
rem_time = (time_end-time_start) 
print rem_time

conn.commit()


'''
--------------------------------------------------Start of web interface program------------------------------------------
'''

app1 = Flask(__name__)


@app1.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST': 
		cur.execute("SELECT password FROM table_user WHERE username = %s ;",(request.form['username'],))
		if request.form['password'] == str(cur.fetchone())[3:-3]:
			print 'After confirming the method'			
			return redirect(url_for('submit'))
		else:
			return render_template('error.html')
	return render_template('login.html')

@app1.route('/submit', methods=['GET','POST'])
def submit():

	if request.method=='POST'
		query = request.form['text']

		val = query.split(" ")
		query_runtime_start = datetime.datetime.now()

		i = 0
		while i<val[2]:
			randomnum = random.uniform(val[0],val[1])
			randomnum = randomnum*8
			cur.execute("SELECT mag FROM new_user_table WHERE mag >= '%s' AND mag <= '%s' ;",(randomnum,randomnum+1.0))

		fet = cur.fetchall()	

		query_runtime_end = datetime.datetime.now()

		rem_time = (query_runtime_end-query_runtime_start)


		return redirect(url_for('display',fet=fet,rem=rem_time))	
	return render_template('submit.html')



@app1.route('/display',method=['GET','POST'])
def display():
	fet = request.args['fet']
	rem = request.args['rem']

	return render_template('display.html',fet=fet,rem=rem)

if __name__ == '__main__':
	app1.run(debug=False)

 

conn.commit()

conn.close()
'''
-------------------------------------------------End of Web interface program-------------------------------------------------------
'''

