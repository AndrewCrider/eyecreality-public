from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import config
import os
from expertai.nlapi.cloud.client import ExpertAiClient


masterEntityList = []
outputDirectory = "Roam Research (Second Brain)/Roam Import/"


def scriptPull(main_address, title):
    opts = Options()
    opts.headless = True
    assert opts.headless  # Operating in headless mode
    browser = Chrome(options=opts)
    browser.get(main_address)
    results = browser.find_elements_by_xpath("//a[@href]")
    scriptLinks = []

    for r in results:
        if(title in r.get_attribute('href')):
            print("found")
            scriptLinks.append(r.get_attribute('href'))
           


    browser2 = Chrome(options=opts)

    for sl in scriptLinks:
        browser2.get(sl)
        fullScript = browser2.find_element_by_class_name("full-script")
        fileName = sl.split('/')[-2] +"_" + sl.split('/')[-1] 
        with open(outputDirectory+'johnOliver_'+fileName+".txt", 'w+') as scriptFile:
            scriptFile.write(fullScript.text)
            scriptFile.close()
        expertAInamed_entity_recognition(fullScript.text, fileName)
    
    
def expertAInamed_entity_recognition(text, episode):
    os.environ["EAI_USERNAME"] = config.eAIUsername
    os.environ["EAI_PASSWORD"] = config.eAIPassword

    client = ExpertAiClient()
    language = 'en'
    print(len(text))

    outputString = f'{"ENTITY":{50}} {"TYPE":{10}}\n'
    for index in range(0, len(text), 5000):
        entityText = text[index: index + 5000]
        output = client.specific_resource_analysis(body={"document": {"text": entityText}}, params={'language': language, 'resource': 'entities'})
        episodeNodes = []

        # Expert.ai Entity Types:  https://docs.expert.ai/nlapi/latest/reference/entity-types/
        entity_types = ['LEN', 'ORG', 'PRD', 'WRK', 'GEO', 'GEX', 'GEA', 'COM', 'MMD']
        for entity in output.entities:
            if (entity.type_ in entity_types):
                outputString = outputString + f'{entity.lemma:{50}} {entity.type_:{10}}\n' 
                masterEntityList.append({"word" : entity.lemma, "type": entity.type_, "episode": episode.split("_")[1], "season": episode.split("_")[0]})
                
                
        
            if (entity.type_ in 'NPH' and sum(1 for c in entity.lemma if c.isupper()) >= 2):
                outputString = outputString + f'{entity.lemma:{50}} {entity.type_:{10}}\n'
                masterEntityList.append({"word" : entity.lemma, "type": entity.type_, "episode": episode.split("_")[1], "season": episode.split("_")[0]})
                

        with open(outputDirectory+'joentities_'+episode+".txt", 'w+') as scriptFile:
                scriptFile.write(outputString)
                scriptFile.close()
        
def contentToRoam():
    seasonList = []
    episodeList = []
    export = ""
    
    for x in masterEntityList:
        seasonList.append(x["season"])
        episodeList.append(x["episode"]+"/"+x["season"])
        
    print(set(seasonList))
    print(set(episodeList))    
    for s in set(seasonList):
        print(s)
        export = export + f"- # Season:: {s}\n- ## Episodes:\n"
        for e in set(episodeList):
            print(s,e)
            if s in e:
                export = export + "  - ### Episode: " + e+"\n"
                for x in masterEntityList:
                    if x["season"] == s and x["episode"] == e.split("/")[0]:

                        export = export + "    - [[" + x["word"] + "]]\n"
           

    outputFile = open(outputDirectory + "Last Week Tonight with [[John Oliver]].md", "w")
    outputFile.write(export)
    outputFile.close()       



if __name__ == "__main__":
    #scriptPull('https://subslikescript.com/series/Last_Week_Tonight_with_John_Oliver-3530232', "Last_Week_Tonight")
    scriptPull('https://subslikescript.com/series/Last_Week_Tonight_with_John_Oliver-3530232', "Election")
    contentToRoam()
    