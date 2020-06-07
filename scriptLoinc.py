import hl7
import os
import matplotlib.pyplot as plt 
from functions import Ulozit,Pridat,VytvorData,oldToLOINC

b=open('Test.txt','r')
pacient_data=" "
Ano=0
for line in b:
    for index,ch in enumerate(line):
        if line[index]=="M":
            if line[index+1]=="S":
                if line[index+2]=="H":
                    Ano=1        
            
        if line[index]=="R":
            if line[index+1]=="e":
                if line[index+2]=="c":
                    Ano=0
        if Ano==1:
            pacient_data+=str(ch)
            # print(ch)

pacient_data=pacient_data[1:]#pro odstraneni prvni mezery
pacient_data=pacient_data.replace("\n","\r")
h=hl7.parse(pacient_data)	

#V if je /zdali se jedna o nova data            
seznam_pacientID=[]
integritaPrvni=' '
integritaDruha=' '
integritaTrue=[]
integritaFalse=[]
integrity=[]
integrity2=0
checkPID=' '
checkForPID=' '
kontrolaDate=' '
kontrolaForDate=' '
ulozeniMSA=[0] # pridani nuly pro prvni index
#Ulozeni do promennych vcetne kontroly


for ind,x in enumerate(h):
    # print(x)    
    if ind<len(h.segments("PID")):
        if checkPID==' ':
            checkPID = h.segments("PID")[ind][3]
            seznam_pacientID.append(checkPID)
        if h.segments("PID")[ind][3] != checkPID:
            checkPID=h.segments("PID")[ind][3]
            seznam_pacientID.append(checkPID)
            PID_integrita= False #PID pacienta jine od minula (zmena)
        else:
            PID_integrita= True #Dalsi PID pacienta je stejne od minula
        #Integrita jedne zpravy
    if ind<len(h.segments("MSH")) and ind<len(h.segments("MSA")):
        if ind==0:
            integritaPrvni=h.segments("MSH")[ind][10]
            integritaDruha=h.segments("MSA")[ind][2]
            integrity.append(integritaPrvni)
        else:
            integritaPrvni=h.segments("MSH")[ind+2][10] #kvuli tomu, ze tam jsou dve MSH
            integritaDruha=h.segments("MSA")[ind][2]
            integrity.append(integritaPrvni)
        # print(integritaPrvni,integritaDruha)
        if str(integritaPrvni)==str(integritaDruha):
            integritaTrue.append("True")
            
        else:
            integritaFalse.append("False")           
    if str(h[ind])==str(h.segments("MSA")[integrity2]):
        integrity2+=1
        ulozeniMSA.append(ind)


#################Convert to LOINC and draw###########################
#Premapuje proprietarni kody na loinc. 
parametr = "VITAL HR"
data = []
time = []
for segment in h.segments("OBX"):
    segment[3] = oldToLOINC(segment[3])
    if(str(segment[3][0][1]) == parametr):
        data.append(float(segment[5][0]))
        time.append(int(segment[14][0]))
plt.plot(time,data)
plt.show()

#Ulozeni do souboru
#print(len(ulozeniMSA))
for index,i in enumerate(ulozeniMSA):
    if index<len(seznam_pacientID):
        nazev=str(seznam_pacientID[index])
        nazev+="Loinc.txt"
    
    if os.path.isfile(nazev)== True and index<len(ulozeniMSA)-1:
        Pridat(nazev,VytvorData(ulozeniMSA[index],ulozeniMSA[index+1],h))
    if os.path.isfile(nazev)== False and index<len(ulozeniMSA)-1:
        Ulozit(nazev,VytvorData(ulozeniMSA[index],ulozeniMSA[index+1],h))
