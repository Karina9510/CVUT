def Ulozit(naz_soubor,data):
    with open(naz_soubor,"w") as file:
        file.write(data)
        file.close()
#Pridani do existujiciho file
def Pridat(naz_soubor,data):
    with open(naz_soubor,"a") as file:
        file.write(data)
        file.close()
#Vytvareni datoveho balicku
def VytvorData(MSA_indexSpodni,MSA_indexVrchni, hl7data):
    novadata=''
    for index,x in enumerate(hl7data):
        if index>=MSA_indexSpodni and MSA_indexSpodni==0 and index<=MSA_indexVrchni:
         novadata+=str(hl7data[index])
         novadata+="\n"
        elif index>MSA_indexSpodni and index<=MSA_indexVrchni:
         novadata+=str(hl7data[index])
         novadata+="\n"
    return novadata

def oldToLOINC(data):
    remap = {
        '001000':'8867-4',
        '002000':'8616-5',
        '003000':'60962-8',
        '003001':'60963-6',
        '003002':'60964-4',
        '003003':'76058-7',
        '003004':'76057-9',
        '003005':'76056-1',
        '003009':'60965-1',
        '003010':'60966-9',
        '004001':'9279-1',
        '004073':'76172-6',
        '007000':'86904-0',
        '007001':'8889-8',
        '027000':'8310-5',
        '028000':'8310-5',
        '049000':'8510-0',
        '049001':'8498-8',
        '049002':'8504-3',
        '049006':'8920-1',
        '053000':'60986-7',
        '053001':'60987-5',
        '053002':'8591-0',
        '072007':'8921-9',
        '072049':'8921-9',
        '073000':'76526-3',
        '073001':'11557-6',
        '073003':'2026-3',
        '054000':'60998-2',
        '054001':'60997-4',
        '054002':'8400-4',
        '044000':'8480-6',
        '044001':'8462-4',
        '044002':'8478-0',
        '072044':'0000',
        '052000':'8440-0',
        '052001':'8385-7',
        '052002':'8414-5',
        '053000':'61005-5',
        '053001':'61003-0',
        '053002':'61004-8',
        '062000':'0000',
        '062001':'0000',
        '062002':'0000',
        '062003':'0000',
        '048000':'60984-2',
        '048001':'60982-6',
        '048002':'60983-4',
        '048006':'0000',
        '044006':'0000',
        '064003':'0000',
        '064000':'0000',
        '064001':'0000',
        '064002':'0000',
        '072048':'0000'
    }
    data[0][0] = remap[str(data[0][0])]
    return data

from lxml import etree
 
#Testova funkce na parserovani
def parseXML(xmlFile):
    with open(xmlFile) as fobj:
        xml = fobj.read()
    
    root = etree.fromstring(xml)
    
    for appt in root.getchildren():
        for elem in appt.getchildren():
            if not elem.text:
                text = "None"
            else:
                text = elem.text
            print(elem.tag + " => " + text)
            # try:
            #     elems = elem.getchildren()
            #     for e in elems:
            #         print(e.tag)
            # except:
            #     pass

    root.append(new_entry)
    f = open('output.xml', 'wb')
    f.write(etree.tostring(root, pretty_print=True))
    f.close()

def getLoincXML(loinc,name):
    x =  '''  <code> 
    <coding> 
      <system value="http://loinc.org"/> 
      <code value="''' + str(loinc)+ '''"/> 
      <display value="''' + str(name) +'''"/>
    </coding> 
  </code> 
    ''' 
    return x

def getValueQuantity(value,jednotka):
    x =   ''' <valueQuantity> 
    <value value="''' + str(value) + '''"/> 
    <unit value="''' + str(jednotka) + '''"/> 
    <code value="''' + str(jednotka) + '''"/> 
  </valueQuantity> '''
    return x

#Generuje FHIR na zaklade zadanych parametru
def hl7ToFHIR(ouputName,xmlFile,loinc,name,value,jednotka):
    with open(xmlFile) as fobj:
        xml = fobj.read()
    
    root = etree.fromstring(xml)
    children = root.getchildren()
    children[2].getparent().remove(children[2])

    new_entry = etree.fromstring(getLoincXML(loinc,name))
    root.insert(2,new_entry)

    new_entry = etree.fromstring(getValueQuantity(value,jednotka))
    root.append(new_entry)


    f = open(ouputName, 'wb')
    f.write(etree.tostring(root, pretty_print=True))
    f.close()

#Vycte z zalogovanycho XML jenom data ktere patreji urcitemu LOINC kodu
def getDataFromReceivedXML(xmlFile,loinc):    
    with open(xmlFile) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    newDataFound = False
    data = []
    for appt in root.getchildren():
        for elem in appt.getchildren():
            if(elem.tag == "{http://hl7.org/fhir}code"):
                els = elem.getchildren()
                els = els[0].getchildren()
                if(dict(els[1].attrib)['value'] == loinc):
                    # print(dict(els[1].attrib)['value'])
                    newDataFound = True
                else:
                    newDataFound = False
            if(elem.tag == "{http://hl7.org/fhir}valueQuantity") and newDataFound == True:
                elems = elem.getchildren()
                elems = elems[0]
                data.append(float(elems.attrib['value']))
    return data