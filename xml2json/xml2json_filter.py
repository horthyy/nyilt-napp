# ------ XML2JSON_FILTER ------
# fájlkezelőben megnyitva van prompt,
# alternatívan az xml_filter_SETTINGS.txt használható beállításhoz

CONST_NAPOK = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "? (y/n): "]
CONST_VALIDATE = [("y","n","igen","nem"), ("y","igen")]

EXPORT_AS_DATA_VAR = True
# az exportált fájl egy js, amiben egy 'data' nevű array van, abban minden elem json object
# mivel a js nem nyithat meg fájlokat, ezért egy html dokumentum head tagjébe kell belinkelni egy 'link' taggel


import json
def panic():
    input("Nyomj entert a bezáráshoz")
    print("-"*40)
    quit()

def vonal():
    print("-"*30)
vonal()
print("log:")

# lokálisan kell lennie ugyanabban a mappában
# az "xml2json.py" készíti el, alapértelmezett nevén "orarend_export.json"
filename = "orarend_export.json"

try:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
except:
    print("HIBA TÖRTÉNT A FÁJL MEGNYITÁSAKOR")
    panic()

# console filter settings
napok = []
while True:
    for i in range(5):
        while True:
            prompt = input(f"{CONST_NAPOK[i]} {CONST_NAPOK[-1]}").strip().lower()
            if prompt in CONST_VALIDATE[0]:
                break
        if prompt in CONST_VALIDATE[1]:
            napok[i] = True
        else:
            napok[i] = False
    print("-"*10)
    print("Ezek a napok lesznek törölve:")
    print("-"+", -".join([CONST_NAPOK[i] for i in range(5) if (napok[i])]))

    prompt = input("Folytatás? (ENTER): ").strip().lower()
    if prompt=="":
        break

# szűrés beállítása
hetfo = napok[0]
kedd = napok[1]
szerda = napok[2]
csutortok = napok[3]
pentek = napok[4]

# szűrés
l = len(data)
noneCounter = 0   # a filterezendo elemeket none-re irja at, vegen ki lesznek torolve


if hetfo:  
    print("HÉTFŐ...")
    for i in range(len(data)):
        if data[i] == None:
            continue
        if data[i]["day"] == "Hétfő":
            data[i] = None
            noneCounter+=1


if kedd:  
    print("KEDD...")
    for i in range(len(data)):
        if data[i] == None:
            continue
        if data[i]["day"] == "Kedd":
            data[i] = None
            noneCounter+=1


if szerda:  
    print("SZERDA...")
    for i in range(len(data)):
        if data[i] == None:
            continue
        if data[i]["day"] == "Szerda":
            data[i] = None
            noneCounter+=1

if csutortok:  
    print("CSÜTÖRTÖK...")
    for i in range(len(data)):
        if data[i] == None:
            continue
        if data[i]["day"] == "Csütörtök":
            data[i] = None
            noneCounter+=1


if pentek:  
    print("PÉNTEK...")
    for i in range(len(data)):
        if data[i] == None:
            continue
        if data[i]["day"] == "Péntek":
            data[i] = None
            noneCounter+=1

vonal()

# cleanup
for _ in range(data.count(None)):
    data.remove(None)


print(f"{l - len(data)}/{l} elem került filterezésre.")

# ugyanaz a kod ami az xml2jsonban van
try:
    export = json.dumps(data, ensure_ascii=False, indent=4).encode('utf8')
    exportFileName = 'orarend-export-filterezett.js'
    if not EXPORT_AS_DATA_VAR:
        exportFileName += 'on'
    with open(exportFileName,'w',encoding='utf-8') as f:
        if EXPORT_AS_DATA_VAR:
            f.write('data = ')
        f.write(export.decode())
        print("Szűrt JSON fájl sikeresen létrehozva.")
    vonal()
except:
    print("HIBA TÖRTÉNT A FÁJL LÉTREHOZÁSAKOR")