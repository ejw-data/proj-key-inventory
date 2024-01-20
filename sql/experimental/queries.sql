-- Query that shows who has not yet registered
select * 
from users
where email not in (
	Select username
	From authentication
);



SELECT key_number, key_copy
FROM key_inventory ki
WHERE (ki.key_status_id = 2) AND (ki.key_number = (
	SELECT key_number
	FROM keys_created
	WHERE access_code_id = (
		SELECT access_code_id
		FROM key_orders
		WHERE transaction_id = 1)
));