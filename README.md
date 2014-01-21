Post-Its
========
Design brief and description of program 
---
The idea is to mount a Raspberry Pi with a webcam at a fixed location in front of a physical taskboard. It should periodically scan the physical taskboard and using post-it image recognision, make the appropriate Jira API calls to make the appropriate changes to the representation of the Jira issues.

This software was designed on a Raspberry Pi and uses a Raspberry Pi Camera module. The software communicates with a [Jira] (https://www.atlassian.com/software/jira) project and workd best when used with [Jira Agile] (https://www.atlassian.com/software/jira/agile)

When the program runs, it first checks to see if there is something blocking the board. It does this by counting the number of yellow dots and comparing that to the amount there should be according to the number of columns specified. It also takes two pictures with a time delay and compares them for and significant changes. 

One of the pictures that were taken is then processed, and all the individual post-its are then croped and stored, and they then each get a signature. The cropped post-its are then compared to the previous set of post-its and if any changes are detected, the neccissary API calls are made and a post-it is then created, moved or removed from Jira.

**Note** The software is only compatible with blue, green, pink and purple post-its

Hardware Required
---
- [Raspberry Pi Model B] (http://www.raspberrypi.org/)
- [Raspberry Pi Camera Module] (http://www.raspberrypi.org/faqs#camera)

Getting started
---
The following need to be installed

- [OpenCV](http://google.com)
- Complete list with versions and links

Set up
--
- Copy the content of the files from the git onto the Pi
- Move config.json to ...
-
- Open .../config.json and make the neccessary changes to the file. See below for more details on each field.
- Set up cron:

  - On the Pi, run: crontab -e  
  - At the bottom of the file type */5 * * * * ... python ...(for now just run crop, then manage)
  - 
- On the physical task board, mark the corners of the columns with yellow stickers


Configuring config.json
---

- username:  The username of the user.

- password:  The password of the user

- projectKey:  The project key that data needs to be posted to  
  Can be found at Projects -> [Your Project Name]. At the top there is [Your project name] and below that, Key:[projectKey]
  
- jiraDirectory: The url of the jira server. Eg. http://172.18.0.108:2990/jira

- picDirectory:  The directory to where the files are kept. Eg. /home/pi/Post-Its/pi

- transitionIDs: The transition IDs for the workflow  
  In the form 
  
  [[col1->col2, col1->col3], [col2->col1, col2->col3], [col3->col1, col1->col2]] for three columns or 
  
  [[col1->col2, col1->col3, col1->col4], [col2->col1, col2->col3, col2->col4], [col3->col1, col1->col2, col2->col4], [col4->col1, col4->col2, col4->col3]] for four columns. 

  Can be found at: Administration -> Issues -> Workflows -> [Workflow for project] -> View. Transition IDs are the numbers in the brackets. Can be changed for more or less columns

- issueName: The type of issue that must be created  
  Can be found at: Administration -> Issues -> [Your selected issue type]. Eg. "Task".

- summary: The summary for a new post-it

- description: The description for a new post-it

- priority:  The prority for a new post-it  
  Can be found at Administration -> Issues -> Priorities. Eg, Minor.

- noCols:  Number of columns on the board

Changing the number of columns
--
- In config.json
  - Change the noCols field
  - Change the transitionIDs field

- In Jira (If not already done)
  - Add new column. When viewing the board in Agile, go to Board->Configure. Click add column and drag status to appropriate column (To add statuses, edit the appropriate workflow at Administration->Issues->Workflows)
