# proj-key-inventory

Author: Erin James Wills [ejw.data@gmail.com](ejw.data@gmail.com)

![Key Database Banner](./images/key-database.png)

<cite>Photo by <a href="https://unsplash.com/@contradirony?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Samantha Lam</a> on <a href="https://unsplash.com/photos/silver-and-gold-round-coins-zFy6fOPZEu0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a></cite>  

## Objective
Simple application that tracks key numbers, key owners, and accessible lock locations


## Dev Notes  

#### PROGRAM EXECUTION
1.  Web Interface to ADD users, buildings, rooms, access_approvers, access_codes
2.  Web Interface to INITIATE key requests starting with the requests table
3.  Request Form starts from User requesting room access.  The form includes 
	a table where new room requests can be added.  When clicking New the popup
	contains input of buiding, wing, and room number.  The space_number is 
	generated from a query.  The space_number is then used to populate a dropdown
	for the space approver.   Additional spaces can be added.
	The submit button then calculates the access_codes and approvers.  The request 
	table has the information inserted into the table for each key determined with
	status_code of 1 (REQUEST SUBMITTED).  
4.  On Submit, the appropriate Approvers action items is update.  The approver clicks
	the action item and can accept or reject and provide a comment. On approval, the
	status_code is updated to REQUEST APPROVED, approved set to TRUE, and 
	approved_comment is updated.  On rejection, the status_code is updated to REQUEST
	REJECTED, approved set to FALSE, and rejected_comment is updated.  The user 
	interface is updated with status updates and comments.  The submit button is now
	replaced with a MODIFY button which pulls up a form containing the request information 
	from the original request.  The change to the space_number or maybe the status_code to
	REQUEST SUBMITTED should trigger resubmit to approver. 
	Note:  The interface for Approvers should default to only show 'REQUEST SUBMITTED' for
	that approver on their home page.  
5.  On change of status_code to 'REQUEST APPROVED' a trigger is enacted and the key_order
	table is updated.
6.  The key_order form should check for available keys in the key_inventory and if there
	are no matches then the keys_created table is updated.  The keyshop makes the key
	based on the access_code.  When complete, the fabrication_status_id of 3 is updated
	and this triggers the update of the key_inventory table and the update of the key_orders
	table.  The key_copy is also updated.
	Note:  The keyshop requests should only display items NOT COMPLETE.
7.  Upon the user picking up the key, the admin staff updates the key_inventory to show 
	the status to be 'ISSUED'
8.  At the final stage after pickup - the key_inventory, key_created, and key_orders

**Does key_orders need a status for the user to know the status?**
