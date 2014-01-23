"""
Copyright 2014

   Scott Lemmer <scottlemmer1@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

#file used to connect with jira

from subprocess import Popen
from subprocess import PIPE
import json
import string

def jsonconfig2str():#get the config file as a array

    f=open('/home/pi/Scott/Post-Its/pi/config.json', 'r')
    j=json.load(f)
    
    return j

def jsonstr2field(strData, field):#get value of specific field form json file
    j=json.loads(strData)
    
    return j[field]

def getTransitionID(col1, col2):# get the transition for the desired transition
    transList=jsonconfig2str()['transitionIDs']
##    transID='0'
##    
##    if col1=='1':
##        if col2=='2':
##            transID=transList[0]
##        elif col2=='3':
##            transID=transList[1]
##            
##    elif col1=='2':
##        if col2=='1':
##            transID=transList[2]
##        elif col2=='3':
##            transID=transList[3]
##
##    elif col1=='3':
##        if col2=='1':
##            transID=transList[4]
##        elif col2=='2':
##            transID=transList[5]

    if col2>col1:
        transID=transList[int(col1)-1][int(col2)-2]
    elif col2<col1:
        transID=transList[int(col1)-1][int(col2)-1]
    else:
        transID=0

    #print 'id'+str(transID)

    return transID

def editJSONfield(issueID, field, filename):#make changes to json file(used to set issueID)

    fread=open(filename, 'r')
    j=json.load(fread)
    j[field]=issueID

    fwrite=open(filename, 'w')
    fwrite.write(json.dumps(j))

def moveIssue(issueID, col1, col2):#move issue between columns
    print 'moving issue'
    jsonstr=jsonconfig2str()
    
    moveID=getTransitionID(col1, col2)
    
    fout=open(jsonstr['picDirectory']+"move.txt", "w")
    fout.write('{"transition": { "id": "'+str(moveID)+'"}}')
    fout.close()

    Popen('curl -u '+jsonstr['username']+':'+jsonstr['password']+' -X POST --data @'+jsonstr['picDirectory']+'\\move.txt -H "Content-Type: application/json" '+jsonstr['jiraDirectory']+'/rest/api/2/issue/'+issueID+'/transitions?expand=transitions.fields ', stdout=PIPE, shell=True).stdout.read()

def addImage(issueID, imgLink):#add image to issue
   print'adding image'
   jsonstr=jsonconfig2str()
   Popen('curl -u '+jsonstr['username']+':'+jsonstr['password']+' -X POST -H "X-Atlassian-Token: nocheck" -F "file=@'+imgLink+'" '+jsonstr['jiraDirectory']+'/rest/api/2/issue/'+issueID+'/attachments', stdout=PIPE, shell=True).stdout.read() 

    
def newIssue(picLink, col):#create new issue
    print 'creating new issue'
    jsonstr=jsonconfig2str()

    fout=open(jsonstr['picDirectory']+"new.txt", "w")
    fout.write('{"fields": {"project":{"key": "'+jsonstr["projectKey"]+'" },"summary": "'+jsonstr['summary']+'","description": "'+jsonstr['description']+'","issuetype": {"name": "'+jsonstr["issueName"]+'"},"priority": {"name": "'+jsonstr["priority"]+'"}}}')
    fout.close()
    
    line= Popen('curl -v -u '+jsonstr['username']+':'+jsonstr['password']+' -X POST --data @'+jsonstr['picDirectory']+'/new.txt -H \"Content-Type: application/json\" '+jsonstr['jiraDirectory']+'/rest/api/2/issue/', stdout=PIPE, shell=True).stdout.read()
    #print line
    
    issueID=jsonstr2field(line, "id")
    
    #add attachment
    addImage(issueID, picLink)

    #move issue
    if col != '1':
        moveIssue(issueID, '1', col)

    editJSONfield(issueID, "issueID", picLink[:-3] + 'json')

def deleteIssue(issueID):#delete issue
    print 'deleting issue'
    jsonstr=jsonconfig2str()
    Popen('curl -u '+jsonstr['username']+':'+jsonstr['password']+' -X DELETE -H "Content-Type: application/json" '+jsonstr['jiraDirectory']+'/rest/api/2/issue/' + issueID, stdout=PIPE, shell=True).stdout.read()
    

#newIssue("day1/post5.jpg", '1')
#moveIssue("POS-525", "2", "1")
#deleteIssue("POS-525")
#addImage("10259", "day1\\post2.jpg")
