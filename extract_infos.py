import extract_cni
import time
import pytesseract as pts
import cv2
import re
from datetime import datetime
from PIL import Image
import pycountry
def generateKey(code):
    resultat = 0
    facteur = (7, 3, 1)
    for (position, car) in enumerate(code):
        if car == "<":
            valeur = 0
        elif "0" <= car <= "9":
            valeur = int(car)
        elif "A" <= car <= "Z":
            valeur = ord(car)-55
        else:
            print("Caractère hors bornes")
            break
        resultat += valeur * facteur[position % 3]
    return (resultat % 10)
def checkKey(code, key):
    resultat = 0
    facteur = (7, 3, 1)
    for (position, car) in enumerate(code):
        if car == "<":
            valeur = 0
        elif "0" <= car <= "9":
            valeur = int(car)
        elif "A" <= car <= "Z":
            valeur = ord(car)-55
        else:
            break
        resultat += valeur * facteur[position % 3]
    return (resultat % 10) == key
def analyzeCard(path):
    cni = extract_cni.getCNI(cv2.imread(path))
    pts.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    cni_thresh = cv2.threshold(cv2.cvtColor(cni[0], cv2.COLOR_RGB2GRAY), 100, 255, cv2.THRESH_BINARY)
    cv2.imshow("ok", cni_thresh[1])
    cv2.waitKey(0)
    text = pts.image_to_string(Image.fromarray(cni_thresh[1]), lang="fra", config="--psm 6")
    text = text.replace("\n", "").replace(" ", "")
    match(cni[1]):
        case "new-back":
            bandeoptique = re.findall(r'IDFRA.{85}', text, re.IGNORECASE)
            if(bandeoptique != None and bandeoptique != []):
                if(type(bandeoptique)!=str):
                    bandeoptique = bandeoptique[-1]
                informations = re.findall(r'^IDFRA([A-Z0-9<]{9})([0-9]).{15}([0-9]{6})([0-9])([FM])([0-9]{6})([0-9])([A-Z]{3}).{11}([0-9])([A-Z<]{30})$', bandeoptique, re.IGNORECASE)
                if (informations!=None and informations!=[]):
                    informations = informations[0] # Getting the tuple which contains the informations / Récupération du n-uplet qui contient les informations
                    if(len(informations[9].rstrip("<<").split("<<"))==2):
                        nom, prenoms = informations[9].rstrip("<<").split("<<") # last name, first names
                        nom = ' '.join(filter(None, nom.split("<")))
                        prenoms = ','.join(filter(None, prenoms.split("<")))
                        if(prenoms!=[]):
                            date_naissance = datetime.strptime(informations[2], "%y%m%d").strftime("%d/%m/%y") # Birthdate
                            date_expiration = datetime.strptime(informations[5], "%y%m%d").strftime("%d/%m/%y") # ID card expiry date
                            sexe = informations[4] # Gender
                            nationalite = pycountry.countries.get(alpha_3=informations[7]) # Nationality
                            if(not(checkKey(informations[0], int(informations[1])) and checkKey(informations[2], int(informations[3])) and checkKey(informations[5], int(informations[6]))and checkKey(informations[0]+informations[1]+informations[2]+informations[3]+informations[5]+informations[6], int(informations[8])))):
                                print("THIS CARD IS A FAKE CARD")
                                return 1
                                
                            else: 
                                print({
                                        "nom":nom,
                                        "prenoms":prenoms,
                                        "date de naissance":date_naissance,
                                        "date d'expiration":date_expiration,
                                        "nationalite":nationalite.name,
                                        "sexe":sexe,
                                        "n°":informations[0]
                                })
                                return 0


            print("THIS CARD IS A FAKE CORD")
            return 1
            
        case "old":
            bandeoptique = re.findall(r'IDFRA.{67}', text, re.IGNORECASE)
            if(bandeoptique != None and bandeoptique != []):
                if(type(bandeoptique)!=str):
                    bandeoptique = bandeoptique[-1]
                #bandeoptique = "IDFRABERTHIER<D<ARDI<DE<LA<POC<<<<<<8806923102858CORINNE<<LO<<A6512068F6"
                informations = re.findall(r'^(IDFRA([A-Z<]{25})[A-Z0-9-<]{6}(([0-9]{2})([0-9]{2})([A-Z0-9-]{3})[0-9]{5})([0-9])([A-Z<-]{14})([0-9]{6})([0-9])([FM]))([0-9])$', bandeoptique, re.IGNORECASE)
                if (informations!=None):
                    informations = informations[0] # Getting the tuple which contains the informations / Récupération du n-uplet qui contient les informations
                    departement = 0
                    date_delivrance = datetime.strptime(informations[3]+"/"+informations[4], "%y/%m") # Date of issue of card
                    # https://www.legifrance.gouv.fr/loda/id/JORFTEXT000033318345 https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034053258 
                    # A 2016's decree has changed the 3-character code, so there are 2 possibilities / Un décret de 2016 a changé le code des 3 caractères donc il y a 2 possibilités
                    # There are a few limitations, as when reading the optical strip we only have the month and year, not the day, so the department on some cards issued in February/March 2017 will not be legible.
                    # Il y a quelques limites car en lisant la bande optique nous n'avons que le mois et l'année, pas le jour donc le département de certaines cartes délivrées en février/mars 2017 ne sera pas lisible
                    # So if the date of the issue of the card is between 02/01/17 and 04/01/17 the department may not be recognized / Donc si la date de délivrance est entre le 01/02/17 et 01/04/17 le département peut ne pas être reconnu
                    maj_departement_fevrier = ["75", "95", "92", "91", "77", "93", "94"]
                    if(date_delivrance < datetime.strptime("17/03", "%y/%m")):
                        departement = informations[5][:2]
                    elif(date_delivrance == datetime.strptime("17/03", "%y/%m") and not informations[5][:2] in maj_departement_fevrier):
                        departement = informations[5][:2]
                    elif(date_delivrance == datetime.strptime("17/03", "%y/%m") and informations[5][:2] in maj_departement_fevrier):
                        departement = int(informations[5])
                    else:
                        departement = int(informations[5])
                    sexe = informations[10] # Gender
                    date_naissance = datetime.strptime(informations[8], "%y%m%d").strftime("%d/%m/%y") # Birthdate
                    nom = ' '.join(filter(None, informations[1].replace("<<C<", "<<<").rstrip("<").split("<")))
                    prenoms = ','.join(filter(None, informations[7].rstrip("<").split("<<"))).replace("<", "-")
                    if(not(checkKey(informations[2], int(informations[6])) and checkKey(informations[8], int(informations[9])) and checkKey(informations[0], int(informations[11])))):
                        print("THIS CARD IS A FAKE CARD")
                        return 1
                        
                    else: 
                        print({
                                "nom":nom, #last name
                                "prenoms":prenoms,#first names
                                "date de naissance":date_naissance,#birthdate
                                "departement":departement,#department
                                "sexe":sexe,#gender
                                "n°":informations[2]
                        })
                        return 0
starttime = int(round(time.time() * 1000))
analyzeCard("test-new-back.png")
print("The program runned during "+str(int(round(time.time() * 1000))-starttime))             