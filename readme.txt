Design brief:
The idea is to mount a Raspberry Pi with a webcam at a fixed location in front of a physical taskboard. It should periodically scan the physical taskboard using post it image recognision and make the appropriate Jira API calls to make the appropriate changes to the representation.

Setup:
...Write setup instructions here...
(Currently to run on windows: Make sure last line of timelog.txt is a file containing pic.jpg. Change appropriate setting in config file, then run crop.py, followed by manage.py.)Pi set up to follow.

config.json explination:
username		The username of the user
password		The password of the user
projectKey		The project key that data needs to be posted to
jiraDirectory		The url of the jira server
picDirectory		The directory to where the files are kept
transitionIDs		The transition IDs for the workflow
issueName		The type of issue that must be created
summary		The summary for a new post-it
description		The description for a new post-it

ProjectKey:  Can be found at Projects -> [Your Project Name]. At the top there is [Your project name] and below that, Key:[ProjectKey]

jiraDirectory: eg http://localhost:2990/jira

picDirectory: eg C:\\Users\\Intern2\\Documents\\Issue\\ (Note the \\ not just \)
OR
\home\pi\Post-Its

transitionIDs: In the form [col1 to col2, col1 to col3, col2 to col1, col2 to col3, col3 to col1, col1 to col2]. 
Can be found at: Administration -> Issues -> Workflows -> [Workflow for project] -> View. Transition IDs are the numbers in the brackets

IssueName: Can be found at: Administration -> Issues -> [Your selected issue type]. Eg, "Task".

