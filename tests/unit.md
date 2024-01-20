# Unit Tests

This file contains descriptions of the different tests applied to the application.  

## Access Code Search
Functions found in access_codes.py

### find_codes()
Function that receives a list of rooms and a list of access codes and returns a dictionary containing the optimal selection of access codes, assigned spaces, and unassigned spaces.  The function was tested initially with a access code dataset that addressed very common use cases.  Below is the test data and tests:


### Testing
``` 
# Codes
# room_access_codes = [
#     {"id": 1, "value": ("r1",), "count": 1},
#     {"id": 2, "value": ("r2",), "count": 1},
#     {"id": 3, "value": ("r3",), "count": 1},
#     {"id": 4, "value": ("r4",), "count": 1},
#     {"id": 5, "value": ("r5",), "count": 1},
#     {"id": 6, "value": ("r6",), "count": 1},
#     {"id": 7, "value": ("r1", "r2"), "count": 2},
#     {"id": 8, "value": ("r3", "r5"), "count": 2},
#     {"id": 9, "value": ("r3", "r4", "r5"), "count": 3},
#     {"id": 10, "value": ("r1", "r2", "r3"), "count": 3},
#     {"id": 11, "value": ("r5", "r6"), "count": 2},
#     {"id": 12, "value": ("r1", "r2", "r3", "r5", "r6"), "count": 5},
#     {"id": 13, "value": ("r1", "r2", "r3", "r5", "r6", "r7"), "count": 6},
# ]
```
``` 
# Cases
# requested_rooms = ("r1", "r3", "r4")
# requested_rooms = ("r5", "r3", "r6", "r2")
# requested_rooms = ("r1", "r2", "r3", "r5", "r6")
# requested_rooms = ("r1", "r2", "r3", "r5", "r4")
# requested_rooms = ("r1",)
# requested_rooms = ("r1", "r2")
# requested_rooms = ("r1", "r4")
# requested_rooms = ("r1", "r4", "r7")
# requested_rooms = ("r1", "r4", "r3", "r5", "r6")
# requested_rooms = ("r1", "r2", "r3", "r4", "r5", "r6")
# requested_rooms = ("r22",)
```
``` 
# Test
# find_codes(requested_rooms, room_access_codes)
```
The cases specifcally looked to ensure that appropriate results were returned for single room requests, multi-room requests, requests for rooms without access codes, requests that had an appropriate single code versus two or more codes, requests that contained the previous configurations and rooms without codes, and several more configurations.  

### Other
The access_codes.py file also has several other functions but these functions were primarily used for filtering and did not require as extensive testing.  

## Request Access Order Basket

The code for this feature is not a single function but multiple interacting pieces of code.  The order basket utilizes the following technologies:  
*  Bootstrap5 HTML modal
*  Javascript event handler that hides the form for interface style purposes  
*  WTF Forms was used to generate the form through an object oriented model and to secure and validate submission inputs in a Flask route
*  Javascript event handlers and API route used to filter form dropdown inputs so only applicable inputs based on the inputs from the previous selection would be allowed.
*  Form submission button that sends form input data to a Flask route that stores the information temporarily as session data
*  Javascript event handler that requests updated HTML code for the order basket table and table messages after each submission.  
*  Basket submission button that runs a Flask route to determine the number of keys (assigned codes) needed and initiate workflows for codes to be generated for spaces not assigned to codes, requests for keys to be sent to building approvers, updates to existing requests that have not yet been approved to be removed if conflicting with new orders, updates to exising request that have been approved that are no longer needed (adds/keeps key in inventory), and requests keys to be returned.
*  The above mentioned Flask route runs multiple functions including the find_codes() function listed at the beginning of this document.   
*  Since the PostgreSQL tables are updated, the page views for the appropriate administrators are also updated and upon their approval or rejection of the request, the database triggers execute database procedures (PL/pgSQL) the remaing steps in the workflow.  
*  The form also has additional features like buttons that enact functions to clear the order basket, and functions that reset the form to have a consistent look each time the form is accessed.  

### Testing  

The testing for this part will initially be a bit limited.  Currently, there are a limited number of rooms and access codes configured in the database so the following will be the initial tests until a large sample database is created:  

**In the cases below, the user has not had any requests approved yet**  
*  Add a single room that has an access code  - B24010101
*  Add the same single room again - update messaging on request form to indicate that the request is bypassed due to duplication  - B24010101
*  Add multiple rooms that also include the initial room - this should delete the original unapproved request and add in the new request showing all the requested rooms in one request - Code 3 - B24010101, B24020101, B24020102
*  Add same multi-room request again - Code 3 - B24010101, B24020101, B24020102
*  Add new request for a single room that already exists in a multi-room request - B24020102
*  Add in one basket the same combination of keys twice - B24020102,  B24020102
*  !Add request for a room that does not have a code and follow up with another room request that does not exist in the system - B24010201, B24010201 (need to add new room)
    * Error - Adds duplicate space add requests - added simple check
*  Continue the above case by adding a single room that does not have a code - B24010201

**Need to revisit**
*  Code 3 + B2400201 resulted in incorrectly deleting Code 3 and correctly add code requestn- fixed
*  Add Rooms where none have their own individual code but one pair makes a code ie, B24010201, B24020101, B24020102
    * Expected Outcome:  The key waiting for pickup be deleted and two of the spaces being assigned one code and the other waiting for for code assignment
    * Actual Outcome:  No errors but all three rooms are listed as not having codes
    * Fix Applied:  fixed get_codes() so that a list of values can be processed instead of a single value and a new action was added to the basket route to delete code assignment requests that have not been approved.  The deletion process required multiple adjustments to correctly delete the prior record(s).  
*  - Add three rooms that make an access code that replaces an existing two room access code - add Code 3 - B24010101, B24020101, B24020102
* - Add a code but don't fill in all the form parts - ie PI/Manager - should just reset form

Note:  More testing needs to be done on the missing codes logic.  It may work fine with the above test but the code functionality is not apparent.

**In the cases below, the user has had requests assigned and approved**
*  Add same key as what has already been received - Add Code 3 - Need to add a message
*  Add key that is not in access codes - B24010201
*  Add key that does not have it's own code but is part of another combo code - B24020102
*  Add request that includes a key that has no individual code but as a combo of multiple keys has a code - B24020101
    * Expected Outcome:  The key pending a code should be removed and the request should be for one access code that is waiting for approval. The assigned code is changed to be waiting return.
    * Actual Outcome:  IndexError: list index out of range - site_routes.py on line 865 - space_owner_id=filter_record[0][0]
    * Fix Applied:  Set conditional check from looking at a single item to looking at any item in a list; also updated logic for deleting keys and code requests that have not been fulfilled.  Expected outcome is now occuring.  

**In the cases below, the user has had requests ready for pickup**  
Same tests as above


**In the cases below, the user has had requests approved**
Same tests as above


**In the cases below, the user has had requests declined**
* Fixed some errors, but need to retest


**In the cases below, the user has had keys returned**
* Test later


**In the cases below, the user has had keys lost**  
* Test later


**In the cases below, the user has had keys broken**
* Test later



