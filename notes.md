

### Features

* hashing passwords into the database with a secret key
* comparing hashed versus plain text passwords for authentication
* webpages with login requirement decorator
* passing template items to multiple pages with a decorator
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
* Register (request goes to approver)
* Dashboard
    * General Dashboard:  System Notices, Keys and Spaces Allowed, Profile
    * Key Shop Dashboard:  Key Fab Requests, Repair Requests, Lock Changes
    * Approver Dashboard:  Requests, Access Space Summary
    * Analyst Dashboard:  Click success, synthetic monitoring (no-sql db?), general system stats,
    * Administrator Dashboard:  Can mimic anyones account, full view
    * Site Owner: only person allowed to add Administors.  Stats of each role.  



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