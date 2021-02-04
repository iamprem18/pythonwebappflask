import ssl
from datetime import datetime
import OpenSSL
import socket
import getpass
from datetime import timedelta

from flask import Flask, render_template

app = Flask(__name__)

#Declare Dictionary and List
ssl_dict = {}
ssl_list = list()

##Opening File
ipfile=open("pythonwebappflask/server_ip.txt")
cur_date = datetime.utcnow()
expcount=0
expday=30

for ip in ipfile:
 try:
   host = ip.strip().split(":")[0]
   port = ip.strip().split(":")[1]
   ##print("\nChecking certifcate for server:",host)
   ctx = OpenSSL.SSL.Context(ssl.PROTOCOL_TLSv1)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((host, int(port)))
   cnx = OpenSSL.SSL.Connection(ctx, s)
   cnx.set_connect_state()
   cnx.do_handshake()
   cert=cnx.get_peer_certificate()
   s.close()
   server_name = cert.get_subject().commonName
   edate=cert.get_notAfter()
   edate=edate.decode()
   exp_date = datetime.strptime(edate,'%Y%m%d%H%M%SZ')
   exp = datetime.strftime(exp_date,'%d %B, %Y')
   days_to_expire = int((exp_date - cur_date).days)
   ssl_dict = {'Name' : host,'Date' : exp,'Days' : days_to_expire}
   ssl_list.append(ssl_dict)
 except:
   print ("Error on connection to Server,",host)
  
#Function to return the key on which to sort
def sortKey(e):
	return e['Days']
#Sorting the Cert as per least number of days to expire
ssl_list.sort(key=sortKey)

@app.route("/")
def home():
	return render_template("index.html",ssl_list=ssl_list)
	
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=7000,debug=True)


   
   
   
   
   
   
   
   
   
   
   
   
   
   
