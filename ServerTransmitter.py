import socket               # Import socket module
import hl7
from functions import hl7ToFHIR

s = socket.socket()         # Create a socket object

host = socket.gethostname() # Get local machine name
port = 1304 

print ("host:", host)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, port)
s.bind((host, port))        # Bind to the port
s.settimeout(10)
s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()        # Establish connection with client.
print ('Got connection from', addr)
print ("Receiving...")
protocol = c.recv(3)
c.settimeout(6)

if(protocol == 'V'.encode()):
    print("Sending in HL7 V2 protocol")
    f = open('2011034.txt','rb')
    l = f.read(1024)
    while (l):
        print ('Sending...')
        c.send(l)
        l = f.read(1024)
    f.close()
else:
    print("Sending in HL7 FHIR protocol")
    b=open('2011034.txt','r')
    pacient_data=" "
    for line in b:
        for index,ch in enumerate(line):
            pacient_data+=str(ch)
    
    pacient_data=pacient_data[1:]#pro odstraneni prvni mezery
    pacient_data=pacient_data.replace("\n","\r")
    
    h=hl7.parse(pacient_data)	

    for segment in h.segments("OBX"):
        hl7ToFHIR("output.xml","example.xml",segment[3][0][0],segment[3][0][1],segment[5],segment[6])
        f = open('output.xml','rb')
        print ('Sending...')
        l = f.read(1024)
        while (l):
            print ('Sending...1')
            c.send(l)
            l = f.read(1024)
        f.close()

print ("Done Sending")
print ("Response received from client : ", str(c.recv(1024)))

s.detach() 
s.close()