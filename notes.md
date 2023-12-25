### Tasks
1.  Improve interface
    *  ! Make sure form options are all formatted the same on input
    *  ! Add requests to appropriate table to complete workflow
    *  ! Admin.html => fix form using /post/approver/add route so that admin approver is not part of form and it uses current_id
    *  ! Admin.html/forms => remove 'input the space id from the Add Room form.  Calculate this value.  Also apply form update javascript to the Add room form on this page so it matches the index.html page.  Need to decide how to add a PI and Building approver to each space!!!!
    *  ! Admin.html/forms => make more room selections to look like the Add Room Amenities form. ie access.html/form Add Room Access
    * Fix menu hamburger menu when page is minimized.

    *  Keys page inputs all correctly formatted to uppercase in db
    *  Access page needs room access form to show more text describing the room
    *  ! Add form logical validation  
        *  Add Building:  existing building number or name can not be submitted
        *  Add Room:  technical building name can not be submitted
        *  Add Room:  Make both inputs be unique in the db
        *  Add User:  verify that Email address is unique in db
    *  Prevent all users from access the different side menu options.  Only admin should have access to each section.

    * Design Choice - all status messages are all caps and all descriptive columns are lower case in db
    * Keys.html needs the orders in progess table resized for small screens.  Maybe just make table responsive with a scroll bar.
    






1.  Add space owner, add student relationship on profile - reports to or sponsored
    *  Also include role so that special rules can be added based on this association
    *  Maybe have utilities vary based on this metric - checks for if student has left.
1.  Create order basket for requests that utilize past and current information.  
1.  ! Create restrictions on who can see what menu
1.  ! Restrict who can access which routes
1.  ! Move common html to template parts in flask
1.  ! Allow to upload picture as profile image
1.  ! Create messaging system that stores all messages per request
1.  ! Create popup that displays the stats of a request and all messages
    *  Request ID Title 
    *  Start date - ready date - pickup date
    *  Total days elapsed
    *  Building Approver - Room Approver
        *  Access Code (key) - Room(s)
    *  Messages (listed as Date, Sender Group, Sender, Message) - Sender Group can also be 'Requester', 'PI'
1.  !/- Separate routes into different files
    * site_routes.py - pages loading (render_templates)
    * api_routes.py - graphics/data
    * form_routes.py - forms posting data
    * table_routes.py - tables getting data
    * workflow_routes.py - updates to the database that often trigger db procedures
1.  ! Create Reports - these could be used in periodic emails request for checks for accuracy
    * Space Owner - people access by Room per PI - each report could be emailed to PI
    * Building Approver - All access under their building
    * Recently removed by affiliation
    * Recently added by affiliation
    * Keyshop response time, keys issued, door maintenance, trends per week and weekday

### Process Updates
* Should I record all space requests or just the access codes?
* I think I should record the access codes because each person will only have unique access codes
* The original request can calculate the access codes and for each access code requested it will receive an request_id
* In addition to the access_code, the space_ids requested will be added to a column to preserve the original request. 
* This will require modifications to the requests table but none of the other tables. 

### key request form
* Create new table that will hold the requests in a modal and the modal brings up another model for adding items
* Each time the for has a new item added the page refreshes.  
* Use separate button to contents of the


Types of Storage
* Local Storage
* Session Storage

Types of Server Updating
* AJAX
* Websockets
* SSE (server sent events) - 

Streaming information (messaging queuing systems, )
* RabbitMQ / ActiveMQ  (message broker / queue)
* Kafta (full streaming system)
* Amazon Kinesis / IBM MQ  (full streaming system)
* Amazon SQS (simple queue )



### Features

* hashing passwords into the database with a secret key
* comparing hashed versus plain text passwords for authentication
* webpages with login requirement decorator
* passing template items to multiple pages with a decorator
* flask_login sessions
* uses flask flash messaging
* add in upload section  
* using flask login manager to track sessions
* form validation
* event logging on all pages
* A/B testing on authenticated pages
* Survey pages



### Types of User Roles
* Site Owner
* Administrator
* Analyst
* Key Shop
* Approver
* Requester

### Pages
* Login
* Register (admin must first add the persons email)
* Dashboard
    * General Dashboard:  System Notices, Keys and Spaces Allowed, Profile
    * Key Shop Dashboard:  Key Fab Requests, Repair Requests, Lock Changes
    * Approver Dashboard:  Requests, Access Space Summary
    * Analyst Dashboard:  Click success, synthetic monitoring (no-sql db?), general system stats,
    * Administrator Dashboard:  Can mimic anyones account, full view
    * Site Owner: only person allowed to add Administors.  Stats of each role.  

* Table Views
    * Requests - shows full summary of users all, active, and inactive requests.  Can report key lost or returned and request new keys.
    * Space Updates - shows Space info and includes an option to add: building, room, amenities
    * Access Updates - includes access matrix, add new codes, and add new code pairs.
    * Users - add approvers, key shop, analyst, and general users.  Shows table of all users with filters by role, recently left, recently new,
    * Key shop - (include access updates) add new keys, add status codes, orders status, stats
    * Admin - see stats of users, approvers

    - collect data of when people login and where they click.

### Case Studies  

Building Numbers:  24, 28, 27
Rooms:  5 rooms per building
Access codes cases:
    * Full Access
    * Single Room
    * Suite Access
Approvers:  Each building has one approver
Requestors:  
    * 3 Requests for each requestor who have a full access
    * Each building has one requestor that is requesting access to a suite
    * a requestor is asking for access to two rooms in different buildings
    * a requestor asks for access to a single room and then asks for access to the main office.  The user should give back one key and receive a new key.  


### Forms

* Registration - add in email address and temporary password.  Redirects to profile page and where new password is generated.  Upon completion they are redirected to login page.

* Login - upon Login, the user is redirected to the dashboard page

* Logout (button) - closes session.  Redirects user to login page.

* Building



### Views

* Buildings - allows building to be selected from dropdown and shows that buildings spaces.  Add/Update/Delete to that rooms list.


### Interactive menus
*  Since the dropdown form options are populated at the time of the page load, the form fields are not affected by the changes in other field settings.  
*  To make it interactive, I will add an event listener on a field and it will modify the DOM of another field using D3.  I think I will just need an api that will take the parameter and return all the other form data.  
* For example, the key quest form has building as an input.  The event listener will be triggered on the change of that field and this input will be used in an API that returns a dictionary of {'floors':[], 'wings':[], 'rooms':[]}.  The basic process would be to d3.select the 2nd dropdown and then bind the data to the element and then clear out the html and then pass a function that updates each element.  

### WTF Forms
* note the variables assigned to the forms need to be unique becasue these become the input id's.
* an id could be assigned in the jinja that could overwrite it but then there would be extra assignments and mismatches in the code.  This is probably not that important but for now I will keep the names unique until I determine if there are any other issues related to this.
* WTF Forms has nice functionality but as I use it there are some less apparent issues with how the standard template generates ids.  This is only apparent if multiple forms are put on the same page or if forms have similar inputs.  My forms are introduced as popups so the form for adding a room and the form for making a room selection use the same variable name (until my last change where I removed these duplications.)


### Tables
* Use datatables.js for large tables 