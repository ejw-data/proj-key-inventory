-- This query is used in the api_routes.py file within the 'api/table/buildings/group` 
-- route that is used to create the Room Table on the users.html page

Select r.user_id, u.first_name, u.last_name, u.email, ap.space_number_id, rc.room_type, r.access_code_id,  r.request_status_id
From requests r
INNER JOIN users u
ON u.user_id = r.user_id
INNER JOIN access_pairs ap
ON ap.access_code_id = r.access_code_id
LEFT JOIN rooms rm
ON rm.space_number_id = ap.space_number_id
LEFT JOIN room_classification rc
ON rc.room_type_id = rm.room_type_id
WHERE r.request_status_id NOT IN (3,8)
UNION
Select r.user_id, u.first_name, u.last_name, u.email, r.spaces_requested, rc.room_type, r.access_code_id, r.request_status_id
From requests r
INNER JOIN users u
ON u.user_id = r.user_id
INNER JOIN rooms rm
ON rm.space_number_id = r.spaces_requested
INNER JOIN room_classification rc
ON rc.room_type_id = rm.room_type_id
WHERE r.access_code_id = 0;