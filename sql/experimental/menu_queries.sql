-- find all approvers
Select first_name || ' ' || last_name as username
FROM users u
WHERE u.user_id in (
	SELECT aa.approver_id
	FROM access_approvers aa);
	
	
-- find all approvers for a building number
Select u.first_name || ' ' || u.last_name as username
FROM users u
WHERE u.user_id in (
	SELECT aa.approver_id
	FROM access_approvers aa
	WHERE aa.access_approver_id in (
		SELECT az.access_approver_id
		FROM approver_zones az
		WHERE az.building_number = 24)
);

-- Find all rooms given a specific building
SELECT CONCAT(CONCAT(rm.floor_number, rm.wing_number), rm.room_number) as room
FROM rooms rm
WHERE rm.building_number = 24;

-- Find access codes given list of rooms
With access_matrix as (select access_code_id,
  MAX(case when space_number_id ='B24010101' then 'true' else null end) as B24010101,
  MAX(case when space_number_id  ='B24020101' then 'true' else null end) as B24020101,
  MAX(case when space_number_id  ='B24020102' then 'true' else null end) as B24020102
from access_pairs
group by access_code_id)
Select am.access_code_id, *
FROM access_matrix am
WHERE (am.B24020101 = 'true') and (am.B24020102 = 'true');

-- Find access codes given list of rooms - Not correct
SELECT * FROM crosstab(
	'SELECT access_code_id::text, space_number_id::text, 1 as Truth FROM access_pairs order by 1,2')
	as access_pairs (room_number text, rm1 int, rm2 int, rm3 int);




-- Find all users with access to a specific room
Select first_name || ' ' || last_name as username
FROM users
WHERE user_id in (
	Select user_id
	FROM requests
	WHERE request_id in (
		Select transaction_id
		FROM key_inventory
		WHERE key_number in (
			Select key_number 
			From keys_created
			Where access_code_id in (
				Select access_code_id
				FROM access_pairs
				WHERE space_number_id = '24-01-01-01'
				)
			)
		)
	);