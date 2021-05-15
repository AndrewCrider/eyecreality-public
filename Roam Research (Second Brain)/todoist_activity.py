from todoist.api import TodoistAPI
import json
import matplotlib.pyplot as plt
import config
from datetime import datetime

api = TodoistAPI(config.todoistAPI)
outputJSON = api.activity.get(page=1,limit=100)
outputDirectory = "Roam Research (Second Brain)/Roam Import/"

projects = []
dates = []
weeks_project =[]
project_counts = []
all_activity = []
complete = []


api.sync()

#Creating a Callable Function for other services
def contentToRoam(data):
    export = ""
    for d in data:
        dateFormatted = custom_strftime('[[%B {S}, %Y]]', datetime.strptime(d["date"], '%Y-%m-%d'))
        export = export + f"- {dateFormatted}\n"
        for t in d["proj_tasks"]:
            export = export + f"  - [[{t['project']}]]\n"
            for st in t["tasks"]:
                doneCheckbox = "{{DONE}}"
                export = export + f"    - {doneCheckbox} {st} \n"

    outputFile = open(outputDirectory+"Todoist Todos.md", "w")
    outputFile.write(export)
    outputFile.close()

        
# Needed Files for Date Format for Roam
def suffix(d):
    return 'th' if 11<=d<=13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


#Beginning of Code

for p in api.state['projects']:
    projName = p['name']
    # Substituting ProjectNames for More Readable Resources
    # projectSubstitition = [{"old": "OriginalProjectName", "new": "ReadableName"}, ...]
    for re in config.projectSubstitution:
        if re["old"] == projName:
            projName = re["new"]

    proj = {"id": p["id"], "name": projName}
    projects.append(proj)



for x in outputJSON["events"]:
    if x['parent_project_id'] not in weeks_project:
        weeks_project.append(x['parent_project_id'])
          
    all_activity.append({"project": x['parent_project_id'], "event_type": x['event_type'], "id": x['object_id'], "eventDate": x['event_date'][0:10], "task": x['extra_data']['content'] })
    



for ip in projects:
    added_count = 0
    updated_count = 0
    completed_count = 0
    updated_items = []
    roamImport = {}
    for aa in all_activity:
        if aa["project"] == ip["id"]:
            if aa["event_type"] == "added":
                added_count = added_count + 1
            if aa["event_type"] == "updated":
                updated_count = updated_count + 1
                updated_items.append(aa["id"])
            if aa["event_type"] == "completed":
                completed_count = completed_count + 1
                dates.append(aa["eventDate"][0:10])
                event = {"date": aa['eventDate'][0:10], "name": aa['task'], "project":aa['project'], "id": aa['id'] }
                complete.append(event)
        
        
    
    if added_count != 0 and updated_count != 0 and completed_count != 0:
        project_counts.append({"project": ip["name"], "added_items": added_count, "updated_count": updated_count, "completed_count": completed_count, "updated_items": updated_items })
    


barChartAxes =[]
barChartCompletedValues = []
barChartUniqueUpdatedCount = []
dateAxes = []
dateCompletedValues=[]


for pp in project_counts:
    barChartAxes.append(pp["project"])
    barChartCompletedValues.append(pp["completed_count"]) 
    barChartUniqueUpdatedCount.append(len(set(pp["updated_items"])))
    #print(pp["project"] + "-" + str(pp["updated_items"]) + " - " + str(len(set(pp["updated_items"]))))


fig, ax = plt.subplots()
ax.bar(barChartAxes, barChartCompletedValues, .35, label='Completed Tasks')
ax.bar(barChartAxes, barChartUniqueUpdatedCount, .35, bottom=barChartCompletedValues, label='Unique Delayed Tasks')
ax.set_title('Velocity for Week')
ax.legend

plt.savefig('Roam Research (Second Brain)/Roam Import/todoist_barchart.png')


todoExport = []
for d in sorted(set(dates)):
    print(d)
    publish =[]
    
    for p in projects:
       
        roamProject = p["name"]
        taskList = []
        for c in complete:
            
            if  p["id"] == c["project"] and c["date"] == d:
                #print("date for match is " + c["date"])
                taskList.append(c["name"])
        
        if len(taskList) > 0:
            publish.append({"project" : roamProject, "tasks": taskList})
    
    todoExport.append({"date": d, "proj_tasks" : publish})

contentToRoam(todoExport)


#print(events)

