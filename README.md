# CVUT
1. úloha - Strandardy a komunikace ve zdravotnictví

Soubor script.py pracuje se spravy pro HL7, odstranuje nezadouci znaky, urcuje integritu zpravy a vykresluje parametry do plotu.
Soubor scriptLoinc.py vymenuje proprietarni kody za loinc kody. Vykresluje vybrany parameter do plotu.
ServertTransmitter-ClientReceiver a serverReceiver-clientTransmitter jsou pary k komunikaci klient-server.

Reciever se pripoji na port, posle 'V' pokud chce data ve formatu HL7 V2, nebo 'F' pokud chce FHIR. Pak zacne cist data a ukladat je do 
souboru (txt pro HL7 V2 nebo xml pro FHIR). Nasledne muze vykreslit nejaky parametr z zalogovaneho xml souboru dle loinc kodu.
Transmitter odpovi na prijaty požadavek a odesle potrebna data.

