
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

INSERT INTO users (user_id, first_name, last_name, title_id, role_id, email)
VALUES (1,'erin', 'wills', 1, 1, 'ew@mysite.com', 1),
		(2,'will', 'wright', 1, 1, 'ww@mysite.com', 1),
		(3,'andrew', 'ng', 1, 1, 'an@mysite.com', 1),
		(4,'bob', 'turtle', 5, 3, 'bt@mysite.com', 1),
		(5,'jake', 'powers', 9, 3, 'jp@mysite.com', 1);

INSERT INTO approvers (approver_id,user_id, role_approved_by)
VALUES (1,4, 5);

-- INSERT INTO authentication (id, username, password_hash)
-- VALUES (1, 'ejwadmin', 'alf344t4090j0aojfsfa');


INSERT INTO buildings (building_number, building_name, building_description)
VALUES (24, 'Chemistry', 'Chemistry Department Research Space');

INSERT INTO approver_zones (building_number, approver_id)
VALUES (24, 1);

INSERT INTO room_classification (room_type_id, room_type)
VALUES (201, 'private office'),
		(205, 'conference room'),
		(210, 'classroom'),
		(220, 'shared office');

INSERT INTO rooms (space_number_id, building_number, floor_number, wing_number, room_number, room_type)
VALUES ('B24010101', 24, 01, 01, 01, 210),
		('B24020101', 24, 02, 01, 01, 201),
		('B24020102', 24, 02, 01, 02, 220);

INSERT INTO room_amenities (space_number_id, room_projector, room_seating)
VALUES ('B24010101', TRUE, 50),
		('B24020101', FALSE, 1),
		('B24020102', FALSE, 4);

INSERT INTO access_codes (access_code_id, access_description, created_by, authorized_by)
VALUES (1,'Classroom', 1, 1),
		(2,'Faculty Office and Suite', 1, 1),
		(3,'Front Suite Only', 1, 1);

-- change status_code to status_code_id
INSERT INTO approval_status (status_code, status_code_name)
VALUES (1,'REQUEST SUBMITTED'),
		(2,'REQUEST APPROVED'),
		(3,'REQUEST REJECTED'),
		(4,'KEY CREATED'),
		(5,'KEY READY FOR PICKUP'),
		(6,'KEY ASSIGNED'),
		(7,'KEY READY FOR RETURN',
		(8,'KEY RETURNED'),
		(9,'KEY LOST');

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

-- This will initiate some of the logic
-- logic needs built to complete this request via forms  
INSERT INTO requests (user_id, space_number_id, building_number, approver_id, access_code_id, status_code)
VALUES (1, 'B24010101', 24, 1, 1, 1),
		(2, 'B24010101', 24, 1, 2, 1),
		(3, 'B24010101', 24, 1, 2, 1),
		(4, 'B24010101', 24, 1, 2, 1),
		(5, 'B24010101', 24, 1, 3, 1);

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
		
-- -- key_orders are added programatically via request trigger
-- -- key_orders will just need to be updated
-- INSERT INTO key_orders (transaction_id, access_code_id)
-- VALUES (1, 3),
-- 		(2, 1),
-- 		(3, 2),
-- 		(4, 2),
-- 		(5, 2);