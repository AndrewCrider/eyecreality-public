import csv
import json
from datetime import datetime

sourceFileName = 'Roam Research (Second Brain)/huluoutput.csv'
outputDirectory = "Roam Research (Second Brain)/roamImport/"

# Creating a Class here so I can include other Services in the Future
def huluExtract():
    seriesNames = []
    service = 'Hulu'
    with open(sourceFileName, newline='') as huluCSV:
        reader = csv.DictReader(huluCSV)
        for row in reader:
            if row["Series Name"] not in seriesNames and row["Series Name"] != '': seriesNames.append(row["Series Name"])
        
        huluCSV.close()
        print(len(seriesNames))
        

    with open(sourceFileName, newline='') as ehuluCSV: 
        ereader =   csv.DictReader(ehuluCSV) 
        print(seriesNames)
        
        for s in seriesNames:
            ereader =   csv.DictReader(ehuluCSV)
            ehuluCSV.seek(0)
            episodes = []
            for row in ereader:
                if s == row["Series Name"]:
                    #My CSV Creation had a weird character in the EpisodeName Header Name, just left it so that it would be easier to import
                    episodes.append({"season": row["Season"],"episode": row['\ufeffEpisode Name'], "lwd" : custom_strftime('[[%B {S}, %Y]] %H:%M', datetime.strptime(row["Last Played At"], '%d %b %Y %H:%M:%S'))})
            
            contentToRoam(service, s, episodes)
          
#Creating a Callable Function for other services
def contentToRoam(service, seriesName, episodes):
    export = f"- Service:: {service}\n- ## Episodes:\n"
    for e in episodes:
        export = export + f"    - **Season {e['season']}** - {e['episode']} \n        - Last Watched - {e['lwd']}\n"

    outputFile = open(outputDirectory+seriesName+".md", "w")
    outputFile.write(export)
    outputFile.close()

        
# Needed Files for Date Format for Roam
def suffix(d):
    return 'th' if 11<=d<=13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

huluExtract()