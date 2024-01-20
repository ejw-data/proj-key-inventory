## Upcoming Features
- Deployable to the Cloud
    *  Deployed on Google Cloud Platform with an App Engine (serverless) - everything works except for a package conflict with Flask-Login  
    *  May deploy to AWS, IBM and Heroku to compare the platforms ease of use
    *  Created requirements.txt file for Python environment

- Messaging System
    *  Basic messaging is already available but could be upgraded to give more customized messages and a log of historical messages for each transaction  
    *  Messaging will use Flask flash messaging with category filters to create a better functioning interface  
    *  Ideally, each request will be hyperlinked to a popup box that displays the message history for that request

- Refactor and Improve Logic for Managing Keys
    *  Some test cases do not work for if keys have been lost, broken, or returned.  
    *  Prior to implementing these logic changes, I will refactor the code to make the updates easier and more readable.  
    *  Refactor code by moving queries to query.py and disperse code via functions

- User Interface Improvment
    *  Add image upload option per user
    *  Use font awesome instead of svgs for icons to simplify interface development

    ## Longterm Development Goals
- Priority Goals
    *  Add unit testing and starting dataset
    *  Add splinter synthetic monitoring and error handling that is logged
    *  Create user logs and monitor cloud performance
    *  Add form logical tests - actions to take if the form is not completely filled out (simple logic already applied)
    *  Analyze query performance
    *  Add repo formatting and linting checks on local commit and remote push
    
- Stretch Goals
    *  Create app with problem reporting section - report broken doors/locks, report access issues (scanner not working), room plaque updates 
    *  Create mobile app interface that would allow QR code scanning in request and problem reporting (QR would be on each door plaque)