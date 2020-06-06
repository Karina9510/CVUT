#Client se pripoji na port, posle 'V' pokud chce data ve formatu HL7 V2, nebo 'F' pokud chce FHIR
#Pak zacne cist data a ukladat je do souboru(txt pro HL7 V2 nebo xml pro FHIR)
#Nasledne muze vykreslit nejaky parametr z zalogovaneho xml souboru dle loinc kodu. 

import socket               # Import socket module
from functions import getDataFromReceivedXML
import matplotlib.pyplot as plt

c = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1304                 # Reserve a port for your service.
print ("hostCl:", host)

c.connect((host, port))
c.settimeout(5)

####################Choosing protocol############################
####################HL7 V2           ############################
f = open('Test2.txt','wb')
print ('waiting for HL7 V2 data')
c.send('V'.encode())
l = c.recv(1024)
while (l):
    print ("Receiving...")
    f.write(l)
    try:
        l = c.recv(1024)
    except socket.timeout:
        f.close()
        print ("Done Receiving")
        c.send('Thank you for data'.encode('utf-8'))
        break

####################HL7 FHIR         ############################
# f = open('Test2.xml','wb')
# f.write("<Data>".encode('utf-8'))
# print ('waiting for HL7 V2 data')
# c.send('F'.encode())
# l = c.recv(1024)
# while (l):
#     print ("Receiving...")
#     f.write(l)
#     try:
#         l = c.recv(1024)
#     except socket.timeout:
#         print ("Done Receiving")
#         c.send('Thank you for data'.encode('utf-8'))
#         break
# f.write("</Data>".encode('utf-8'))
# f.close()

data = getDataFromReceivedXML('Test2.xml','8867-4')
plt.plot(data)
plt.show()


c.detach()
c.close() 

