Post-Its
========
Design brief and description of program 
---
The idea is to mount a Raspberry Pi with a webcam at a fixed location in front of a physical taskboard. It should periodically scan the physical taskboard and using post-it image recognition, make the appropriate Jira API calls to make the appropriate changes to the representation of the Jira issues.

This software was designed to run on a Raspberry Pi with Raspbian and uses a Raspberry Pi Camera module. The software communicates with a [Jira] (https://www.atlassian.com/software/jira) project and [Jira Agile] (https://www.atlassian.com/software/jira/agile)

When the program runs, it first checks to see if there is something blocking the board. It does this by counting the number of yellow dots. The yellow dots mark the corners of the columns. (see Post-Its/pics for examples). Below is an example of a blank board ![Sample blank board](/pics/pic1-board.jpg)
It then compares that to the amount of dots there should be according to the number of columns specified. It also takes two pictures with a time delay and compares them for any significant changes. 

One of the pictures that was taken is then processed, and all the individual post-its are then cropped and stored. The cropped post-its are then compared to the previous set of post-its and if any changes are detected, the necessary API calls are made and a post-it is then created, moved or removed from Jira.

**Note** The software is only compatible with blue, green, pink and purple post-its

Hardware Required
---
- [Raspberry Pi Model B] (http://www.raspberrypi.org/) with [Raspbian] (http://www.raspberrypi.org/downloads) installed
- [Raspberry Pi Camera Module] (http://www.raspberrypi.org/faqs#camera) 
  
  For setting up the camera see: http://www.raspberrypi.org/technical-help-and-resource-documents -> Camera Documentation

Getting started
---
The following need to be installed

- [OpenCV](http://opencv.org/) version 2.3.1

Set up
--
- Copy the content from the git onto the Pi into the directory /home/pi/Scott `cd /home/pi/Scott && git clone https://github.com/scolem/Post-Its`
- Open Post-Its/pi/config.json and make the necessary changes to the file. See below for more details on each field.
- Set up crontab:
  - Simply run `python /home/pi/Scott/Post-Its/setup/addToCron.py`
 
  OR
  
  - On the Pi, run: `crontab -e`  
  - At the bottom of the file type `*/5 * * * * python /home/pi/Scott/Post-Its/pi/runThis.py >>/tmp/out.txt 2>&1` 
- On the physical task board, mark the corners of the columns with yellow stickers. All future post-its must be contained within these dots. See examples under Post-Its/pics/ . 
- Connect the Pi the network on which Jira is running using a LAN cable


Configuring config.json
---

- username:  The username of the user.

- password:  The password of the user

- projectKey:  The project key that data needs to be posted to  
  Can be found at Projects -> [Your Project Name]. At the top there is [Your project name] and below that, Key:[projectKey]
  
- jiraDirectory: The url of the jira server. E.g. http://172.18.0.108:2990/jira

- picDirectory:  The directory to where the files are kept. E.g. /home/pi/Post-Its/pi

- transitionIDs: The transition IDs for the workflow  
  In the form 
  
  [[col1->col2, col1->col3], [col2->col1, col2->col3], [col3->col1, col3->col2]] for three columns or 
  
  [[col1->col2, col1->col3, col1->col4], [col2->col1, col2->col3, col2->col4], [col3->col1, col1->col2, col3->col4], [col4->col1, col4->col2, col4->col3]] for four columns. 

  Can be found at: Administration -> Issues -> Workflows -> [Workflow for project] -> View. Transition IDs are the numbers in the brackets. Can be changed for more or less columns

- issueName: The type of issue that must be created  
  Can be found at: Administration -> Issues -> [Your selected issue type]. Eg. "Task".

- summary: The summary for a new post-it

- description: The description for a new post-it

- priority:  The priority for a new post-it  
  Can be found at Administration -> Issues -> Priorities. E.g. Minor.

- noCols:  Number of columns on the board

Changing the number of columns
--
- In config.json
  - Change the noCols field
  - Change the transitionIDs field

- In Jira (If not already done)
  - Add new column. When viewing the board in Agile, go to Board->Configure. Click add column and drag status to appropriate column (To add statuses, edit the appropriate workflow at Administration->Issues->Workflows)


Runtime
---
- A log is available at /tmp/out.txt
- If it all runs correctly, the pictures taken by the camera as well as the cropped pictures can be found at pi/[timestamp]
- The Jira task board will update to reflect the changes made on the physical task board
- Error checking:
  When first starting the program, there is some error checking done to see if
  - The number of yellow dots is correct
  - There is movement in front of the board. This is done by comparing two pictures taken with a few second delay and checking for any significant changes
