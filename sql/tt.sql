Select * from requests;

Select * from approval_status;

-- key_orders table may need an extra field for status and key_assigned
Select * from key_orders;

INSERT INTO requests (user_id, space_number_id, building_number, access_approver_id, access_code_id, status_code)
VALUES (1,'B24010101',24,1,1,1);

-- upon key_order table getting updated the following actions occur
-- 1.  Trigger on key_orders that when updated it executes a procedure
-- 2. Procedure checks inventory to see if it exists   
--     2a.  if true then it updates key_orders to have a fulfilled status and the key number in that table.  
--     This triggers for the request table to be updated.
--     2b.  if false then it adds request to the keys_created table and upon the keyshop updating this table
--          the key_orders table is updated and this triggers the request table to be updated also.
--     		Note:  The inventory table also needs updated with the key as being checked out.


UPDATE requests
SET  status_code = 2,  approved_date=NOW(), approved=true, approval_comment='Approved for six months.'
WHERE request_id = 1;