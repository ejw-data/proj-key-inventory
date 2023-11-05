DROP TABLE IF EXISTS key_inventory;
DROP TABLE IF EXISTS keys_created;
DROP TABLE IF EXISTS key_status;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS access_pairs;
DROP TABLE IF EXISTS access_codes CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS room_amenities;
DROP TABLE IF EXISTS room_classification CASCADE;
DROP TABLE IF EXISTS key_orders CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS titles;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS access_approvers CASCADE;
DROP TABLE IF EXISTS approval_status;
DROP TABLE IF EXISTS approver_zones;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS fabrication_status;



-- USERS ------------------------------------------------------
CREATE TABLE titles (
	title_id SERIAL PRIMARY KEY,
	title VARCHAR
);

INSERT INTO titles (title)
VALUES ('faculty'),
		('undergraduate student'),
		('graduate student'),
		('staff'),
		('building manager'),
		('department head'),
		('dean'),
		('senior administration'),
		('facilities');

CREATE TABLE roles (
	role_id SERIAL PRIMARY KEY,
	user_role VARCHAR
);

INSERT INTO roles (user_role)
VALUES ('requester'),
		('approver'),
		('admin');

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	title_id INT REFERENCES titles (title_id),
	role_id INT REFERENCES roles (role_id)
);

INSERT INTO users (first_name, last_name, title_id, role_id)
VALUES ('erin', 'wills', 1, 1),
		('will', 'wright', 1, 1),
		('andrew', 'ng', 1, 1),
		('bob', 'turtle', 5, 3),
		('jake', 'powers', 9, 3);
		

CREATE TABLE access_approvers (
	access_approver_id SERIAL PRIMARY KEY,
	approver_id INT REFERENCES users (user_id),
	role_approved_by VARCHAR,
	date_approved TIMESTAMP NOT NULL DEFAULT NOW(),
	date_removed TIMESTAMP
);

INSERT INTO access_approvers (approver_id, role_approved_by)
VALUES (4, 9);


-- SPACE & GRANTED APPROVAL ------------------------------------------------------------

CREATE TABLE buildings (
	building_number INT PRIMARY KEY,
	building_name VARCHAR,
	building_description VARCHAR
);

INSERT INTO buildings (building_number, building_name, building_description)
VALUES (24, 'Chemistry', 'Chemistry Department Research Space');


CREATE TABLE approver_zones (
	building_number INT REFERENCES buildings (building_number),
	access_approver_id INT REFERENCES access_approvers (access_approver_id),
	PRIMARY KEY (building_number, access_approver_id)
);

INSERT INTO approver_zones (building_number, access_approver_id)
VALUES (24, 1);

CREATE TABLE room_classification (
	room_type_id INT PRIMARY KEY,
	room_type VARCHAR
);

INSERT INTO room_classification (room_type_id, room_type)
VALUES (201, 'private office'),
		(205, 'conference room'),
		(210, 'classroom'),
		(220, 'shared office');

CREATE TABLE rooms (
	space_number_id VARCHAR PRIMARY KEY,
	building_number INT REFERENCES buildings (building_number),
	floor_number INT,
	wing_number INT,
	room_number INT,
	room_type INT REFERENCES room_classification (room_type_id)
);

INSERT INTO rooms (space_number_id, building_number, floor_number, wing_number, room_number, room_type)
VALUES ('24-01-01-01', 24, 01, 01, 01, 210),
		('24-02-01-01', 24, 02, 01, 01, 201),
		('24-02-01-02', 24, 02, 01, 02, 220);


CREATE TABLE room_amenities (
	space_number_id VARCHAR PRIMARY KEY REFERENCES rooms (space_number_id),
	room_projector BOOL,
	room_seating INT
); 

INSERT INTO room_amenities (space_number_id, room_projector, room_seating)
VALUES ('24-01-01-01', TRUE, 50),
		('24-02-01-01', FALSE, 1),
		('24-02-01-02', FALSE, 4);


-- ACCESS ASSIGNMENT -------------------------------------------------------------------
-- changed access_code to access_code_id - need to consider the effect
CREATE TABLE access_codes (
	access_code_id SERIAL PRIMARY KEY,
	access_description VARCHAR,
	created_by VARCHAR,
	authorized_by VARCHAR,
	created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO access_codes (access_description, created_by, authorized_by)
VALUES ('Classroom', 'ejw', 'T. Bundy'),
		('Faculty Office and Suite', 'ejw', 'Prof. Andrews'),
		('Front Suite Only', 'ejw', 'Prof. Andrews');

-- APPROVAL PROCESS ------------------------------------------------------------

CREATE TABLE approval_status (
	status_code SERIAL PRIMARY KEY,
	status_code_name VARCHAR
);

INSERT INTO approval_status (status_code_name)
VALUES ('REQUEST SUBMITTED'),
		('REQUEST APPROVED'),
		('REQUEST REJECTED'),
		('KEY CREATED'),
		('KEY READY FOR PICKUP'),
		('KEY ASSIGNED');

-- requests table:  request_id, user_id, space, approver, status, dates, reasoning
-- logic updates record
-- logic on update adds record to key_owner table the deletes record
CREATE TABLE requests (
	request_id SERIAL PRIMARY KEY,
	user_id INT,
	space_number_id VARCHAR,
	building_number INT,
	access_approver_id INT,
	access_code_id INT REFERENCES access_codes (access_code_id),
	status_code INT REFERENCES approval_status (status_code),
	request_date TIMESTAMP NOT NULL DEFAULT NOW(),
	approved_date TIMESTAMP,
	approved BOOL DEFAULT FALSE,
	approval_comment VARCHAR,
	rejection_comment VARCHAR,
	FOREIGN KEY (building_number, access_approver_id) REFERENCES approver_zones (building_number, access_approver_id)
);

-- Logic 
-- create function that is triggered by status_code = 2 (approved)
CREATE OR REPLACE FUNCTION log_key_order()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.status_code == 2 THEN
		 INSERT INTO key_order (transaction_id, access_code_id)
		 VALUES(OLD.request_id, OLD.access_code_id);
	END IF;

	RETURN NEW;
END;
$$;

CREATE TRIGGER request_approved_create_order
  AFTER UPDATE
  ON requests
  FOR EACH ROW
  EXECUTE PROCEDURE log_key_order();
  

-- cannot make access_code_id a FK since it is not a primary key in requests table
-- instead of making a constraint, I will add this information via a trigger function
CREATE TABLE key_orders (
	transaction_id INT PRIMARY KEY REFERENCES requests (request_id),
	access_code_id INT
);

		
-- -- Need to add logic so access code is programatically obtained
-- INSERT INTO key_orders (transaction_id, access_code_id)
-- VALUES (1, 3),
-- 		(2, 1),
-- 		(3, 2),
-- 		(4, 2),
-- 		(5, 2);


CREATE TABLE access_pairs (
	access_code_id INT REFERENCES access_codes (access_code_id),
	space_number_id VARCHAR REFERENCES rooms (space_number_id),
	PRIMARY KEY (access_code_id, space_number_id) 
);

SELECT * FROM access_codes;

INSERT INTO access_pairs (access_code_id, space_number_id)
VALUES (1, '24-01-01-01'),
		(2, '24-02-01-01'),
		(2, '24-02-01-02'),
		(3, '24-01-01-01'),
		(3, '24-02-01-01'),
		(3, '24-02-01-02');
		
CREATE TABLE fabrication_status (
	fabrication_status_id SERIAL PRIMARY KEY,
	fabrication_status VARCHAR
);		

INSERT INTO fabrication_status (fabrication_status)
VALUES ('IN QUEUE'),
		('SCHEDULED'),
		('COMPLETED');

CREATE TABLE keys_created (
	key_number INT,
	key_copy INT,
	access_code_id INT REFERENCES access_codes (access_code_id),
	fabrication_status_id INT REFERENCES fabrication_status (fabrication_status_id),
	PRIMARY KEY (key_number, key_copy)
);

INSERT INTO keys_created (key_number, key_copy, access_code_id, fabrication_status_id)
VALUES (43221, 1, 3, 3),
		(56432, 1, 1, 3),
		(34523, 1, 2, 3),
		(46363, 2, 2, 3),
		(59873, 3, 2, 3);


CREATE TABLE key_status (
	key_status_id SERIAL PRIMARY KEY,
	key_status VARCHAR 
);

INSERT INTO key_status (key_status)
VALUES ('ISSUED'),
		('INVENTORY'),
		('ASSIGNED FOR PICKUP'),
		('BROKEN'),
		('LOST');

CREATE TABLE key_inventory (
	transaction_id INT REFERENCES key_orders (transaction_id),
	key_number INT,
	key_copy INT,
	key_status_id INT REFERENCES key_status (key_status_id),
	date_transferred TIMESTAMP NOT NULL DEFAULT NOW(),
	date_returned TIMESTAMP,
	PRIMARY KEY (transaction_id, key_number, key_copy),
	FOREIGN KEY (key_number, key_copy) REFERENCES keys_created (key_number, key_copy)
);


-- This will initiate some of the logic
-- logic needs built to complete this request via forms  
INSERT INTO requests (user_id, space_number_id, building_number, access_approver_id, access_code_id, status_code)
VALUES (1, '24-01-01-01', 24, 1, 1, 1),
		(2, '24-01-01-01', 24, 1, 2, 1),
		(3, '24-01-01-01', 24, 1, 2, 1),
		(4, '24-01-01-01', 24, 1, 2, 1),
		(5, '24-01-01-01', 24, 1, 3, 1);


-- INSERT INTO key_inventory (transaction_id, key_number, key_copy, key_status_id)
-- VALUES (1, 43221, 1, 1),
-- 		(2, 56432, 1, 1),
-- 		(3, 59873, 3, 1),
-- 		(4, 34523, 1, 1),
-- 		(5, 46363, 2, 1);

--  determine if key is available in inventory



-- PROGRAM EXECUTION -------------------------------------------------------------------
-- 1.  Web Interface to ADD users, buildings, rooms, access_approvers, access_codes
-- 2.  Web Interface to INITIATE key requests starting with the requests table
-- 3.  Request Form starts from User requesting room access.  The form includes 
-- 	a table where new room requests can be added.  When clicking New the popup
-- 	contains input of buiding, wing, and room number.  The space_number is 
-- 	generated from a query.  The space_number is then used to populate a dropdown
-- 	for the space approver.   Additional spaces can be added.
-- 	The submit button then calculates the access_codes and approvers.  The request 
-- 	table has the information inserted into the table for each key determined with
-- 	status_code of 1 (REQUEST SUBMITTED).  
-- 4.  On Submit, the appropriate Approvers action items is update.  The approver clicks
-- 	the action item and can accept or reject and provide a comment. On approval, the
-- 	status_code is updated to REQUEST APPROVED, approved set to TRUE, and 
-- 	approved_comment is updated.  On rejection, the status_code is updated to REQUEST
-- 	REJECTED, approved set to FALSE, and rejected_comment is updated.  The user 
-- 	interface is updated with status updates and comments.  The submit button is now
-- 	replaced with a MODIFY button which pulls up a form containing the request information 
-- 	from the original request.  The change to the space_number or maybe the status_code to
-- 	REQUEST SUBMITTED should trigger resubmit to approver. 
-- 	Note:  The interface for Approvers should default to only show 'REQUEST SUBMITTED' for
-- 	that approver on their home page.  
-- 5.  On change of status_code to 'REQUEST APPROVED' a trigger is enacted and the key_order
-- 	table is updated.
-- 6.  The key_order form should check for available keys in the key_inventory and if there
-- 	are no matches then the keys_created table is updated.  The keyshop makes the key
-- 	based on the access_code.  When complete, the fabrication_status_id of 3 is updated
-- 	and this triggers the update of the key_inventory table and the update of the key_orders
-- 	table.  The key_copy is also updated.
-- 	Note:  The keyshop requests should only display items NOT COMPLETE.
-- 7.  Upon the user picking up the key, the admin staff updates the key_inventory to show 
-- 	the status to be 'ISSUED'
-- 8.  At the final stage after pickup - the key_inventory, key_created, and key_orders

-- Does key_orders need a status for the user to know the status?
 
		
		
