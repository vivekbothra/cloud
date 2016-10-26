#Programmer Name : Tejvir Singh

#Cloud Computing

import os
import psycopg2
from urlparse import urlparse
import swiftclient.client as swiftclient
from swiftclient.exceptions import ClientException
import datetime
import re
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random


auth_url = "https://identity.open.softlayer.com/v3"
projectId = "0abbb256c109441698ada06ee4db49a7"
region = "dallas"
#username = "Admin_b7645d4de7d51463f9e14bb9c5791da4fc0781f1"
user_id = "b1f0cecbfbe84635b5c5624d5aa5da36"
password = "Md2u*nWhOK.vu09^"


conn = swiftclient.Connection(
	key=password,
	authurl=auth_url,
	auth_version ='3',
	os_options={"project_id":projectId,
				"user_id":user_id,
				"region_name":region}
	)


#Upload files f* to BlueMix, then show total sizes (BM files) on your screen.
org_container = "org_files_container"
bak_container = "bak_files_container"

conn.put_container(org_container)
conn.put_container(bak_container)
print "Containers successfully created"

# Files being read 


user_object = open('users','r')

user_object_file = user_object.read()

count = 0
while count <= 10:
	if re.split('\n',user_object_file):
		count = count+1


#print count
for x in range(0,count-1):
	mylist = re.split(', |\r\n',user_object_file)
	


user_name = raw_input('Enter your user_name ')

file_size_user1 = mylist[1]
file_size_user2 = (mylist[3])
file_size_user3 = (mylist[5])


value = input('Enter 1 to upload and 2 for download ')


file_name = raw_input('Enter the file name ')

new_file_name = str(file_name)+'.'+user_name
print new_file_name

file_size = os.path.getsize(file_name)

file_size_user1 = int(file_size_user1) * 1000
file_size_user2 = int(file_size_user2) * 1000
file_size_user3 = int(file_size_user3) * 1000

print file_size_user1
file_array = file_name.split('.')

if file_size < file_size_user1:
	try:
		print 'Size is Okay'
		if value == 1:
			if file_array[1]=='org':
				hello1 = open(file_name,'r')
				hello1_read = hello1.read()
				conn.put_object(org_container,file_name,hello1_read,content_type='text')
			elif file_array[1]=='bak':
				hello2 = open(file_name,'r')
				hello2_read = hello2.read()
				conn.put_object(bak_container,file_name,hello2_read,content_type='text')
				#conn.put_object(bak_container,file_name,hello2_read,content_type='text')
			
		else:
			if file_array[1]=='org':
				obj1 = conn.get_object(org_container,file_name)
				with open(file_name, 'w') as write_example1:
					write_example1.write(obj1)
			elif file_array[1]=='bak':
				obj2 = conn.get_object(bak_container,file_name)
				with open(file_name,'w') as write_example2:
					write_example2.write(obj2)		
	except Exception:
		print 'Not there'
else:
	print 'The size is larger.. Cannot upload the file.. '




def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)
#with open('example.txt', 'rb') as in_file, open('out.txt', 'wb') as out_file:
#    encrypt(in_file, out_file, 'password')
with open(file_name, 'rb') as in_file, open('decrypted_example.txt', 'wb') as out_file:
    decrypt(in_file, out_file, 'password')





@app1.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST': 
		if request.form['username'] == 'user1' and request.form['password'] == '1234':
			print "in the login method."
			cur.execute("SELECT tot_quota FROM User_Table where username = 'user1';")
			total_quota = cur.fetchone()
			print total_quota
			return render_template('home.html')		
		else: 
			if request.form['username'] == 'user2' and request.form['password'] == '2345':
				print "in the else if.. "
			return render_template('.html')
	return render_template('index.html')


# start the server with the 'run()' method
if __name__ == '__main__':
	app1.run(debug=True)



# Code ends here.




























