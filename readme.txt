Design brief:
The idea is to mount a Raspberry Pi with a webcam at a fixed location in front of a physical taskboard. It should periodically scan the physical taskboard using post it image recognision and make the appropriate Jira API calls to make the appropriate changes to the representation.

Setup:
The following instructions are for setting up the program on a pi and using the Raspberry Pi camera module.

Copy the pi folder onto the Pi.
Set up the config file by changing the neccessary fields(specific details on each field below)
Open issue.py and change the location of the config file to match your destination (about the 7th line below the license)

To set amount of columns:
Change noCols in config file
Change transitionIDs in config file
In jira: When viewing the board, Click Board->Configure. Click add column and drag status to appropriate column (To add statuses, edit the appropriate workflow at Administration->Issues->Workflows)
 
(To test: Make sure last line of timelog.txt is the same name as file containing pic.jpg. Change appropriate setting in config file, then run crop.py, followed by manage.py.)


config.json explination:
username		The username of the user
password		The password of the user
projectKey		The project key that data needs to be posted to
jiraDirectory		The url of the jira server
picDirectory		The directory to where the files are kept
transitionIDs		The transition IDs for the workflow
issueName		The type of issue that must be created
summary			The summary for a new post-it
description		The description for a new post-it
priority			The prority for a new post-it
noCols				Number of Columns on the board

ProjectKey:  Can be found at Projects -> [Your Project Name]. At the top there is [Your project name] and below that, Key:[ProjectKey]

jiraDirectory: eg http://172.18.0.108:2990/jira

picDirectory: eg C:\\Users\\Intern2\\Documents\\Issue\\ (Note the \\ not just \ in windows)
OR
\home\pi\Post-Its

transitionIDs: In the form [[col1 to col2, col1 to col3], [col2 to col1, col2 to col3], [col3 to col1, col1 to col2]]. 
Can be found at: Administration -> Issues -> Workflows -> [Workflow for project] -> View. Transition IDs are the numbers in the brackets. Can be changed for more or less columns

IssueName: Can be found at: Administration -> Issues -> [Your selected issue type]. Eg, "Task".

Priority: Can be found at Administration -> Issues -> Priorities. Eg, Minor.

