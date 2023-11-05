SELECT *
FROM requests;

SELECT *
FROM key_orders;

-- trigger occurs when status code is changed to 2
UPDATE requests
SET status_code = 2 
WHERE request_id = 1;

-- request table is updated and key_orders has new record