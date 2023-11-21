INSERT INTO titles (title)
VALUES ('undergraduate student'),
		('graduate student'),
		('staff'),
		('faculty'),
		('building manager'),
		('department head'),
		('dean'),
		('senior administration'),
		('facilities');

INSERT INTO roles (user_role)
VALUES ('requester'),
		('approver'),
		('administrator');

INSERT INTO users (first_name, last_name, title_id, role_id, email)
VALUES ('erin', 'wills', 1, 1, 'ew@mysite.com'),
		('will', 'wright', 1, 1, 'ww@mysite.com'),
		('andrew', 'ng', 1, 1, 'an@mysite.com'),
		('bob', 'turtle', 5, 3, 'bt@mysite.com'),
		('jake', 'powers', 9, 3, 'jp@mysite.com');

INSERT INTO access_approvers (approver_id, role_approved_by)
VALUES (4, 9);

INSERT INTO authentication (login_id, username, password_hash)
VALUES (1, 'ejwadmin', 'alf344t4090j0aojfsfa');


INSERT INTO buildings (building_number, building_name, building_description)
VALUES (24, 'Chemistry', 'Chemistry Department Research Space');

INSERT INTO approver_zones (building_number, access_approver_id)
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

INSERT INTO access_codes (access_description, created_by, authorized_by)
VALUES ('Classroom', 1, 1),
		('Faculty Office and Suite', 1, 1),
		('Front Suite Only', 1, 1);

INSERT INTO approval_status (status_code_name)
VALUES ('REQUEST SUBMITTED'),
		('REQUEST APPROVED'),
		('REQUEST REJECTED'),
		('KEY CREATED'),
		('KEY READY FOR PICKUP'),
		('KEY ASSIGNED');

INSERT INTO access_pairs (access_code_id, space_number_id)
VALUES (1, 'B24010101'),
		(2, 'B24020101'),
		(2, 'B24020102'),
		(3, 'B24010101'),
		(3, 'B24020101'),
		(3, 'B24020102');

INSERT INTO fabrication_status (fabrication_status)
VALUES ('IN QUEUE'),
		('SCHEDULED'),
		('COMPLETED');

INSERT INTO keys_created (key_number, key_copy, access_code_id, fabrication_status_id)
VALUES (43221, 1, 3, 3),
		(56432, 1, 1, 3),
		(34523, 1, 2, 3),
		(46363, 2, 2, 3),
		(59873, 3, 2, 3);

INSERT INTO key_status (key_status)
VALUES ('ISSUED'),
		('INVENTORY'),
		('ASSIGNED FOR PICKUP'),
		('BROKEN'),
		('LOST');

-- This will initiate some of the logic
-- logic needs built to complete this request via forms  
INSERT INTO requests (user_id, space_number_id, building_number, access_approver_id, access_code_id, status_code)
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

INSERT INTO order_status (order_status)
VALUES ('READY FOR PICKUP'),
		('WAITING FOR FABRICATION'),
		('WAITING FOR DELIVERY'),
		('PICKED UP COMPLETE');
		
-- -- key_orders are added programatically via request trigger
-- -- key_orders will just need to be updated
-- INSERT INTO key_orders (transaction_id, access_code_id)
-- VALUES (1, 3),
-- 		(2, 1),
-- 		(3, 2),
-- 		(4, 2),
-- 		(5, 2);