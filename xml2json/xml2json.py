# ------ XML2JSON ------

EXPORT_AS_JAVASCRIPT = False  # kiterjesztés beállítása:
# false => .json , true => .js

def vonal():
    print("-"*40)
vonal()

def count_tobb(txt, *args): # tesztelés illegális fájlnév karakterekre
    for i in range(len(args)):
        if txt.count(args[i]):
            return True
    else:
        return False

def testForLevel(group): # true: "emelt szint"; false: "alap szint"
    group = group.lower()
    if bool(group.count("alap")):
        group = False
    elif bool(group.count("emelt")):
        group = True
    elif bool(group.count("e/")):
        group = True
    elif bool(group.count(" e/")):
        group = True
    else:
        group = False
    if group:
        return "emelt"
    else:
        return "alap"

def testForNyelv(group): # true, ha angol/német/orosz/francia, kulonben false
    group = group.lower()
    if bool(group.count("angol")) or bool(group.count("német")):
        return True
    elif bool(group.count("francia")) or bool(group.count("orosz")):
        return True
    else:
        return False
def findNyelvLevel(group):
    group = group.lower()
    if bool(group.count("francia")) or bool(group.count("orosz")):
        return "masodik"
    elif bool(group.count("angol 2")) or bool(group.count("német 2")):
        return "masodik"
    else:
        return "elso"

# BEÁLLÍTÁSOK
doUnicodeCheck = True  # ellenőrzi, hogy az xml dokumentum karakterkódolása UTF-8
doHanyadikNyelv = True # első, vagy második a tanult nyelv (!! NEM MŰKÖDIK !!)
doShortNames = False # a tanárok neveinek rövidítéseit is kigyűjti (FELESLEGES)
doFullRooms = False # a termek teljes neveit is kigyűjti (FELESLEGES)
# - - - - - - - - - - - -

from bs4 import BeautifulSoup
import json
import requests


filename = 'orarend_2022_23_2.xml'
try:
    prompt = input("Fájlnév: ").strip().split('.')[0]
    if (prompt=="") or count_tobb(prompt,'.',';',':','/','\\','*','(',')','{','}','<','>','[',']','='):
        raise Exception
    else:
        filename = prompt + ".xml"
except:
    print("Hibás fájlnév")
    quit()

#print(soup.prettify())

if doUnicodeCheck:
    print("Karakterkódolás ellenőrzése...")
    try:
        with open(filename,'r', encoding="utf-8") as check:
            if check.readline().count("utf-8") == 0:
                print("A fájl karakterkódolása nem megfelelő, a szövegek olvashatatlanak lehetnek.")
                if input("Kívánja folytatni? (y/n)") in ("y","Y"):
                    pass
                else:
                    print("END")
                    quit()
    except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError):
        print("KARAKTERKÓDOLÁSI HIBA")
        quit()
    except:
        print("ISMERETLEN HIBA TÖRTÉNT")
        quit()
    else:
        pass
else:
    print("FIGYELMEZTETÉS: A karakterkódolás ellenőrzése ki van kapcsolva.")


with open(filename,'r', encoding="utf-8") as f:  #encoding dolog
    xample = BeautifulSoup(f.read(), 'xml')

cards = xample.find_all('card')
#teachers = xample.find_all('teacher')
#subjects = xample.find_all('subject')
#classrooms = xample.find_all('classroom')
#classes = xample.find_all('class')
#groups = xample.find_all('group')
#periods = xample.find_all('period')


l = len(cards)
kinyert = [{} for _ in range(l)]

#print(xample.find_all("lesson", {"id": "*8"}))

print("Előkészületek...")
for i in range(l):
    kinyert[i]["lessonid"] = cards[i]["lessonid"]

print("Osztálytermek...")
for i in range(l):
    temp = cards[i]
    kinyert[i]["room"] = xample.find("classroom", {"id": temp["classroomids"]})["short"]
    kinyert[i]["roomFull"] = xample.find("classroom", {"id": cards[i]["classroomids"]})["name"]

print("Óraszámok...")
for i in range(l):
    kinyert[i]["period"] = cards[i]["period"]

print("Időpontok...")
for i in range(l):
    temp = cards[i]
    kinyert[i]["starttime"] = xample.find("period", {"period": temp["period"]})["starttime"]
    kinyert[i]["endtime"] = xample.find("period", {"period": temp["period"]})["endtime"] #lehet kesobb optimailzalni ugy hogy +45

print("Tanárok...")
for i in kinyert:
    temp = i["lessonid"]
    i["teacherid"] = xample.find("lesson", {"id": temp})["teacherids"]
    i["subject"] = xample.find("lesson", {"id": temp})["subjectid"]

print("Tanárok nevei...")
for i in kinyert:
    temp = i["teacherid"]
    i["teacher"] = xample.find("teacher", {"id": temp})["name"]

if doShortNames:
    for i in kinyert:
        temp = i["teacherid"]
        i["teacherShort"] = xample.find("teacher", {"id": temp})["short"]


print("Tantárgyak...")
for i in kinyert:
    temp = i["subject"]
    i["subject"] = xample.find("subject", {"id": temp})["name"]

print("Napok...")
for i in range(l):
    temp = cards[i]["day"]
    kinyert[i]["day"] = xample.find("day", {"day": temp})["name"]

print("Osztályok...")
for i in kinyert:
    temp = i["lessonid"]
    i["class"] = xample.find("lesson", {"id": temp})["classids"]
    if bool(i["class"].count(",")):
        i["class"] = i["class"].split(",")
        for j in range(len(i["class"])):
            i["class"][j] = xample.find("class", {"id": i["class"][j]})["name"]
    else:
        i["class"] = xample.find("class", {"id": i["class"]})["name"]
        
print("Évfolyamok...")
for i in kinyert:
    if isinstance(i["class"], list):
        i["grade"] = i["class"][0].split(".")[0]
    else:
        i["grade"] = i["class"].split(".")[0]

print("Csoportok szintjei...")
if doHanyadikNyelv:
    print("Első/második nyelv...")

for i in kinyert:
    temp = i["lessonid"]
    i["group"] = xample.find("lesson", {"id": temp})["groupids"]
    if bool(i["group"].count(",")):
        i["group"] = i["group"].split(",")
        for j in range(len(i["group"])):
            i["group"][j] = xample.find("group", {"id": i["group"][j]})["name"]
        
        tempindex = i["group"][0]
        i["level"] = testForLevel(tempindex)

        if not doHanyadikNyelv: # skip mert ez egy work in progress feature
            continue

        if testForNyelv(tempindex):
            i["hanyadikNyelv"] = findNyelvLevel(tempindex)
        else:
            i["hanyadikNyelv"] = None

    else:
        i["group"] = xample.find("group", {"id": i["group"]})["name"]
        i["level"] = testForLevel(i["group"])

        if not doHanyadikNyelv:
            continue

        tempindex = i["group"]
        if testForNyelv(tempindex):
            i["hanyadikNyelv"] = findNyelvLevel(tempindex)
        else:
            i["hanyadikNyelv"] = None


        
# felesleg törlése
print("Adatfeldolgozás befejezése...")
for i in kinyert:
    del i["lessonid"]
    del i["teacherid"]

if not doFullRooms:
    for i in kinyert:
        del i["roomFull"]

print("Azonosítók...")
for i in range(len(kinyert)):
    kinyert[i]["id"] = i


print("JSON fájl enkódolása...")
export = json.dumps(kinyert, ensure_ascii=False, indent=4).encode('utf8')

# NINCS TRYCATCH
exportFileName = 'orarend_export.json'
if EXPORT_AS_JAVASCRIPT:
    exportFileName = 'orarend_export.js'

with open(exportFileName,'w',encoding='utf-8') as f:
    f.write(export.decode())
    print("JSON fájl sikeresen exportálva.")

print("END")



#print(len(xample.find_all('card')))
#print(len(xample.find_all('lesson')))


vonal()