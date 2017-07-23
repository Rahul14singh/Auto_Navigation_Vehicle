from urllib.request import urlopen
from scp import SCPClient
from json import dumps, JSONEncoder,loads
from base64 import b64encode, b64decode
import httplib2
import base64
import json
import paramiko
import pickle
import errno
import socket
import pymysql
import requests

path=[]
pathdis=[]
pathduration=[]
direction=[]
distance=[]
apiMethod="http://"
apiVersion="/v21"
apiServer="api.weaved.com"
apiKey="WeavedDemoKey$2015"
userName = XXXX ## ENTER 
password = XXXX ## ENTER
url = 'https://maps.googleapis.com/maps/api/directions/json?'

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}


def databasepathfinder():
    params = dict(
        origin='Embedded System Training in Jaipur|Techinest', ## This is Source can Edit here
        destination='Jagatpura Fatak', ## This is Destination can Edit here
        mode='driving',
        key= XXXX, ## ENTER YOUR GOOGLE MAP DIRECTION API KEY HERE
        )

    r = requests.get(url=url,params=params)
    r=r.json()
    r=r['routes']
    r=r[0]
    r=r['legs']
    r=r[0]
    r=r['steps']
    for keys in r:
        for newkeys in keys:
            if newkeys == 'html_instructions':
                path.append(keys[newkeys])
            elif newkeys == 'distance':
                pathdis.append(keys[newkeys])
            elif newkeys == 'duration':
                pathduration.append(keys[newkeys])

    #print(path)
    #print(pathdis)

    for sec in path:
        if 'Turn <b>left</b>' in sec:
            direction.append('LEFT')
        elif 'Turn <b>right</b>' in sec:
            direction.append('RIGHT')
        else:
            direction.append('STRAIGHT')
        
    for sec in pathdis:
        distance.append(int(sec['value']))
    
    if len(direction) == len(distance):
        print('Starting Processing....')
    else:
        print('Error in api data " May be some exception "')

    i=0
    while i< len(distance):
        print( str( direction[i])+ ' ' + str(distance[i]) )
        i+=1

    db=pymysql.connect(## Enter your Database connection credentials to connect )
    cursor = db.cursor()

    print("Database Connected")

    cursor.execute("DROP TABLE IF EXISTS NAVIGATION")

    print("Current NAVIGATION Table DROPPED")

    sql = """CREATE TABLE NAVIGATION (
        SNO INT NOT NULL AUTO_INCREMENT,
        DIRECTION  CHAR(20) NOT NULL,
        DISTANCE INT NOT NULL,
        PARITY_BIT INT,
        PRIMARY KEY(SNO))"""

    cursor.execute(sql)

    sql="""ALTER TABLE NAVIGATION AUTO_INCREMENT=1"""

    cursor.execute(sql)

    print("New Table Created")

    sql=("INSERT INTO NAVIGATION"
         "(DIRECTION,DISTANCE,PARITY_BIT)"
         "VALUES(%(dir)s,%(dis)s,%(par)s)")

    i=0
    while i<len(distance):
        data={'dir':direction[i],'dis':distance[i],'par':1}
        cursor.execute(sql,data)
        i+=1

    print("Commands added in database")

    db.close()
    
def trySSHConnect(host, portNum):
    paramiko.util.log_to_file ('paramiko.log') 
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host,port=portNum,username="pi", password="raspberry")
        ssh.get_transport().window_size = 3 * 1024 * 1024
        command='python3 /home/pi/Desktop/control_gpio/initial_check.py' ## Check this address for the file on pi if it's correct or change this
        stdin,stdout,stderr = ssh.exec_command(command)
        print('\nstout:',stdout.read())
        command='python3 /home/pi/Desktop/Navigationpi.py' ## Check this address for the file on pi if it's correct or change this
        stdin,stdout,stderr = ssh.exec_command(command)
        print('\nstout:',stdout.read())
        ssh.close()
    except paramiko.AuthenticationException:
        print ("Authentication failed!")
        return -1
    except paramiko.BadHostKeyException:
        print ("BadHostKey Exception!")
        return -1
    except paramiko.SSHException:
        print ("SSH Exception!")
        ssh.close()
        return -1
    except socket.error as e:
        print ("Socket error ", e)
        return -1
    except:
        print ("Could not SSH to %s, unhandled exception" % host)
        return -1
    print ("Made connection to " + host + ":" + str(portNum))
    return 0

def proxyConnect(UID, token):
    my_ip = urlopen('http://ip.42.pl/raw').read()
    proxyConnectURL = apiMethod + apiServer + apiVersion + "/api/device/connect"

    proxyHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey,
                'token': token
            }

    proxyBody = {
                'deviceaddress': UID,
                'hostip': my_ip,
                'wait': "true"
            }

    response, content = http.request( proxyConnectURL,
                                          'POST',
                                          headers=proxyHeaders,
                                          body=dumps(proxyBody,cls=PythonObjectEncoder)
                                       )
    print ("Response = ", response)
    print ("Content = ", content)
    data = json.loads(content.decode('utf-8'))["connection"]["proxy"]
    print(data)
    URI = data.split(":")[0] + ":" + data.split(":")[1]
    URI = URI.split("://")[1]
    portNum = data.split(":")[2]
    print(URI)
    print(portNum)
    val = trySSHConnect(URI,int(portNum))
    if val==0:
        print("Yeah Check that it worked")

if __name__ == '__main__':

    databasepathfinder()

    httplib2.debuglevel     = 0
    http                    = httplib2.Http()
    content_type_header     = "application/json"


    loginURL = apiMethod + apiServer + apiVersion + "/api/user/login"

    print ("Login URL = " + loginURL)

    loginHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey
            }
    try:        
        response, content = http.request( loginURL + "/" + userName + "/" + password,
                                          'GET',
                                          headers=loginHeaders)
        
    except:
        print ("Server not found.  Possible connection problem!")
        exit()

    try:
        data = json.loads(content.decode('utf-8'))
        if(data["status"] != "true"):
            print ("Can't connect to Weaved server!")
            print (data["reason"])
            exit()

        token = data["token"]
    except KeyError:
        print ("Comnnection failed!")
        exit()
        
    print ("Token = " +  token)

    deviceListURL = apiMethod + apiServer + apiVersion + "/api/device/list/all"

    deviceListHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey,
                'token': token,
            }
            
    response, content = http.request( deviceListURL,
                                          'GET',
                                          headers=deviceListHeaders)
    print ("----------------------------------") 
    deviceData = json.loads(content.decode('utf-8'))
    print (deviceData)
    devices = deviceData['devices']
    for part in devices:
        if part['servicetitle']=='Bulk Service':
            BULKaddress=part['deviceaddress']
        elif part['servicetitle']=='HTTP':
            HTTPaddress=part['deviceaddress']
        elif part['servicetitle']=='SSH':
            SSHaddress=part['deviceaddress']
        elif part['servicetitle']=='VNC':
            VNCaddress=part['deviceaddress']
    #print(SSHaddress)
    proxyConnect(SSHaddress,token)

