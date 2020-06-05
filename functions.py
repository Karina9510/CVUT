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