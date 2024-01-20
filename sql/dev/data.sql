
INSERT INTO titles (title_id, title)
VALUES (1,'undergraduate student'),
		(2,'graduate student'),
		(3,'staff'),
		(4,'faculty'),
		(5,'building manager'),
		(6,'department head'),
		(7,'dean'),
		(8,'senior administration'),
		(9,'facilities'),
		(10,'visitor');

INSERT INTO roles (role_id, user_role)
VALUES (1,'requester'),
		(2,'approver'),
		(3,'administrator'),
		(4,'analyst');

INSERT INTO users (user_id, first_name, last_name, title_id, role_id, email, sponsor_id)
VALUES (0,'unassigned', 'unassigned', 1,1,'unassigned', 1),
		(1,'erin', 'wills', 1, 3, 'ew@mysite.com', 1),
		(2,'wendy', 'warhol', 1, 4, 'ww@mysite.com', 1),
		(3,'andy', 'newman', 1, 1, 'an@mysite.com', 1),
		(4,'bob', 'turtle', 5, 2, 'bt@mysite.com', 1),
		(5,'jake', 'powers', 9, 2, 'jp@mysite.com', 1);

INSERT INTO approvers (approver_id,user_id, role_approved_by)
VALUES (1,4, 5), 
		(0,0,1);

INSERT INTO buildings (building_number, building_name, building_description)
VALUES (24, 'Chemistry', 'Chemistry Department Research Space');

INSERT INTO zones (building_number, approver_id)
VALUES (24, 1);

INSERT INTO room_classification (room_type_id, room_type)
VALUES (201, 'private office'),
		(205, 'conference room'),
		(210, 'classroom'),
		(220, 'shared office');

INSERT INTO rooms (space_number_id, building_number, floor_number, wing_number, room_number, room_type_id)
VALUES ('B24010101', 24, 01, 01, 01, 210),
		('B24010201', 24, 01, 02, 01, 210),
		('B24010202', 24, 01, 02, 02, 210),
		('B24020101', 24, 02, 01, 01, 201),
		('B24020102', 24, 02, 01, 02, 220);

INSERT INTO room_assignment (space_number_id, user_id)
VALUES ('B24010101', 1),
		('B24020101', 2),
		('B24020102', 2),
		('B24010101', 2),
		('B24010201', 1);

INSERT INTO room_amenities (space_number_id, room_projector, room_seating)
VALUES ('B24010101', TRUE, 50),
		('B24020101', FALSE, 1),
		('B24020102', FALSE, 4);

INSERT INTO access_codes (access_code_id, access_description, created_by, authorized_by)
VALUES (0,'Unassigned', 1, 1),
		(1,'Classroom', 1, 1),
		(2,'Faculty Office and Suite', 1, 1),
		(3,'Front Suite Only', 1, 1);

INSERT INTO request_status (request_status_id, request_status_name)
VALUES (1,'REQUEST SUBMITTED'),
		(2,'REQUEST APPROVED'),
		(3,'REQUEST REJECTED'),
		(4,'KEY CREATED'),
		(5,'KEY READY FOR PICKUP'),
		(6,'KEY ASSIGNED'),
		(7,'KEY READY FOR RETURN'),
		(8,'KEY RETURNED'),
		(9,'KEY LOST'),
		(10, 'SPACE NEEDS ADDED TO SYSTEM');

INSERT INTO access_pairs (access_code_id, space_number_id)
VALUES (1, 'B24010101'),
		(2, 'B24020101'),
		(2, 'B24020102'),
		(3, 'B24010101'),
		(3, 'B24020101'),
		(3, 'B24020102');

INSERT INTO fabrication_status (fabrication_status_id, fabrication_status)
VALUES (1,'IN QUEUE'),
		(2,'SCHEDULED'),
		(3,'COMPLETED');

-- -- This was used to test functionality before SQL triggers automated the process
-- INSERT INTO keys_created (request_id, access_code_id, key_copy, fabrication_status_id)
-- VALUES (1, 1, 3, 3),
-- 		(2, 1, 1, 3),
-- 		(3, 1, 2, 3),
-- 		(4, 2, 2, 3),
-- 		(5, 3, 2, 3);

INSERT INTO key_status (key_status_id, key_status)
VALUES (1,'ISSUED'),
		(2,'INVENTORY'),
		(3,'ASSIGNED FOR PICKUP'),
		(4,'BROKEN'),
		(5,'LOST'),
		(6,'TRANSFERRED');

-- -- This was used to test functionality before SQL triggers automated the process
-- INSERT INTO requests (user_id, spaces_requested, building_number, approver_id, access_code_id, status_code)
-- VALUES (1, 'B24010101', 24, 1, 1, 1),
-- 		(2, 'B24010101', 24, 1, 2, 1),
-- 		(3, 'B24010101', 24, 1, 2, 1),
-- 		(4, 'B24010101', 24, 1, 2, 1),
-- 		(5, 'B24010101', 24, 1, 3, 1);

-- INSERT INTO key_inventory (transaction_id, key_number, key_copy, key_status_id)
-- VALUES (1, 43221, 1, 1),
-- 		(2, 56432, 1, 1),
-- 		(3, 59873, 3, 1),
-- 		(4, 34523, 1, 1),
-- 		(5, 46363, 2, 1);

INSERT INTO order_status (order_status_id, order_status)
VALUES (1,'READY FOR PICKUP'),
		(2,'WAITING FOR FABRICATION'),
		(3,'WAITING FOR DELIVERY'),
		(4,'PICK UP COMPLETE');
		
-- -- This was used to test functionality before SQL triggers automated the process
-- INSERT INTO key_orders (transaction_id, access_code_id)
-- VALUES (1, 3),
-- 		(2, 1),
-- 		(3, 2),
-- 		(4, 2),
-- 		(5, 2);