# proj-key-inventory

## Objective
> Create a cloud-based space management system that will automate traditional keys systems found at universities.  Often universities use a decentralized system for managing key and key card access.  Relying on a decentralized system often creates several issues such as:
    - building managers must approve all keys and maintain their own system of tracking users leading to issues when buiding managers leave or do not have time to create a quality record system
    - records are often duplicated between key shop/billing, building managers, and the manager of the space leading to inconsistencies and gaps in information
    - each building will often have different standards for documenting, disbursing, and collecting the keys
    - assessing the quality of the system can become very difficult as individual steps are not clearly demarcated  

## Summary  
This system is a self-serve web portal that allows building managers to add new people to the system by only knowing their email address.  The user can then complete the registration process and then can request access to one or multiple spaces.  The building manager will then be notified in their dashboard view of the request that they can approve or reject or message the user for information.  The manager may want to verify information from the user's profile with their records to ensure consistency with other systems like safety systems.  Upon approval, the request is then sent to the fabrication shop or key administration ofice depending on whether the key needs made or is available in inventory.  Each stage of the process, has updates so the user requesting the key can see the progress from 'Key Requested', 'Key Approved', 'Key being Fabricated', 'Key Available, Waiting for Delivery', and 'Key Ready for Pickup'.    


## Features
- User Access
    *  Login page that hashes passwords in the database
    *  Only administrators can add users but upon first login the user much generate their own password

- App Security
    *  Flask app manages security of form submissions, form validation, cookies, and access  
    *  Webpages are protected to be viewed by only logged in users and further restrictions based on user role have been placed on pages and apis.

- App Scaleability
    *  Database designed with PostgreSQL and normalized (1N, 2N, and 3N)
    *  Complicated manipulations created in PL/pgSQL
    *  Database triggers used to automate tasks 
    *  Multistep workflow built into table design
    *  SQLAlchemy used to manage queries using ORM Table methods (instead of session methods)

- App Modularity
    *  HTML tables are generated from javascript (d3.js) and apis.
    *  Order basket updates without page reloads and utilizes api that loads updated HTML for only a section of the page
    *  Site pages and api routes are separated into separate files
    *  Site templates and layouts applied
    *  Custom jinja filters created to add python functionality and make code more readable
    *  App split into multiple files for ease of tracking and updating
    *  Created standardized HTML page layouts, styles using bootstrap5

- User Interface - Custom Order Process
    *  Complete shopping basket created with flask routes and D3.js
    *  Order basket entries stored in session variables 
    *  Order menus show all options if javascript is deactivated but when active the menu's filter to show only possible selections based on prior selections.
    *  Order basket determines optimum selection of ordered items to show fewest dispersements - checks inventory of available keys, checks if key needs fabricated, checks to see if key needs added to system, checks to see if keys need returned.

- Staff Interface - Custom Views by Role
    * Dashboard
    * Admin
    * Key Shop
    * Building Manager
    
- App Development Processes
    *  Used venv as a simple virtual environment
    *  Developed application using git and task-based git branches
    *  Data governance by restricting data access
    *  Separated app into purpose-based files
    *  Applied Object Oriented design such that SQLAlchemy ORM and Flask extensions could be added in the future  

## App Value
The direct value of this app would be assessed by the time savings gained by the implementing institution but would also have indirect value by increasing data availability and consistency, institutionalizing policies across all units, improving user experience, defining and enforcing role responsibilities, disbursing improvements across all units at a fraction of the individual unit investment, and providing intuitive use such that cross-functional staff training can be implemented to reduce single source of authority (aka increasing availability of approvers even if on vacation, travel, re-assignment, or unfilled position).  

Lets assume that an institution has 200 buildings, approvimately 200 building managers, 10,000 staff and faculty, and 1,000 part-time space users (5% of 20,000 students).  In total, the 200 building managers would need to manage requests and track data of 11,000 people with approximately 20% leaving and the equivalent new people replenshing those vacancies.  This would indicate that 4,400 changes occur annually.  At first look, this would indicate that each building manager would need to to make 22 updates but in reality of the 200 building managers, only about 40 would manage large spaces with large number of users.  This would indicate each manager makes more than 110 requests.  If the request takes 10 minutes to process the data, 5 minutes to communicate instructions and updates to the requester, and 5 minute to retrieve and hand-off keys then in total, the manager spends 2,200 minutes managing keys.  It is assumed that these numbers include time spent updating documentation, auditing records, and generating reports.  

At $45 an hour, this arrives at narly a week of their time is spent on this process and nearly $1,700 invested per building manager.  Given 40 building managers then this comes out to be nearly $66,000 investment annually for just the building manager's involvment.  There are still costs associated with key fabrication and key disbursement that are not included but often require significant communication and hand-off of materials with both building managers and users.  In effect, space access could easily cost more than $100,000 annually from just a labor perspective.  

By reducing the time spent performing documentation and reporting, staff costs for this process could be cut by 50% and the time savings could be leveraged toward revenue generating processes.  If revenue generating processes have a margin of 2% and labor costs account for 30% of the service or product cost then this would generate a possible $160,000 in additional revenue and $3,300 in net income.  The true value would be cost savings ($50,000), generated profit ($3,300), and any reduced need for additional labor that would have otherwise been needed to accomplish this new goal.  The cost savings by themselves could fund approximately 33% of the new revenue cost so the investment of $160,000 is really more like an investment of $106,700 in new capital.   

## Cost of Deployment  
Deploying on AWS Cloud with redundant PostgreSQL servers would cost approximately $400 annually.  

## Data
All data used for this application was synthetically created and based on a theoretical scenario  

## Collaborators  
Currently there are no collaborators and advanced features will probably not be made available due to the potential for this app to be commercially distributed.  Please contact repo owner to request collaboration interest or access to the full source code and installation instructions.  

## Future Features
- Priority Goals
    *  Deploy to the cloud - AWS, GCP, Azure (Microsoft), IBM Cloud
    *  Add splinter synthetic monitoring and error handling that is logged
    *  Create user logs and monitor cloud performance
    *  Add unit testing and starting dataset
    *  Add form logical tests
    *  Move queries to query.py and disperse code via functions
    *  Use font awesome for icons
    *  Analyze query performance
    *  Add requirements.txt file
    *  Add repo formatting and linting checks on local commit and remote push
    *  Add messaging system
    *  Add image upload option per user
- Stretch Goals
    *  Create app with problem reporting section - report broken doors/locks, report access issues (scanner not working), room plaque updates 
    *  Create mobile app interface that would allow QR code scanning in request and problem reporting (QR would be on each door plaque)





## Setup

### Create Environment
* `python -m venv <name_of_virtualenv>`

### Installs
* `pip install Flask`
* `pip install -U Flask-SQLAlchemy`
* `pip install sqlalchemy-utils`
* `pip install werkzeug`
* `pip install flask-WTF`
* `pip install psycopg2`
* `pip install flask_login`
* `pip install pandas`

* may need the `pip install ipykernel` - this is really only needed for interactive window in VSCode 

### Activate Environment
* `. venv/Scripts/activate`